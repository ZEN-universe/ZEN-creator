from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.datasets.dataset_collections import (
    EconomicParameters,
)
from zen_creator.elements import (
    ConversionTechnology,
)
from zen_creator.utils.attribute import Attribute


class Photovoltaics(ConversionTechnology):

    name: str = "photovoltaics"

    def __init__(self, model: Model):
        super().__init__(model=model)

    def _set_lifetime(self) -> Attribute:
        attr = self._lifetime
        lifetime = EconomicParameters(self.model.source_path).get_lifetime(self.name)
        return attr.set_data(default_value=lifetime, source="multiple sources")

    def _set_capex_specific_conversion(self) -> Attribute:
        attr = self._capex_specific_conversion
        sic = float(
            EconomicParameters(self.model.source_path)
            .get_cost_data(self.name, "capex", self.model.config)
            .loc[self.model.config.time_settings.reference_year]
        )
        return attr.set_data(default_value=sic, unit="Euro/kW", source="")

    def _set_conversion_factor(self) -> Attribute:
        return Attribute(
            name="conversion_factor", default_value=[], source="", element=self
        )

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(
            name="reference_carrier", default_value=["electricity"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        return Attribute(name="input_carrier", default_value=[], element=self)

    def _set_output_carrier(self) -> Attribute:
        return Attribute(
            name="output_carrier", default_value=["electricity"], element=self
        )
