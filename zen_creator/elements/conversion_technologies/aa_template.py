from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements import ConversionTechnology
from zen_creator.utils.attribute import Attribute


class Template(ConversionTechnology):
    name: str = "template_conversion_technology"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_lifetime(self) -> Attribute:
        attr = self._lifetime
        return attr.set_data(default_value=25, source="assumption")

    def _set_conversion_factor(self) -> Attribute:
        return Attribute(
            name="conversion_factor",
            default_value=[{"electricity": {"default_value": 1, "unit": "GWh/GWh"}}],
            element=self,
        )

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(name="reference_carrier", default_value=["heat"], element=self)

    def _set_input_carrier(self) -> Attribute:
        return Attribute(
            name="input_carrier", default_value=["electricity"], element=self
        )

    def _set_output_carrier(self) -> Attribute:
        return Attribute(name="output_carrier", default_value=["heat"], element=self)
