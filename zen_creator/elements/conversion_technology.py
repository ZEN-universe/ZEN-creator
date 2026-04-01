from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from abc import ABC, abstractmethod

from zen_creator.elements.technology import Technology
from zen_creator.utils.attribute import Attribute


class ConversionTechnology(Technology, ABC):

    subpath = "set_conversion_technologies"
    name = "conversion_technology"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

        # copy attributes from superclass
        # copy to prevent override
        self._attribute_names = list(self._attribute_names)

        # attributes which are added in this class
        self._subclass_attribute_names = [
            "capex_specific_conversion",
            "input_carrier",
            "output_carrier",
            "conversion_factor",
            "min_full_load_hours_fraction",
        ]
        self._attribute_names.extend(self._subclass_attribute_names)

        # initialize all attributes to default values
        self.set_default_values_conversion_technology()

    def set_default_values_conversion_technology(self):
        """Initialize internal attributes to default values."""
        self._capex_specific_conversion = Attribute(
            "capex_specific_conversion",
            default_value=0.0,
            unit=f"Euro/({self.power_unit})",
            element=self,
        )
        self._conversion_factor = Attribute(
            name="conversion_factor",
            default_value=[],
            element=self,
        )
        self.min_full_load_hours_fraction = Attribute(
            name="min_full_load_hours_fraction",
            default_value=0,
            element=self,
        )
        self._input_carrier = self._set_input_carrier()
        self._output_carrier = self._set_output_carrier()

    # ---------- Properties ----------

    @property
    def capex_specific_conversion(self) -> Attribute:
        return self._capex_specific_conversion

    @capex_specific_conversion.setter
    def capex_specific_conversion(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._capex_specific_conversion = value

    @property
    def input_carrier(self) -> Attribute:
        return self._input_carrier

    @input_carrier.setter
    def input_carrier(self, value: Attribute) -> None:
        self._validate_attribute(value)
        old_default_value = self._input_carrier.default_value
        new_default_value = value.default_value
        if old_default_value and old_default_value != new_default_value:
            raise ValueError(
                "Input carrier cannot be changed once set. Old value:"
                f"{old_default_value}, new value {new_default_value}"
            )
        self._input_carrier = value

    @property
    def output_carrier(self) -> Attribute:
        return self._output_carrier

    @output_carrier.setter
    def output_carrier(self, value: Attribute) -> None:
        self._validate_attribute(value)
        old_default_value = self._output_carrier.default_value
        new_default_value = value.default_value
        if old_default_value and old_default_value != new_default_value:
            raise ValueError(
                "Output carrier cannot be changed once set. Old value:"
                f"{old_default_value}, new value {new_default_value}"
            )
        self._output_carrier = value

    @property
    def conversion_factor(self) -> Attribute:
        return self._conversion_factor

    @conversion_factor.setter
    def conversion_factor(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._conversion_factor = value


    @property
    def min_full_load_hours_fraction(self) -> Attribute:
        return self._min_full_load_hours_fraction

    @min_full_load_hours_fraction.setter
    def min_full_load_hours_fraction(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._min_full_load_hours_fraction = value

    # ---------- Mandatory attributes to be filled for each technology --------

    @abstractmethod
    def _set_input_carrier(self) -> Attribute:
        raise NotImplementedError(
            "All subclasses of ConversionTechnology must "
            "implement `_set_input_carrier()`"
        )

    @abstractmethod
    def _set_output_carrier(self) -> Attribute:
        raise NotImplementedError(
            "All subclasses of ConversionTechnology must "
            "implement `_set_output_carrier()`"
        )

    @abstractmethod
    def _set_conversion_factor(self) -> Attribute:
        raise NotImplementedError(
            "All subclasses of ConversionTechnology must "
            "implement `_set_conversion_factor()`"
        )


class GenericConversionTechnology(ConversionTechnology):

    name: str = "generic_conversion_technology"  # for element registry

    def __init__(self, name: str, model: Model, power_unit: str = "MW"):
        self.name = name  # overwrite with new name
        super().__init__(model=model, power_unit=power_unit)

    def _set_lifetime(self) -> Attribute:
        attr = self.lifetime  # get default value
        return attr

    def _set_conversion_factor(self) -> Attribute:
        attr = self.conversion_factor  # get default value
        return attr

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(name="reference_carrier", default_value=[], element=self)

    def _set_input_carrier(self) -> Attribute:
        return Attribute(name="input_carrier", default_value=[], element=self)

    def _set_output_carrier(self) -> Attribute:
        return Attribute(name="output_carrier", default_value=[], element=self)
