from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.technologies.conversion_technology import (
    ConversionTechnology,
)
from zen_creator.datasets.dataset_collections.dataset_collection_technoeconomic_parameters import (
    EconomicParameters,
)

from zen_creator.utils.attribute import Attribute


class LigniteCoalPlant(ConversionTechnology):
    def __init__(self, model: Model):
        super().__init__(name="lignite_coal_plant", model=model)

    def _set_lifetime(self) -> Attribute:
        lifetime = 46
        return Attribute(
            name="lifetime",
            default_value=lifetime,
            source="https://www.nature.com/articles/s41467-019-12618-3",
            element=self,
        )

    def _set_capex_specific_conversion(self) -> Attribute:
        attr = self._capex_specific_conversion
        capex = (
            EconomicParameters(self.model.source_path)
            .get_cost_data(self.name, "capex", self.model.config)
            .loc[self.model.config.time_settings.reference_year]
        )
        return attr.set_data(
            default_value=capex, unit="Euro/kW", source="multiple sources"
        )

    def _set_conversion_factor(self) -> Attribute:
        conversion_factor = 1 / EconomicParameters(
            self.model.source_path
        ).get_efficiency(self.name)
        return Attribute(
            name="conversion_factor",
            default_value=[
                {"lignite": {"default_value": conversion_factor, "unit": "GWh/GWh"}}
            ],
            source="multiple sources",
            element=self,
        )

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(
            name="reference_carrier", default_value=["electricity"], element=self
        )

    def _set_input_carrier(self) -> Attribute:
        return Attribute(name="input_carrier", default_value=["lignite"], element=self)

    def _set_output_carrier(self) -> Attribute:
        return Attribute(
            name="output_carrier", default_value=["electricity"], element=self
        )
