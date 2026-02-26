from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.element import Element
from zen_creator.utils.attribute import Attribute


class Technology(Element, ABC):
    subpath = "set_technologies"
    name = "technology"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model, power_unit=power_unit)

        # copy attributes from superclass
        self._attribute_names = list(self._attribute_names)  # copy to prevent override

        # attributes which are added in this class
        self._subclass_attribute_names = [
            "capacity_addition_min",
            "capacity_addition_max",
            "capacity_addition_unbounded",
            "capacity_existing",
            "capacity_limit",
            "min_load",
            "max_load",
            "opex_specific_variable",
            "opex_specific_fixed",
            "carbon_intensity_technology",
            "construction_time",
            "capacity_investment_existing",
            "max_diffusion_rate",
            "lifetime",
            "reference_carrier",
        ]
        self._attribute_names.extend(self._subclass_attribute_names)

        # initialize all attributes to default values
        self.set_default_values_technology()

        ## dynamic property generation

        # for name in self._attribute_names:
        #     prop_name = name
        #     private_name = f"_{name}"

        #     def getter(self, _private_name=private_name):
        #         return getattr(self, _private_name)

        #     setattr(Technology, prop_name, property(getter))

    def set_default_values_technology(self):

        # initialize internal attributes to default values
        self._capacity_addition_min = Attribute(
            "capacity_addition_min",
            default_value=0.0,
            unit=self.power_unit,
            element=self,
        )
        self._capacity_addition_max = Attribute(
            "capacity_addition_max",
            default_value=np.inf,
            unit=self.power_unit,
            element=self,
        )
        self._capacity_addition_unbounded = Attribute(
            "capacity_addition_unbounded",
            default_value=0.0,
            unit=self.power_unit,
            element=self,
        )
        self._capacity_existing = Attribute(
            "capacity_existing",
            default_value=0.0,
            unit=f"{self.power_unit}",
            element=self,
        )
        self._capacity_limit = Attribute(
            "capacity_limit",
            default_value=np.inf,
            unit=f"{self.power_unit}",
            element=self,
        )
        self._min_load = Attribute(
            "min_load", default_value=0.0, unit="1", element=self
        )
        self._max_load = Attribute(
            "max_load", default_value=1.0, unit="1", element=self
        )
        self._opex_specific_variable = Attribute(
            "opex_specific_variable",
            default_value=0.0,
            unit=f"Euro/({self.power_unit}*h)",
            element=self,
        )
        self._opex_specific_fixed = Attribute(
            "opex_specific_fixed",
            default_value=0.0,
            unit=f"Euro/({self.power_unit})",
            element=self,
        )
        self._carbon_intensity_technology = Attribute(
            "carbon_intensity_technology",
            default_value=0.0,
            unit=f"kilotons/({self.power_unit}*h)",
            element=self,
        )
        self._construction_time = Attribute(
            "construction_time", default_value=0, unit="1", element=self
        )
        self._capacity_investment_existing = Attribute(
            "capacity_investment_existing",
            default_value=0.0,
            unit=f"{self.power_unit}",
            element=self,
        )
        self._max_diffusion_rate = Attribute(
            "max_diffusion_rate", default_value=np.inf, unit="1", element=self
        )
        self._lifetime = Attribute(
            "lifetime", default_value=np.nan, unit="1", element=self
        )
        self._reference_carrier = self._set_reference_carrier()

    # ---------- Properties ----------

    @property
    def capacity_addition_min(self) -> Attribute:
        return self._capacity_addition_min

    @capacity_addition_min.setter
    def capacity_addition_min(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._capacity_addition_min = value

    @property
    def capacity_addition_max(self) -> Attribute:
        return self._capacity_addition_max

    @capacity_addition_max.setter
    def capacity_addition_max(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._capacity_addition_max = value

    @property
    def capacity_addition_unbounded(self) -> Attribute:
        return self._capacity_addition_unbounded

    @capacity_addition_unbounded.setter
    def capacity_addition_unbounded(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._capacity_addition_unbounded = value

    @property
    def capacity_existing(self) -> Attribute:
        return self._capacity_existing

    @capacity_existing.setter
    def capacity_existing(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._capacity_existing = value

    @property
    def capacity_limit(self) -> Attribute:
        return self._capacity_limit

    @capacity_limit.setter
    def capacity_limit(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._capacity_limit = value

    @property
    def min_load(self) -> Attribute:
        return self._min_load

    @min_load.setter
    def min_load(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._min_load = value

    @property
    def max_load(self) -> Attribute:
        return self._max_load

    @max_load.setter
    def max_load(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._max_load = value

    @property
    def opex_specific_variable(self) -> Attribute:
        return self._opex_specific_variable

    @opex_specific_variable.setter
    def opex_specific_variable(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._opex_specific_variable = value

    @property
    def opex_specific_fixed(self) -> Attribute:
        return self._opex_specific_fixed

    @opex_specific_fixed.setter
    def opex_specific_fixed(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._opex_specific_fixed = value

    @property
    def carbon_intensity_technology(self) -> Attribute:
        return self._carbon_intensity_technology

    @carbon_intensity_technology.setter
    def carbon_intensity_technology(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._carbon_intensity_technology = value

    @property
    def construction_time(self) -> Attribute:
        return self._construction_time

    @construction_time.setter
    def construction_time(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._construction_time = value

    @property
    def capacity_investment_existing(self) -> Attribute:
        return self._capacity_investment_existing

    @capacity_investment_existing.setter
    def capacity_investment_existing(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._capacity_investment_existing = value

    @property
    def max_diffusion_rate(self) -> Attribute:
        return self._max_diffusion_rate

    @max_diffusion_rate.setter
    def max_diffusion_rate(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._max_diffusion_rate = value

    @property
    def lifetime(self) -> Attribute | None:
        return self._lifetime

    @lifetime.setter
    def lifetime(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._lifetime = value

    @property
    def reference_carrier(self) -> Attribute:
        return self._reference_carrier

    @reference_carrier.setter
    def reference_carrier(self, value: Attribute):
        """
        Validate reference carrier when set.

        - must be an attribure
        - cannot change after being set
        """
        self._validate_attribute(value)

        old_default_value = self._reference_carrier.default_value
        new_default_value = value.default_value
        if old_default_value and old_default_value != new_default_value:
            raise ValueError(
                "Reference carrier cannot be changed once set. Old value:"
                f"{old_default_value}, new value {new_default_value}"
            )

        self._reference_carrier = value

    # ---------- Mandatory attributes to be filled for each technology --------
    @abstractmethod
    def _set_lifetime(self) -> Attribute:
        raise NotImplementedError(
            "All subclasses of Technology must implement `_set_lifetime()`"
        )

    @abstractmethod
    def _set_reference_carrier(self) -> Attribute:
        raise NotImplementedError(
            "All subclasses of Technology must implement " "`_set_reference_carrier()`"
        )
