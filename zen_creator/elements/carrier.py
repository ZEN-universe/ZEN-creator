from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

import numpy as np

from zen_creator.elements.element import Element
from zen_creator.utils.attribute import Attribute


class Carrier(Element):
    subpath = "set_carriers"
    name = "carrier"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model = model, power_unit=power_unit)

        # copy attributes from superclass
        self._attribute_names = list(self._attribute_names)  # copy to prevent override

        # attributes which are added in this class
        self._subclass_attribute_names = [
            "demand",
            "availability_import",
            "availability_export",
            "availability_import_yearly",
            "availability_export_yearly",
            "price_import",
            "price_export",
            "carbon_intensity_carrier_import",
            "carbon_intensity_carrier_export",
            "price_shed_demand",
        ]
        self._attribute_names.extend(self._subclass_attribute_names)

        # initialize all attributes to default values
        self.set_default_values()

    def set_default_values(self):
        """Initialize internal attributes to default values."""
        self._demand = Attribute(
            "demand", default_value=0.0, unit=f"{self.power_unit}", element=self
        )
        self._availability_import = Attribute(
            "availability_import",
            default_value=0.0,
            unit=f"{self.power_unit}",
            element=self,
        )
        self._availability_export = Attribute(
            "availability_export",
            default_value=0.0,
            unit=f"{self.power_unit}",
            element=self,
        )
        self._availability_import_yearly = Attribute(
            "availability_import_yearly",
            default_value=0.0,
            unit=f"{self.power_unit}*h",
            element=self,
        )
        self._availability_export_yearly = Attribute(
            "availability_export_yearly",
            default_value=0.0,
            unit=f"{self.power_unit}*h",
            element=self,
        )
        self._price_import = Attribute(
            "price_import",
            default_value=0.0,
            unit=f"Euro/({self.power_unit}*h)",
            element=self,
        )
        self._price_export = Attribute(
            "price_export",
            default_value=0.0,
            unit=f"Euro/({self.power_unit}*h)",
            element=self,
        )
        self._carbon_intensity_carrier_import = Attribute(
            "carbon_intensity_carrier_import",
            default_value=0.0,
            unit=f"kilotons/({self.power_unit}*h)",
            element=self,
        )
        self._carbon_intensity_carrier_export = Attribute(
            "carbon_intensity_carrier_export",
            default_value=0.0,
            unit=f"kilotons/({self.power_unit}*h)",
            element=self,
        )
        self._price_shed_demand = Attribute(
            "price_shed_demand",
            default_value=np.inf,
            unit=f"Euro/({self.power_unit}*h)",
            element=self,
        )

    # ---------- Properties ----------

    @property
    def demand(self) -> Attribute:
        return self._demand

    @demand.setter
    def demand(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._demand = value

    @property
    def availability_import(self) -> Attribute:
        return self._availability_import

    @availability_import.setter
    def availability_import(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._availability_import = value

    @property
    def availability_export(self) -> Attribute:
        return self._availability_export

    @availability_export.setter
    def availability_export(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._availability_export = value

    @property
    def availability_import_yearly(self) -> Attribute:
        return self._availability_import_yearly

    @availability_import_yearly.setter
    def availability_import_yearly(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._availability_import_yearly = value

    @property
    def availability_export_yearly(self) -> Attribute:
        return self._availability_export_yearly

    @availability_export_yearly.setter
    def availability_export_yearly(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._availability_export_yearly = value

    @property
    def price_import(self) -> Attribute:
        return self._price_import

    @price_import.setter
    def price_import(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._price_import = value

    @property
    def price_export(self) -> Attribute:
        return self._price_export

    @price_export.setter
    def price_export(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._price_export = value

    @property
    def carbon_intensity_carrier_import(self) -> Attribute:
        return self._carbon_intensity_carrier_import

    @carbon_intensity_carrier_import.setter
    def carbon_intensity_carrier_import(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._carbon_intensity_carrier_import = value

    @property
    def carbon_intensity_carrier_export(self) -> Attribute:
        return self._carbon_intensity_carrier_export

    @carbon_intensity_carrier_export.setter
    def carbon_intensity_carrier_export(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._carbon_intensity_carrier_export = value

    @property
    def price_shed_demand(self) -> Attribute:
        return self._price_shed_demand

    @price_shed_demand.setter
    def price_shed_demand(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._price_shed_demand = value
