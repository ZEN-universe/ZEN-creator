from __future__ import annotations
from typing import TYPE_CHECKING, ClassVar, Type

if TYPE_CHECKING:
    from zen_creator.model import Model
    from zen_creator.utils.default_config import Config
    from zen_creator.utils.attribute import Attribute
from zen_creator.utils.attribute import Attribute
import json
from pathlib import Path


class Element:
    subpath: ClassVar[str] = ""
    _element_registry: dict[str, Type[Element]] = {}

    def __init__(self, name: str, model: Model, power_unit: str = "MW"):

        # Attributes that should be saved
        self._attribute_names: list[str] = []

        # set public attribute values
        self.name: str = name
        self.model: Model = model
        self.config: Config = model.config
        self.power_unit: str = power_unit
        self.source_path: Path = model.source_path

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "name"):
            raise Exception(
                f"Subclass {cls.__name__} should define a class variable " "" "'name'."
            )
        Element._element_registry[cls.name] = cls

    # ----------- properties ------------------------------------------

    @property
    def attributes(self) -> dict[str, Attribute]:
        return {name: getattr(self, name) for name in self._attribute_names}

    @property
    def relative_output_path(self) -> Path:
        """
        Get output path relative to root model directory.
        """
        path = Path(self.name)
        for _cls in self.__class__.mro()[1:]:
            if hasattr(_cls, "subpath"):
                path = Path(_cls.subpath) / path

        return path

    @property
    def output_path(self) -> Path:
        """
        Get absolute output path and ensure directory exists
        """
        output_path = self.get_output_path()
        output_path.mkdir(parents=True, exist_ok=True)

        return output_path

    # ------- methods for building -------------------------------------

    def overwrite_from_existing_model(self, existing_model_path: Path):
        existing_element_path = existing_model_path / self.relative_output_path
        for attribute in self.attributes.values():
            attribute.overwrite_from_existing_model(existing_element_path)

    def build(self):
        """
        Sets self.<attribute_name> = self._set_<attribute_name>() for all
        attributes
        """
        for name in self._attribute_names:
            setter = getattr(self, f"_set_{name}", None)
            if setter:
                setattr(self, name, setter())

    # Methods for validating
    def _validate_attribute(self, value: Attribute) -> None:
        """Validate that the value is an Attribute instance."""
        if not isinstance(value, Attribute):
            raise TypeError(
                f"Value must be an instance of Attribute, got {type(value)}"
            )

    # ----------- methods for saving ---------------------------
    def get_output_path(self) -> Path:
        """
        Get path to element and create that directory
        """
        return self.model.out_path / self.relative_output_path

    def attributes_to_dict(self) -> dict:
        output = {}
        for attr_name in self._attribute_names:
            attr = getattr(self, attr_name)
            output[attr_name] = attr.default_to_dict()
        return output

    def save_attributes(self):
        print(f"Saving 'attributes.json' for element '{self.name}' ...")

        out_path = self.output_path
        output = self.attributes_to_dict()
        with (out_path / "attributes.json").open("w") as f:
            json.dump(output, f, indent=4)

    def save_data(self):

        out_path = self.output_path

        for attr_name in self._attributes_list:
            attr = getattr(self, attr_name)
            attr.save_data(out_path, self.name)
