from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from abc import ABC, abstractmethod

from zen_creator.elements import ConversionTechnology
from zen_creator.utils.attribute import Attribute


class RetrofittingTechnology(ConversionTechnology, ABC):
    subpath = "set_retrofitting_technologies"
    name = "retrofitting_technology"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model, power_unit=power_unit)

        # copy attributes from superclass
        # copy to prevent override
        self._attribute_names = list(self._attribute_names)

        # attributes which are added in this class
        self._subclass_attribute_names = [
            "retrofit_flow_coupling_factor",
            "retrofit_reference_carrier",
        ]
        self._attribute_names.extend(self._subclass_attribute_names)

        # initialize all attributes to default values
        self.set_default_values_retrofitting_technology()

    def set_default_values_retrofitting_technology(self):
        """Initialize internal attributes to default values."""
        self._retrofit_flow_coupling_factor = Attribute(
            name="retrofit_flow_coupling_factor", default_value=1.0, element=self
        )
        self._retrofit_reference_carrier = Attribute(
            name="retrofit_reference_carrier", default_value=[], element=self
        )

    # ---------- Properties ----------

    @property
    def retrofit_flow_coupling_factor(self) -> Attribute:
        return self._retrofit_flow_coupling_factor

    @retrofit_flow_coupling_factor.setter
    def retrofit_flow_coupling_factor(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._retrofit_flow_coupling_factor = value

    @property
    def retrofit_reference_carrier(self) -> Attribute:
        return self._retrofit_reference_carrier

    @retrofit_reference_carrier.setter
    def retrofit_reference_carrier(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._retrofit_reference_carrier = value

    # ---------- Mandatory attributes to be filled for each technology ----------

    @abstractmethod
    def _set_retrofit_flow_coupling_factor(self) -> Attribute:
        raise NotImplementedError(
            "All subclasses of RetrofittingTechnology must "
            "implement `_set_retrofit_flow_coupling_factor()`"
        )

    @abstractmethod
    def _set_retrofit_reference_carrier(self) -> Attribute:
        raise NotImplementedError(
            "All subclasses of RetrofittingTechnology must "
            "implement `_set_retrofit_reference_carrier()`"
        )


class GenericRetrofittingTechnology(RetrofittingTechnology):

    name: str = "generic_retrofitting_technology"  # for element registry

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
        attr = self.reference_carrier  # get default value
        return attr

    def _set_input_carrier(self) -> Attribute:
        attr = self.input_carrier  # get default value`
        return attr

    def _set_output_carrier(self) -> Attribute:
        attr = self.output_carrier  # get default value
        return attr

    def _set_retrofit_flow_coupling_factor(self) -> Attribute:
        attr = self.retrofit_flow_coupling_factor  # get default value
        return attr

    def _set_retrofit_reference_carrier(self) -> Attribute:
        attr = self.retrofit_reference_carrier  # get default value
        return attr
