from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, ClassVar, Type

if TYPE_CHECKING:
    from zen_creator.model import Model
    from zen_creator.utils.attribute import Attribute
    from zen_creator.utils.default_config import Config
import json
from pathlib import Path

from zen_creator.utils.attribute import Attribute
from zen_creator.utils.registry import Registry


class Element(Registry["Element"], ABC):
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

        # set public attribute values
        self.model: Model = model
        self.config: Config = model.config
        self.power_unit: str = power_unit

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
            setter = getattr(self, f"_set_{name}", None)
            if setter:
                setattr(self, name, setter())

    def _validate_attribute(self, value: Attribute) -> None:
        """Validate that the value is an Attribute instance.

        Args:
            value (Attribute): The value to validate.

        Raises:
            TypeError: If value is not an Attribute instance.
        """
        if not isinstance(value, Attribute):
            raise TypeError(
                f"Value must be an instance of Attribute, got {type(value)}"
            )

    def write(self):
        """Write the element to disk.

        This method saves the attributes.json file and any associated
        data files.
        """
        # write attributes.json file
        self.save_attributes()

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
        """Save the element's attributes to attributes.json."""
        print(f"Saving 'attributes.json' for element '{self.name}' ...")

        out_path = self.output_path
        output = self.attributes_to_dict()
        with (out_path / "attributes.json").open("w") as f:
            json.dump(output, f, indent=4)

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
                output_lines.append(attr.sources_to_string())
                output_lines.append("")

        if not has_sources:
            output_lines.extend(["_No sources available._", ""])

        return "\n".join(output_lines).rstrip()
