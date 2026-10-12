from __future__ import annotations

import logging
from abc import ABC
from typing import TYPE_CHECKING, ClassVar, Type

if TYPE_CHECKING:
    from zen_creator.model import Model
    from zen_creator.utils.attribute import Attribute
    from zen_creator.utils.config import Config
    from zen_creator.utils.settings import Settings
from pathlib import Path

import yaml

from zen_creator.utils.attribute import Attribute
from zen_creator.utils.registry import Registry
from zen_creator.utils.utils import get_energy_unit_from_power_unit

logger = logging.getLogger(__name__)


class Element(ABC, Registry["Element"], is_base_registry=True):
    """Base class for all elements in the ZEN model.

    This class provides the foundation for carriers, technologies, and other
    model components. It handles attribute management, path resolution, and
    serialization.

    Attributes:
        name (str): The name of the element.
        subpath (ClassVar[str]): Subpath for organizing element files.
        _element_registry (dict[str, Type[Element]]): Registry of all element classes.
    """

    name: str = "element"
    subpath: ClassVar[str] = ""
    _element_registry: dict[str, Type[Element]] = {}

    def __init__(self, model: Model, power_unit: str = "MW"):
        """Initialize an Element instance.

        Args:
            model (Model): The model this element belongs to.
            power_unit (str): The unit for power values. Defaults to "MW".
        """
        # Attributes that should be saved
        self._attribute_names: list[str] = []

        # names of attributes whose _set_<name> setter has already run, see
        # _build_attribute
        self._built_attribute_names: set[str] = set()

        # set public attribute values
        self.model: Model = model
        self.config: Config = model.config
        self.settings: Settings = model.settings
        self.power_unit: str = power_unit
        self.energy_unit: str = get_energy_unit_from_power_unit(power_unit)

    # ----------- properties ------------------------------------------

    @property
    def attributes(self) -> dict[str, Attribute]:
        """Dictionary of all attributes for this element.

        Returns:
            dict[str, Attribute]: Mapping of attribute names to Attribute
                objects.
        """
        return {name: getattr(self, name) for name in self._attribute_names}

    @property
    def scenario_key(self) -> str:
        """Get the key of this element in scenarios.yaml.

        Returns:
            str: The name under which scenarios address this element.
        """
        return self.name

    @property
    def relative_output_path(self) -> Path:
        """Get the relative output path for this element.

        The path is constructed by combining the element name with subpaths
        from the class hierarchy.

        Returns:
            Path: The relative path for output files.
        """
        path = Path(self.name)
        for _cls in self.__class__.mro()[1:]:
            if hasattr(_cls, "subpath"):
                path = Path(_cls.subpath) / path

        return path

    @property
    def output_path(self) -> Path:
        """Get the absolute output path and ensure the directory exists.

        Side Effects:
            Creates the output path if it does not exist.

        Returns:
            Path: The absolute path to the output directory for this element.
        """
        output_path = self.get_output_path()
        output_path.mkdir(parents=True, exist_ok=True)

        return output_path

    @property
    def source_path(self) -> Path:
        """Get the source path of the model where the raw data is located.

        Returns:
            Path: The source path to the raw data.
        """

        return self.model.source_path

    # ------- methods for building -------------------------------------

    def overwrite_from_existing_model(self, existing_model_path: Path):
        """Overwrite attributes with values from an existing model.

        Args:
            existing_model_path (Path): Path to the existing model directory.
        """
        existing_element_path = existing_model_path / self.relative_output_path
        for attribute in self.attributes.values():
            attribute.overwrite_from_existing_model(existing_element_path)

    def build(self):
        """Build the element by setting attributes from their setters.

        This method calls the _set_<attribute_name> methods whenever
        these exist. The attributes are set to the output of these
        methods.
        """
        for name in self._attribute_names:
            self._build_attribute(name)

    def _build_attribute(self, name: str) -> None:
        """Build a single attribute via its ``_set_<name>`` setter.

        Idempotent: does nothing if ``name`` has already been built, or has
        no ``_set_<name>`` setter (its default/loaded value is final). Safe
        to call re-entrantly from within another attribute's setter - this
        is how cross-attribute and cross-element dependencies (e.g. a
        technology reading a related technology's already-built lifetime)
        get built on demand regardless of ``_attribute_names`` order. See
        ``Attribute.__getattribute__`` for the read-triggered call site.

        Raises:
            RuntimeError: If ``name`` of this element is already being built
                further up the call chain (a cyclic attribute dependency).
        """
        if name in self._built_attribute_names:
            return
        setter = getattr(self, f"_set_{name}", None)
        if setter is None:
            return

        stack = self.model._build_stack
        frame = (self, name)
        if frame in stack:
            chain = " -> ".join(f"{el.name}.{attr}" for el, attr in stack)
            raise RuntimeError(
                f"Cyclic attribute dependency detected: {chain} -> "
                f"{self.name}.{name}"
            )

        stack.append(frame)
        try:
            setattr(self, name, setter())
        finally:
            stack.pop()
        self._built_attribute_names.add(name)

    def _validate_attribute(self, value: Attribute) -> None:
        """Validate that the value is an Attribute instance.

        Args:
            value (Attribute): The value to validate.

        Raises:
            TypeError: If value is not an Attribute instance.
        """
        if not isinstance(value, Attribute):
            if value is None:
                raise TypeError(
                    f"No attribute returned for '{self.name}'. "
                    "Ensure that all _set_<attribute_name> methods "
                    "return an Attribute instance."
                )
            else:
                raise TypeError(
                    f"Setter returned {type(value)} for '{self.name}',"
                    " must be an instance of Attribute, "
                    f"but got {type(value)}."
                )

    def write(self):
        """Write the element to disk.

        This method saves the attributes.yaml file and any associated
        data files.
        """
        # write attributes.yaml file
        self.save_attributes()

        # write sources.md file
        self.save_sources()

        # write data files
        self.save_data()

    def get_output_path(self) -> Path:
        """Get the path to the element output directory and create it.

        Returns:
            Path: The absolute path to the element's output directory.
        """
        return self.model.output_path / self.relative_output_path

    def attributes_to_dict(self) -> dict:
        """Convert element attributes to a dictionary for serialization.

        Returns:
            dict: Dictionary representation of the element's attributes.
        """
        output = {}
        for attr_name in self._attribute_names:
            attr = getattr(self, attr_name)

            # skip for attributes such as set_nodes or set_edges with not default
            if attr.default_value is not None:
                output[attr_name] = attr.default_to_dict()

        return output

    def save_attributes(self):
        """Save the element's attributes to attributes.yaml."""
        logger.info(f"Saving 'attributes.yaml' for element '{self.name}.'")

        out_path = self.output_path
        output = self.attributes_to_dict()
        with (out_path / "attributes.yaml").open("w") as f:
            yaml.safe_dump(output, f, sort_keys=False)

        self.save_scenario_attributes(output)

    def save_scenario_attributes(self, base_attributes: dict):
        """Save one attributes file per scenario that changes a default value.

        The scenario files hold a full copy of the attributes, with the default
        values of the scenario applied, since ZEN-garden reads them in place of
        'attributes.yaml'.

        Args:
            base_attributes (dict): The attributes of the default scenario.
        """
        overrides: dict[str, dict] = {}

        for attr_name in self._attribute_names:
            attr = getattr(self, attr_name)
            for scenario in attr.scenarios.values():
                if scenario.default_value is None:
                    continue
                overrides.setdefault(scenario.suffix, {})[attr_name] = (
                    attr.scenario_default_to_dict(scenario)
                )

        out_path = self.output_path
        for suffix, attributes in overrides.items():
            logger.info(f"Saving 'attributes_{suffix}.yaml' for element '{self.name}.'")
            with (out_path / f"attributes_{suffix}.yaml").open("w") as f:
                yaml.safe_dump({**base_attributes, **attributes}, f, sort_keys=False)

    def save_sources(self):
        """Save the element's sources to sources.md."""
        if not any(
            getattr(self, attr_name).sources for attr_name in self._attribute_names
        ):
            return

        logger.debug(f"Saving 'sources.md' for element '{self.name}.'")

        out_path = self.output_path
        with (out_path / "sources.md").open("w") as f:
            f.write(self.sources_to_str())

    def save_data(self):
        """Save the element's data files."""
        out_path = self.output_path

        for attr_name in self._attribute_names:
            attr = getattr(self, attr_name)
            attr.save_data(out_path, self.name)

    def sources_to_str(self) -> str:
        """Convert the sources of all attributes to a markdown page.

        Returns:
            str: A markdown-formatted string of all sources for this element.
        """
        output_lines = [self.name, "=" * len(self.name), ""]
        has_sources = False

        for attr_name in self._attribute_names:
            attr = getattr(self, attr_name)
            if attr.sources:
                has_sources = True
                output_lines.extend([attr_name, "-" * len(attr_name), ""])
                output_lines.append(attr.sources_to_str())
                output_lines.append("")

        if not has_sources:
            output_lines.extend(["_No sources available._", ""])

        return "\n".join(output_lines).rstrip()
