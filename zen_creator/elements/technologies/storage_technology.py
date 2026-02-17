from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.technologies.technology import Technology
from zen_creator.utils.attribute import Attribute

from abc import ABC, abstractmethod
import numpy as np


class StorageTechnology(Technology, ABC):
    subpath = "set_storage_technologies"
    name = "storage_technology"

    def __init__(self, name: str, model: Model, power_unit: str = "MW"):
        super().__init__(name, model, power_unit=power_unit)

        # copy attributes from superclass
        self._attribute_names = list(self._attribute_names)  # copy to prevent override

        # attributes which are added in this class
        self._subclass_attribute_names = [
            "efficiency_charge",
            "efficiency_discharge",
            "self_discharge",
            "capex_specific_storage",
            "capex_specific_storage_energy",
            "capacity_addition_min_energy",
            "capacity_addition_max_energy",
            "capacity_existing_energy",
            "capacity_limit_energy",
            "min_load_energy",
            "max_load_energy",
            "capacity_investment_existing_energy",
            "opex_specific_fixed_energy",
            "energy_to_power_ratio_min",
            "energy_to_power_ratio_max",
            "flow_storage_inflow",
        ]
        self._attribute_names.extend(self._subclass_attribute_names)

        # initialize all attributes to default values
        self.set_default_values_storage_technology()

    def set_default_values_storage_technology(self):
        """Initialize internal attributes to default values."""
        self._efficiency_charge = Attribute(
            "efficiency_charge", default_value=1.0, unit="1", element=self
        )
        self._efficiency_discharge = Attribute(
            "efficiency_discharge", default_value=1.0, unit="1", element=self
        )
        self._self_discharge = Attribute(
            "self_discharge", default_value=0.0, unit="1", element=self
        )
        self._capex_specific_storage = Attribute(
            "capex_specific_storage",
            default_value=0.0,
            unit=f"Euro/({self.power_unit})",
            element=self,
        )
        self._capex_specific_storage_energy = Attribute(
            "capex_specific_storage_energy",
            default_value=0.0,
            unit=f"Euro/({self.power_unit}*h)",
            element=self,
        )
        self._capacity_addition_min_energy = Attribute(
            "capacity_addition_min_energy",
            default_value=0.0,
            unit=f"{self.power_unit}*h",
            element=self,
        )
        self._capacity_addition_max_energy = Attribute(
            "capacity_addition_max_energy",
            default_value=np.inf,
            unit=f"{self.power_unit}*h",
            element=self,
        )
        self._capacity_existing_energy = Attribute(
            "capacity_existing_energy",
            default_value=0.0,
            unit=f"{self.power_unit}*h",
            element=self,
        )
        self._capacity_limit_energy = Attribute(
            "capacity_limit_energy",
            default_value=np.inf,
            unit=f"{self.power_unit}*h",
            element=self,
        )
        self._min_load_energy = Attribute(
            "min_load_energy", default_value=0.0, unit="1", element=self
        )
        self._max_load_energy = Attribute(
            "max_load_energy", default_value=1.0, unit="1", element=self
        )
        self._capacity_investment_existing_energy = Attribute(
            "capacity_investment_existing_energy",
            default_value=0.0,
            unit=f"{self.power_unit}*h",
            element=self,
        )
        self._opex_specific_fixed_energy = Attribute(
            "opex_specific_fixed_energy",
            default_value=0.0,
            unit=f"Euro/({self.power_unit}*h)",
            element=self,
        )
        self._energy_to_power_ratio_min = Attribute(
            "energy_to_power_ratio_min", default_value=0.0, unit="h", element=self
        )
        self._energy_to_power_ratio_max = Attribute(
            "energy_to_power_ratio_max", default_value=np.inf, unit="h", element=self
        )
        self._flow_storage_inflow = Attribute(
            "flow_storage_inflow",
            default_value=0.0,
            unit=f"{self.power_unit}",
            element=self,
        )

    # ---------- Properties ----------

    @property
    def efficiency_charge(self) -> Attribute:
        return self._efficiency_charge

    @efficiency_charge.setter
    def efficiency_charge(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._efficiency_charge = value

    @property
    def efficiency_discharge(self) -> Attribute:
        return self._efficiency_discharge

    @efficiency_discharge.setter
    def efficiency_discharge(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._efficiency_discharge = value

    @property
    def self_discharge(self) -> Attribute:
        return self._self_discharge

    @self_discharge.setter
    def self_discharge(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._self_discharge = value

    @property
    def capex_specific_storage(self) -> Attribute:
        return self._capex_specific_storage

    @capex_specific_storage.setter
    def capex_specific_storage(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._capex_specific_storage = value

    @property
    def capex_specific_storage_energy(self) -> Attribute:
        return self._capex_specific_storage_energy

    @capex_specific_storage_energy.setter
    def capex_specific_storage_energy(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._capex_specific_storage_energy = value

    @property
    def capacity_addition_min_energy(self) -> Attribute:
        return self._capacity_addition_min_energy

    @capacity_addition_min_energy.setter
    def capacity_addition_min_energy(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._capacity_addition_min_energy = value

    @property
    def capacity_addition_max_energy(self) -> Attribute:
        return self._capacity_addition_max_energy

    @capacity_addition_max_energy.setter
    def capacity_addition_max_energy(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._capacity_addition_max_energy = value

    @property
    def capacity_existing_energy(self) -> Attribute:
        return self._capacity_existing_energy

    @capacity_existing_energy.setter
    def capacity_existing_energy(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._capacity_existing_energy = value

    @property
    def capacity_limit_energy(self) -> Attribute:
        return self._capacity_limit_energy

    @capacity_limit_energy.setter
    def capacity_limit_energy(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._capacity_limit_energy = value

    @property
    def min_load_energy(self) -> Attribute:
        return self._min_load_energy

    @min_load_energy.setter
    def min_load_energy(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._min_load_energy = value

    @property
    def max_load_energy(self) -> Attribute:
        return self._max_load_energy

    @max_load_energy.setter
    def max_load_energy(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._max_load_energy = value

    @property
    def capacity_investment_existing_energy(self) -> Attribute:
        return self._capacity_investment_existing_energy

    @capacity_investment_existing_energy.setter
    def capacity_investment_existing_energy(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._capacity_investment_existing_energy = value

    @property
    def opex_specific_fixed_energy(self) -> Attribute:
        return self._opex_specific_fixed_energy

    @opex_specific_fixed_energy.setter
    def opex_specific_fixed_energy(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._opex_specific_fixed_energy = value

    @property
    def energy_to_power_ratio_min(self) -> Attribute:
        return self._energy_to_power_ratio_min

    @energy_to_power_ratio_min.setter
    def energy_to_power_ratio_min(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._energy_to_power_ratio_min = value

    @property
    def energy_to_power_ratio_max(self) -> Attribute:
        return self._energy_to_power_ratio_max

    @energy_to_power_ratio_max.setter
    def energy_to_power_ratio_max(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._energy_to_power_ratio_max = value

    @property
    def flow_storage_inflow(self) -> Attribute:
        return self._flow_storage_inflow

    @flow_storage_inflow.setter
    def flow_storage_inflow(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._flow_storage_inflow = value
