"""Element class definitions for the existing_model fixture.

This module contains custom Carrier, Technology, and EnergySystem classes
that mirror the structure of the existing_model fixture. These classes are
kept in a separate module to allow lazy importing in tests, preventing
registry contamination between tests.

To use these classes in a test:
    import importlib
    importlib.import_module("tests.end_to_end.fixtures.existing_model_elements")
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from zen_creator.datasets.datasets.metadata import MetaData, SourceInformation
from zen_creator.elements import Carrier, ConversionTechnology, EnergySystem
from zen_creator.elements.storage_technologies.storage_technology import (
    StorageTechnology,
)
from zen_creator.elements.transport_technologies.transport_technology import (
    TransportTechnology,
)
from zen_creator.model import Model
from zen_creator.utils.attribute import Attribute

FIXTURE_ROOT = Path(__file__).parent
EXISTING_MODEL_PATH = FIXTURE_ROOT / "existing_model"


def _fixture_csv(relative_path: str, index_col=0):
    return pd.read_csv(EXISTING_MODEL_PATH / relative_path, index_col=index_col)


def _fixture_metadeta(from_csv: bool = False) -> MetaData:
    if from_csv:
        name = "existing_model_csv"
        title = "Existing Model CSV File"
    else:
        name = "existing_model"
        title = "Existing Model"

    return MetaData(
        name=name,
        title=title,
        author=["RRE Lab"],
        publication="ZEN Creator Test Cases",
        publication_year=2026,
        url="https://github.com/ZEN-universe/ZEN-creator",
    )


def _fixture_default_source(attr_name: str) -> list[SourceInformation]:
    return [
        SourceInformation(
            description=(
                f"Using default value for {attr_name} from the existing model fixture."
            ),
            metadata=_fixture_metadeta(),
        )
    ]


def _fixture_csv_source(attr_name: str) -> SourceInformation:
    return SourceInformation(
        description=f"Using csv file for {attr_name} from the existing model fixture.",
        metadata=_fixture_metadeta(from_csv=True),
    )


class ExistingModelEnergySystem(EnergySystem):
    """Energy system that mirrors the existing_model fixture."""

    name = "energy_system_existing_model"

    def __init__(self, model: Model):
        super().__init__(model=model)

    def _set_carbon_emissions_annual_limit(self) -> Attribute:
        return Attribute(
            name="carbon_emissions_annual_limit",
            element=self,
            default_value=np.inf,
            unit="gigatons",
            sources=_fixture_default_source("carbon_emissions_annual_limit"),
        )

    def _set_carbon_emissions_budget(self) -> Attribute:
        return Attribute(
            name="carbon_emissions_budget",
            element=self,
            default_value=4.2749370139006455,
            unit="gigatons",
            sources=_fixture_default_source("carbon_emissions_budget"),
        )

    def _set_carbon_emissions_cumulative_existing(self) -> Attribute:
        return Attribute(
            name="carbon_emissions_cumulative_existing",
            element=self,
            default_value=0.0,
            unit="gigatons",
            sources=_fixture_default_source("carbon_emissions_cumulative_existing"),
        )

    def _set_price_carbon_emissions(self) -> Attribute:
        return Attribute(
            name="price_carbon_emissions",
            element=self,
            default_value=0.0,
            unit="Euro/tons",
            sources=_fixture_default_source("price_carbon_emissions"),
        )

    def _set_price_carbon_emissions_budget_overshoot(self) -> Attribute:
        return Attribute(
            name="price_carbon_emissions_budget_overshoot",
            element=self,
            default_value=400.0,
            unit="Euro/tons",
            sources=_fixture_default_source("price_carbon_emissions_budget_overshoot"),
        )

    def _set_price_carbon_emissions_annual_overshoot(self) -> Attribute:
        return Attribute(
            name="price_carbon_emissions_annual_overshoot",
            element=self,
            default_value=np.inf,
            unit="Euro/tons",
            sources=_fixture_default_source("price_carbon_emissions_annual_overshoot"),
        )

    def _set_discount_rate(self) -> Attribute:
        return Attribute(
            name="discount_rate",
            element=self,
            default_value=0.06,
            unit="1",
            sources=_fixture_default_source("discount_rate"),
        )

    def _set_knowledge_spillover_rate(self) -> Attribute:
        return Attribute(
            name="knowledge_spillover_rate",
            element=self,
            default_value=0.025,
            unit="1",
            sources=_fixture_default_source("knowledge_spillover_rate"),
        )

    def _set_knowledge_depreciation_rate(self) -> Attribute:
        return Attribute(
            name="knowledge_depreciation_rate",
            element=self,
            default_value=0.1,
            unit="1",
            sources=_fixture_default_source("knowledge_depreciation_rate"),
        )

    def _set_market_share_unbounded(self) -> Attribute:
        return Attribute(
            name="market_share_unbounded",
            element=self,
            default_value=0.1,
            unit="1",
            sources=_fixture_default_source("market_share_unbounded"),
        )

    def _set_set_nodes(self) -> Attribute:
        return Attribute(
            name="set_nodes",
            element=self,
            default_value=None,
            sources=_fixture_default_source("set_nodes"),
        ).set_data(
            source=_fixture_csv_source("set_nodes"),
            df=_fixture_csv("energy_system/set_nodes.csv"),
        )

    def _set_set_edges(self) -> Attribute:
        return Attribute(
            name="set_edges",
            element=self,
            default_value=None,
            sources=_fixture_default_source("set_edges"),
        ).set_data(
            source=_fixture_csv_source("set_edges"),
            df=_fixture_csv("energy_system/set_edges.csv"),
        )


class ElectricityCarrier(Carrier):
    """Carrier definition for electricity in the existing_model fixture."""

    name = "electricity"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_demand(self) -> Attribute:
        return Attribute(
            name="demand",
            element=self,
            default_value=50.0,
            unit="GW",
            sources=_fixture_default_source("demand"),
        ).set_data(
            source=_fixture_csv_source("demand"),
            df=_fixture_csv("set_carriers/electricity/demand.csv"),
        )

    def _set_availability_import(self) -> Attribute:
        return Attribute(
            name="availability_import",
            element=self,
            default_value=0.0,
            unit="GW",
            sources=_fixture_default_source("availability_import"),
        )

    def _set_availability_export(self) -> Attribute:
        return Attribute(
            name="availability_export",
            element=self,
            default_value=0.0,
            unit="GW",
            sources=_fixture_default_source("availability_export"),
        )

    def _set_availability_import_yearly(self) -> Attribute:
        return Attribute(
            name="availability_import_yearly",
            element=self,
            default_value=np.inf,
            unit="GWh",
            sources=_fixture_default_source("availability_import_yearly"),
        )

    def _set_availability_export_yearly(self) -> Attribute:
        return Attribute(
            name="availability_export_yearly",
            element=self,
            default_value=np.inf,
            unit="GWh",
            sources=_fixture_default_source("availability_export_yearly"),
        )

    def _set_price_import(self) -> Attribute:
        return Attribute(
            name="price_import",
            element=self,
            default_value=30.0,
            unit="kiloEuro/GWh",
            sources=_fixture_default_source("price_import"),
        )

    def _set_price_export(self) -> Attribute:
        return Attribute(
            name="price_export",
            element=self,
            default_value=0.0,
            unit="kiloEuro/GWh",
            sources=_fixture_default_source("price_export"),
        )

    def _set_carbon_intensity_carrier_import(self) -> Attribute:
        return Attribute(
            name="carbon_intensity_carrier_import",
            element=self,
            default_value=0.127,
            unit="kilotons/GWh",
            sources=_fixture_default_source("carbon_intensity_carrier_import"),
        )

    def _set_carbon_intensity_carrier_export(self) -> Attribute:
        return Attribute(
            name="carbon_intensity_carrier_export",
            element=self,
            default_value=0.127,
            unit="kilotons/GWh",
            sources=_fixture_default_source("carbon_intensity_carrier_export"),
        )

    def _set_price_shed_demand(self) -> Attribute:
        return Attribute(
            name="price_shed_demand",
            element=self,
            default_value=1000.0,
            unit="Euro/MWh",
            sources=_fixture_default_source("price_shed_demand"),
        )

    def save_data(self):
        super().save_data()
        demand_2024 = _fixture_csv("set_carriers/electricity/demand_2024.csv")
        demand_2024.to_csv(self.output_path / "demand_2024.csv")


class HeatCarrier(Carrier):
    """Carrier definition for heat in the existing_model fixture."""

    name = "heat"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_demand(self) -> Attribute:
        return Attribute(
            name="demand",
            element=self,
            default_value=100.0,
            unit="GW",
            sources=_fixture_default_source("demand"),
        ).set_data(
            source=_fixture_csv_source("demand"),
            df=_fixture_csv("set_carriers/heat/demand.csv"),
        )

    def _set_availability_import(self) -> Attribute:
        return Attribute(
            name="availability_import",
            element=self,
            default_value=0.0,
            unit="GW",
            sources=_fixture_default_source("availability_import"),
        )

    def _set_availability_export(self) -> Attribute:
        return Attribute(
            name="availability_export",
            element=self,
            default_value=0.0,
            unit="GW",
            sources=_fixture_default_source("availability_export"),
        )

    def _set_availability_import_yearly(self) -> Attribute:
        return Attribute(
            name="availability_import_yearly",
            element=self,
            default_value=np.inf,
            unit="GWh",
            sources=_fixture_default_source("availability_import_yearly"),
        )

    def _set_availability_export_yearly(self) -> Attribute:
        return Attribute(
            name="availability_export_yearly",
            element=self,
            default_value=np.inf,
            unit="GWh",
            sources=_fixture_default_source("availability_export_yearly"),
        )

    def _set_price_import(self) -> Attribute:
        return Attribute(
            name="price_import",
            element=self,
            default_value=0.0,
            unit="kiloEuro/GWh",
            sources=_fixture_default_source("price_import"),
        )

    def _set_price_export(self) -> Attribute:
        return Attribute(
            name="price_export",
            element=self,
            default_value=0.0,
            unit="kiloEuro/GWh",
            sources=_fixture_default_source("price_export"),
        )

    def _set_carbon_intensity_carrier_import(self) -> Attribute:
        return Attribute(
            name="carbon_intensity_carrier_import",
            element=self,
            default_value=0.0,
            unit="kilotons/GWh",
            sources=_fixture_default_source("carbon_intensity_carrier_import"),
        )

    def _set_carbon_intensity_carrier_export(self) -> Attribute:
        return Attribute(
            name="carbon_intensity_carrier_export",
            element=self,
            default_value=0.0,
            unit="kilotons/GWh",
            sources=_fixture_default_source("carbon_intensity_carrier_export"),
        )

    def _set_price_shed_demand(self) -> Attribute:
        return Attribute(
            name="price_shed_demand",
            element=self,
            default_value=np.inf,
            unit="kiloEuro/GWh",
            sources=_fixture_default_source("price_shed_demand"),
        )


class NaturalGasCarrier(Carrier):
    """Carrier definition for natural gas in the existing_model fixture."""

    name = "natural_gas"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_demand(self) -> Attribute:
        return Attribute(
            name="demand",
            element=self,
            default_value=0.0,
            unit="GW",
            sources=_fixture_default_source("demand"),
        )

    def _set_availability_import(self) -> Attribute:
        return Attribute(
            name="availability_import",
            element=self,
            default_value=np.inf,
            unit="GW",
            sources=_fixture_default_source("availability_import"),
        ).set_data(
            source=_fixture_csv_source("availability_import"),
            df=_fixture_csv("set_carriers/natural_gas/availability_import.csv"),
        )

    def _set_availability_export(self) -> Attribute:
        return Attribute(
            name="availability_export",
            element=self,
            default_value=0.0,
            unit="GW",
            sources=_fixture_default_source("availability_export"),
        )

    def _set_availability_import_yearly(self) -> Attribute:
        return Attribute(
            name="availability_import_yearly",
            element=self,
            default_value=np.inf,
            unit="GWh",
            sources=_fixture_default_source("availability_import_yearly"),
        )

    def _set_availability_export_yearly(self) -> Attribute:
        return Attribute(
            name="availability_export_yearly",
            element=self,
            default_value=np.inf,
            unit="GWh",
            sources=_fixture_default_source("availability_export_yearly"),
        )

    def _set_price_import(self) -> Attribute:
        return Attribute(
            name="price_import",
            element=self,
            default_value=23.0,
            unit="kiloEuro/GWh",
            sources=_fixture_default_source("price_import"),
        )

    def _set_price_export(self) -> Attribute:
        return Attribute(
            name="price_export",
            element=self,
            default_value=0.0,
            unit="kiloEuro/GWh",
            sources=_fixture_default_source("price_export"),
        )

    def _set_carbon_intensity_carrier_import(self) -> Attribute:
        return Attribute(
            name="carbon_intensity_carrier_import",
            element=self,
            default_value=0.2,
            unit="kilotons/GWh",
            sources=_fixture_default_source("carbon_intensity_carrier_import"),
        )

    def _set_carbon_intensity_carrier_export(self) -> Attribute:
        return Attribute(
            name="carbon_intensity_carrier_export",
            element=self,
            default_value=0.2,
            unit="kilotons/GWh",
            sources=_fixture_default_source("carbon_intensity_carrier_export"),
        )

    def _set_price_shed_demand(self) -> Attribute:
        return Attribute(
            name="price_shed_demand",
            element=self,
            default_value=np.inf,
            unit="kiloEuro/GWh",
            sources=_fixture_default_source("price_shed_demand"),
        )


class NaturalGasBoiler(ConversionTechnology):
    """Conversion technology for the existing_model fixture."""

    name = "natural_gas_boiler"

    def __init__(self, model: Model, power_unit: str = "GW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(
            name="reference_carrier",
            element=self,
            default_value=["heat"],
            sources=_fixture_default_source("reference_carrier"),
        )

    def _set_input_carrier(self) -> Attribute:
        return Attribute(
            name="input_carrier",
            element=self,
            default_value=["natural_gas"],
            sources=_fixture_default_source("input_carrier"),
        )

    def _set_output_carrier(self) -> Attribute:
        return Attribute(
            name="output_carrier",
            element=self,
            default_value=["heat"],
            sources=_fixture_default_source("output_carrier"),
        )

    def _set_lifetime(self) -> Attribute:
        return Attribute(
            name="lifetime",
            element=self,
            default_value=24.0,
            unit="1",
            sources=_fixture_default_source("lifetime"),
        )

    def _set_conversion_factor(self) -> Attribute:
        return Attribute(
            name="conversion_factor",
            element=self,
            default_value=[{"natural_gas": {"default_value": 1.1, "unit": "GWh/GWh"}}],
            sources=_fixture_default_source("conversion_factor"),
        )

    def _set_max_load(self) -> Attribute:
        return Attribute(
            name="max_load",
            element=self,
            default_value=1.0,
            unit="1",
            sources=_fixture_default_source("max_load"),
        )

    def _set_opex_specific_variable(self) -> Attribute:
        return Attribute(
            name="opex_specific_variable",
            element=self,
            default_value=0.0,
            unit="kiloEuro/GWh",
            sources=_fixture_default_source("opex_specific_variable"),
        )

    def _set_opex_specific_fixed(self) -> Attribute:
        return Attribute(
            name="opex_specific_fixed",
            element=self,
            default_value=87.6,
            unit="Euro/kW",
            sources=_fixture_default_source("opex_specific_fixed"),
        )

    def _set_capex_specific_conversion(self) -> Attribute:
        return Attribute(
            name="capex_specific_conversion",
            element=self,
            default_value=876.0,
            unit="Euro/kW",
            sources=_fixture_default_source("capex_specific_conversion"),
        )


class Photovoltaics(ConversionTechnology):
    """Conversion technology for the existing_model fixture."""

    name = "photovoltaics"

    def __init__(self, model: Model, power_unit: str = "GW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(
            name="reference_carrier",
            element=self,
            default_value=["electricity"],
            sources=_fixture_default_source("reference_carrier"),
        )

    def _set_input_carrier(self) -> Attribute:
        return Attribute(
            name="input_carrier",
            element=self,
            default_value=[],
            sources=_fixture_default_source("input_carrier"),
        )

    def _set_output_carrier(self) -> Attribute:
        return Attribute(
            name="output_carrier",
            element=self,
            default_value=["electricity"],
            sources=_fixture_default_source("output_carrier"),
        )

    def _set_lifetime(self) -> Attribute:
        return Attribute(
            name="lifetime",
            element=self,
            default_value=24.0,
            unit="1",
            sources=_fixture_default_source("lifetime"),
        )

    def _set_conversion_factor(self) -> Attribute:
        return Attribute(
            name="conversion_factor",
            element=self,
            default_value=[{"": {"default_value": 1.1, "unit": "GWh/GWh"}}],
            sources=_fixture_default_source("conversion_factor"),
        )

    def _set_max_load(self) -> Attribute:
        return Attribute(
            name="max_load",
            element=self,
            default_value=1.0,
            unit="1",
            sources=_fixture_default_source("max_load"),
        )

    def _set_opex_specific_variable(self) -> Attribute:
        return Attribute(
            name="opex_specific_variable",
            element=self,
            default_value=1.0,
            unit="kiloEuro/GWh",
            sources=_fixture_default_source("opex_specific_variable"),
        )

    def _set_opex_specific_fixed(self) -> Attribute:
        return Attribute(
            name="opex_specific_fixed",
            element=self,
            default_value=0.07,
            unit="Euro/MW",
            sources=_fixture_default_source("opex_specific_fixed"),
        )

    def _set_capex_specific_conversion(self) -> Attribute:
        return Attribute(
            name="capex_specific_conversion",
            element=self,
            default_value=751.0,
            unit="Euro/kW",
            sources=_fixture_default_source("capex_specific_conversion"),
        )


class NaturalGasStorage(StorageTechnology):
    """Storage technology for the existing_model fixture."""

    name = "natural_gas_storage"

    def __init__(self, model: Model, power_unit: str = "GW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(
            name="reference_carrier",
            element=self,
            default_value=["natural_gas"],
            sources=_fixture_default_source("reference_carrier"),
        )

    def _set_lifetime(self) -> Attribute:
        return Attribute(
            name="lifetime",
            element=self,
            default_value=100.0,
            unit="1",
            sources=_fixture_default_source("lifetime"),
        )

    def _set_max_load(self) -> Attribute:
        return Attribute(
            name="max_load",
            element=self,
            default_value=1.0,
            unit="1",
            sources=_fixture_default_source("max_load"),
        )

    def _set_opex_specific_variable(self) -> Attribute:
        return Attribute(
            name="opex_specific_variable",
            element=self,
            default_value=0.0,
            unit="kiloEuro/GWh",
            sources=_fixture_default_source("opex_specific_variable"),
        )

    def _set_opex_specific_fixed(self) -> Attribute:
        return Attribute(
            name="opex_specific_fixed",
            element=self,
            default_value=135.74,
            unit="kiloEuro/GW",
            sources=_fixture_default_source("opex_specific_fixed"),
        )

    def _set_carbon_intensity_technology(self) -> Attribute:
        return Attribute(
            name="carbon_intensity_technology",
            element=self,
            default_value=0.0,
            unit="kilotons/GWh",
            sources=_fixture_default_source("carbon_intensity_technology"),
        )

    def _set_efficiency_charge(self) -> Attribute:
        return Attribute(
            name="efficiency_charge",
            element=self,
            default_value=0.9746794344808963,
            unit="1",
            sources=_fixture_default_source("efficiency_charge"),
        )

    def _set_efficiency_discharge(self) -> Attribute:
        return Attribute(
            name="efficiency_discharge",
            element=self,
            default_value=0.9746794344808963,
            unit="1",
            sources=_fixture_default_source("efficiency_discharge"),
        )

    def _set_self_discharge(self) -> Attribute:
        return Attribute(
            name="self_discharge",
            element=self,
            default_value=0.0,
            unit="1",
            sources=_fixture_default_source("self_discharge"),
        )

    def _set_capex_specific_storage(self) -> Attribute:
        return Attribute(
            name="capex_specific_storage",
            element=self,
            default_value=238.68,
            unit="Euro/kW",
            sources=_fixture_default_source("capex_specific_storage"),
        )

    def _set_capex_specific_storage_energy(self) -> Attribute:
        return Attribute(
            name="capex_specific_storage_energy",
            element=self,
            default_value=3.43,
            unit="Euro/kWh",
            sources=_fixture_default_source("capex_specific_storage_energy"),
        )

    def _set_capacity_addition_min_energy(self) -> Attribute:
        return Attribute(
            name="capacity_addition_min_energy",
            element=self,
            default_value=0.0,
            unit="GWh",
            sources=_fixture_default_source("capacity_addition_min_energy"),
        )

    def _set_capacity_addition_max_energy(self) -> Attribute:
        return Attribute(
            name="capacity_addition_max_energy",
            element=self,
            default_value=np.inf,
            unit="GWh",
            sources=_fixture_default_source("capacity_addition_max_energy"),
        )

    def _set_capacity_existing_energy(self) -> Attribute:
        return Attribute(
            name="capacity_existing_energy",
            element=self,
            default_value=0.0,
            unit="GWh",
            sources=_fixture_default_source("capacity_existing_energy"),
        )

    def _set_capacity_limit_energy(self) -> Attribute:
        return Attribute(
            name="capacity_limit_energy",
            element=self,
            default_value=np.inf,
            unit="GWh",
            sources=_fixture_default_source("capacity_limit_energy"),
        )

    def _set_min_load_energy(self) -> Attribute:
        return Attribute(
            name="min_load_energy",
            element=self,
            default_value=0.0,
            unit="1",
            sources=_fixture_default_source("min_load_energy"),
        )

    def _set_max_load_energy(self) -> Attribute:
        return Attribute(
            name="max_load_energy",
            element=self,
            default_value=1.0,
            unit="1",
            sources=_fixture_default_source("max_load_energy"),
        )

    def _set_capacity_investment_existing_energy(self) -> Attribute:
        return Attribute(
            name="capacity_investment_existing_energy",
            element=self,
            default_value=0.0,
            unit="GWh",
            sources=_fixture_default_source("capacity_investment_existing_energy"),
        )

    def _set_opex_specific_fixed_energy(self) -> Attribute:
        return Attribute(
            name="opex_specific_fixed_energy",
            element=self,
            default_value=55.54,
            unit="Euro/MWh",
            sources=_fixture_default_source("opex_specific_fixed_energy"),
        )

    def _set_energy_to_power_ratio_min(self) -> Attribute:
        return Attribute(
            name="energy_to_power_ratio_min",
            element=self,
            default_value=700.0,
            unit="h",
            sources=_fixture_default_source("energy_to_power_ratio_min"),
        )

    def _set_energy_to_power_ratio_max(self) -> Attribute:
        return Attribute(
            name="energy_to_power_ratio_max",
            element=self,
            default_value=700.0,
            unit="h",
            sources=_fixture_default_source("energy_to_power_ratio_max"),
        )

    def _set_flow_storage_inflow(self) -> Attribute:
        return Attribute(
            name="flow_storage_inflow",
            element=self,
            default_value=0.0,
            unit="GW",
            sources=_fixture_default_source("flow_storage_inflow"),
        )


class PumpedHydro(StorageTechnology):
    """Storage technology for the existing_model fixture."""

    name = "pumped_hydro"

    def __init__(self, model: Model, power_unit: str = "GW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(
            name="reference_carrier",
            element=self,
            default_value=["electricity"],
            sources=_fixture_default_source("reference_carrier"),
        )

    def _set_lifetime(self) -> Attribute:
        return Attribute(
            name="lifetime",
            element=self,
            default_value=55.0,
            unit="1",
            sources=_fixture_default_source("lifetime"),
        )

    def _set_max_load(self) -> Attribute:
        return Attribute(
            name="max_load",
            element=self,
            default_value=1.0,
            unit="1",
            sources=_fixture_default_source("max_load"),
        )

    def _set_opex_specific_variable(self) -> Attribute:
        return Attribute(
            name="opex_specific_variable",
            element=self,
            default_value=10.0,
            unit="Euro/MWh",
            sources=_fixture_default_source("opex_specific_variable"),
        )

    def _set_opex_specific_fixed(self) -> Attribute:
        return Attribute(
            name="opex_specific_fixed",
            element=self,
            default_value=7.5883468159272995,
            unit="Euro/kW",
            sources=_fixture_default_source("opex_specific_fixed"),
        ).set_data(
            source=_fixture_csv_source("opex_specific_fixed"),
            df=_fixture_csv(
                "set_technologies/set_storage_technologies/pumped_hydro/opex_specific_fixed.csv"
            ),
        )

    def _set_carbon_intensity_technology(self) -> Attribute:
        return Attribute(
            name="carbon_intensity_technology",
            element=self,
            default_value=0.0,
            unit="kilotons/GWh",
            sources=_fixture_default_source("carbon_intensity_technology"),
        )

    def _set_efficiency_charge(self) -> Attribute:
        return Attribute(
            name="efficiency_charge",
            element=self,
            default_value=0.8831760866327847,
            unit="1",
            sources=_fixture_default_source("efficiency_charge"),
        )

    def _set_efficiency_discharge(self) -> Attribute:
        return Attribute(
            name="efficiency_discharge",
            element=self,
            default_value=0.8831760866327847,
            unit="1",
            sources=_fixture_default_source("efficiency_discharge"),
        )

    def _set_self_discharge(self) -> Attribute:
        return Attribute(
            name="self_discharge",
            element=self,
            default_value=0.1,
            unit="1",
            sources=_fixture_default_source("self_discharge"),
        )

    def _set_capex_specific_storage(self) -> Attribute:
        return Attribute(
            name="capex_specific_storage",
            element=self,
            default_value=1070.9054443977402,
            unit="Euro/kW",
            sources=_fixture_default_source("capex_specific_storage"),
        )

    def _set_capex_specific_storage_energy(self) -> Attribute:
        return Attribute(
            name="capex_specific_storage_energy",
            element=self,
            default_value=75.883468159273,
            unit="Euro/kWh",
            sources=_fixture_default_source("capex_specific_storage_energy"),
        )

    def _set_capacity_addition_min_energy(self) -> Attribute:
        return Attribute(
            name="capacity_addition_min_energy",
            element=self,
            default_value=0.0,
            unit="GWh",
            sources=_fixture_default_source("capacity_addition_min_energy"),
        )

    def _set_capacity_addition_max_energy(self) -> Attribute:
        return Attribute(
            name="capacity_addition_max_energy",
            element=self,
            default_value=np.inf,
            unit="GWh",
            sources=_fixture_default_source("capacity_addition_max_energy"),
        )

    def _set_capacity_existing_energy(self) -> Attribute:
        return Attribute(
            name="capacity_existing_energy",
            element=self,
            default_value=0.0,
            unit="GWh",
            sources=_fixture_default_source("capacity_existing_energy"),
        ).set_data(
            source=_fixture_csv_source("capacity_existing_energy"),
            df=_fixture_csv(
                "set_technologies/set_storage_technologies/pumped_hydro/capacity_existing_energy.csv",
                index_col=[0, 1],
            ),
        )

    def _set_capacity_existing(self) -> Attribute:
        return Attribute(
            name="capacity_existing",
            element=self,
            default_value=0.0,
            unit="GW",
            sources=_fixture_default_source("capacity_existing"),
        ).set_data(
            source=_fixture_csv_source("capacity_existing"),
            df=_fixture_csv(
                "set_technologies/set_storage_technologies/pumped_hydro/capacity_existing.csv",
                index_col=[0, 1],
            ),
        )

    def _set_capacity_limit_energy(self) -> Attribute:
        return Attribute(
            name="capacity_limit_energy",
            element=self,
            default_value=0.0,
            unit="GWh",
            sources=_fixture_default_source("capacity_limit_energy"),
        )

    def _set_capacity_limit(self) -> Attribute:
        return Attribute(
            name="capacity_limit",
            element=self,
            default_value=0.0,
            unit="GW",
            sources=_fixture_default_source("capacity_limit"),
        )

    def _set_min_load_energy(self) -> Attribute:
        return Attribute(
            name="min_load_energy",
            element=self,
            default_value=0.0,
            unit="1",
            sources=_fixture_default_source("min_load_energy"),
        )

    def _set_max_load_energy(self) -> Attribute:
        return Attribute(
            name="max_load_energy",
            element=self,
            default_value=1.0,
            unit="1",
            sources=_fixture_default_source("max_load_energy"),
        )

    def _set_capacity_investment_existing_energy(self) -> Attribute:
        return Attribute(
            name="capacity_investment_existing_energy",
            element=self,
            default_value=0.0,
            unit="GWh",
            sources=_fixture_default_source("capacity_investment_existing_energy"),
        )

    def _set_opex_specific_fixed_energy(self) -> Attribute:
        return Attribute(
            name="opex_specific_fixed_energy",
            element=self,
            default_value=1.0,
            unit="Euro/MWh",
            sources=_fixture_default_source("opex_specific_fixed_energy"),
        )

    def _set_flow_storage_inflow(self) -> Attribute:
        return Attribute(
            name="flow_storage_inflow",
            element=self,
            default_value=0.0,
            unit="GW",
            sources=_fixture_default_source("flow_storage_inflow"),
        ).set_data(
            source=_fixture_csv_source("flow_storage_inflow"),
            df=_fixture_csv(
                "set_technologies/set_storage_technologies/pumped_hydro/flow_storage_inflow.csv"
            ),
        )


class NaturalGasPipeline(TransportTechnology):
    """Transport technology for the existing_model fixture."""

    name = "natural_gas_pipeline"

    def __init__(self, model: Model, power_unit: str = "GW"):
        super().__init__(model=model, power_unit=power_unit)

    def _set_reference_carrier(self) -> Attribute:
        return Attribute(
            name="reference_carrier",
            element=self,
            default_value=["natural_gas"],
            sources=_fixture_default_source("reference_carrier"),
        )

    def _set_lifetime(self) -> Attribute:
        return Attribute(
            name="lifetime",
            element=self,
            default_value=50.0,
            unit="1",
            sources=_fixture_default_source("lifetime"),
        )

    def _set_max_load(self) -> Attribute:
        return Attribute(
            name="max_load",
            element=self,
            default_value=1.0,
            unit="1",
            sources=_fixture_default_source("max_load"),
        )

    def _set_opex_specific_variable(self) -> Attribute:
        return Attribute(
            name="opex_specific_variable",
            element=self,
            default_value=0.0,
            unit="kiloEuro/GWh",
            sources=_fixture_default_source("opex_specific_variable"),
        )

    def _set_opex_specific_fixed(self) -> Attribute:
        return Attribute(
            name="opex_specific_fixed",
            element=self,
            default_value=0.0,
            unit="Euro/MW",
            sources=_fixture_default_source("opex_specific_fixed"),
        )

    def _set_carbon_intensity_technology(self) -> Attribute:
        return Attribute(
            name="carbon_intensity_technology",
            element=self,
            default_value=0.0,
            unit="kilotons/GWh/km",
            sources=_fixture_default_source("carbon_intensity_technology"),
        )

    def _set_transport_loss_factor_linear(self) -> Attribute:
        return Attribute(
            name="transport_loss_factor_linear",
            element=self,
            default_value=5e-05,
            unit="1/km",
            sources=_fixture_default_source("transport_loss_factor_linear"),
        )

    def _set_capex_per_distance_transport(self) -> Attribute:
        return Attribute(
            name="capex_per_distance_transport",
            element=self,
            default_value=265.0,
            unit="Euro/km/MW",
            sources=_fixture_default_source("capex_per_distance_transport"),
        )

    def _set_distance(self) -> Attribute:
        return Attribute(
            name="distance",
            element=self,
            default_value=np.inf,
            unit="km",
            sources=_fixture_default_source("distance"),
        )
