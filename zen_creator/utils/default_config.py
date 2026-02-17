from pydantic import BaseModel,ConfigDict
from typing import Any, Optional, Union, Literal
import copy
import yaml
import os

class Subscriptable(BaseModel):
    """
    Allows dictionary-like access to class attributes.

    This class allows dictionary-like access to class attributes, such as
    ``obj["key"]`` instead of ``obj.key``. Similarly, attribute values can
    be changed in a dictionary like fashion ``obj["key"] = new_value``. Lastly,
    attribute names and values can be called using the methods ``.keys()``,
    ``.values()``, and ``.items()`` like in a normal dictionary. 

    Inherits from:
        :class:`BaseModel` - Class from the Pydantic package which provides
        advanced features in input data handling and validation. 

    """

    model_config = ConfigDict(extra="allow")

    def __getitem__(self, __name: str) -> Any:
        return getattr(self, __name)

    def __setitem__(self, __name: str, __value: Any) -> None:
        setattr(self, __name, __value)

    def keys(self) -> Any:
        return self.model_dump().keys()

    def items(self) -> Any:
        return self.model_dump().items()

    def values(self) -> Any:
        return self.model_dump().values()
    

class MainSettings(Subscriptable):
    """
    Main settings for ZEN-creator.
    """
    source_path: str | None = None
    output_folder: str = "./outputs/"
    use_no_storage: bool = False # TODO remove?
    use_self_discharge: bool = False # TODO remove?


class TimeSettings(Subscriptable):
    """
    Time settings for ZEN-creator.
    """
    reference_year: int = 2022
    final_year: int = 2050
    data_general_year: int = 2021
    data_timeseries_year: int = 2019
    reference_year_default: int = copy.copy(reference_year) # TODO remove?
    interval_between_years: int = 2
    unaggregated_time_steps_per_year: int = 8760
    aggregated_time_steps_per_year: int = 100
    conduct_time_series_aggregation: bool = True
    use_rolling_horizon: bool = False
    years_in_rolling_horizon: int = 2
    years_in_decision_horizon: int = 1
    optimized_years: int = int((final_year - reference_year) / interval_between_years + 1)
    opti_years: list = list(range(reference_year, final_year + 1))

class InvestmentSettings(Subscriptable):
    """
    Investment settings for ZEN-creator.
    """
    use_existing_capacities: bool = True 
    use_existing_oil_to_x_capacities: bool = False  # if True, existing oil to x capacities are used, if False, they are not used # TODO remove?
    keep_existing_capacities: list = [] # technologies where existing capacities should be kept, even if self.use_existing_capacities is False
    use_diffusion_rates: bool = False
    use_varying_diffusion_rates: bool = False
    use_inf_spillover_rate: bool = True
    use_unbounded_market_share: bool = True
    use_unbounded_capacity_addition_carbon: bool = True
    use_construction_times: bool = False
    allow_investment: bool = True
    use_nuclear_capacity_limit: bool = True
    use_power_line_capacity_limit: bool = True
    use_chemical_pipelines: bool = True
    account_for_offshore_transport: bool = False
    use_retrofit: bool = False
    use_battery_existing_capacity: bool = True
    force_ice_phase_out: bool = False
    knowledge_depreciation_rate: float = 0.1 # TODO move to energy system default parameters
    use_battery_e2p_ratio: bool = False
    use_renewables_tag: bool = False # TODO remove?
    use_coal_capacity_phaseout: bool = False
    use_coal_production_phaseout: bool = False

class CostSettings(Subscriptable):
    """
    Cost settings for ZEN-creator.
    """
    use_cost_comparison: bool = True
    use_learning_curves: bool = True
    min_max_mean_costs: str = "mean"
    use_seasonal_fuel_prices: bool = False
    use_nodal_gas_prices: bool = False
    use_nodal_biomass_prices: bool = False
    take_mean_carrier_prices: bool = True
    use_expensive_DAC: bool = False
    use_cheaper_demand_shedding: bool = False
    assume_oil_price_for_diesel_and_gasoline: bool = False

class EmissionSettings(Subscriptable):
    """
    Emission settings for ZEN-creator.
    """
    use_carbon_budget: bool = True
    use_carbon_annual_limit: bool = True
    use_intermediate_emission_goal: bool = True
    use_annual_limit_overshoot: bool = True
    use_EU_ETS_cap: bool = False
    use_detailed_carbon_intensity: bool = True
    use_upstream_carbon_emissions: bool = False
    use_only_CO2: bool = True # if false, all ghg emissions are considered, if true, only CO2
    use_only_public_electricity_and_heat: bool = True
    use_precovid_aviation_shipping_emissions: bool = False
    allow_hard_coal_export_emission_credit: bool = False # if true, hard coal export is considered as emission credit --> biochar
    temperature_increase: float = 1.5
    probability_carbon_budget: float = 0.5
    calculate_budget_from_ETS: bool = False
    use_EU_ETS_cap_ETS1only: bool = False
    use_adjusted_ETS_to_keep_carbon_budget: bool = True
    use_min_budget: bool = False # TODO clarify

class DataSourceSettings(Subscriptable):
    """
    Data source settings for ZEN-creator.
    """
    use_old_api_data: bool = False # TODO remove?
    use_bnef_capacities: bool = True  # overwrites the next
    use_opsd: bool = True
    use_full_scigrid_dataset: bool = False
    use_eurostat_heat: bool = True
    use_industrial_gas_demand: bool = False
    use_CATF_carbon_storage: bool = False # instead of ICP
    use_OG_carbon_storage: bool = False # use oil and gas extraction data for carbon storage
    use_IOGP_new_values: bool = True
    use_CATF_dataset_foresight_error: bool = False
    use_inf_foresight_error_carbon_storage: bool = True
    use_antonini_tavoni_cf: bool = False # use capacity factors of Antonini, Di Bella and Tavoni https://www.nature.com/articles/s41597-024-04129-8
    use_monthly_entsoe_ntc: bool = True
    potential_capacity_power_line: str = "candidates" # options: "tyndp", "candidates", "both"
    entsoe_api_key: str = None  

class AvailabilitySettings(Subscriptable):
    """
    Availability settings for ZEN-creator.
    """
    cap_waste_import: bool = False
    cap_coal_oil_import: bool = False
    annual_cap_coal_oil_import: bool = False
    annual_cap_biomass_import: bool = False
    use_biomass_projections: bool = True
    allow_heat_demand_shedding: bool = False
    allow_all_demand_shedding: bool = False

class MaxLoadSettings(Subscriptable):
    """
    Max load settings for ZEN-creator.
    """
    use_fuel_substitution: bool = False  # for all heating, True: all heating can be substituted, False: individual heating cannot be substituted, DH see below
    use_district_heating_fuel_substitution: str = "mixed"  # options "full","mixed","none"; before: mixed
    ramp_up_lng: bool = True # TODO remove?
    use_seasonal_nuclear_max_load: bool = True
    use_nodal_nuclear_max_load: bool = True

class SensitivitySettings(Subscriptable):
    """
    Sensitivity settings for ZEN-creator.
    """
    only_relaxing_sensitivity: bool = False # only those sensitivity values that relax the problem (e.g., lowering the demand but not increasing it)
    use_sensitivity_fuel_costs: bool = False
    use_sensitivity_spillover: bool = False
    use_sensitivity_carbon: bool = False
    use_sensitivity_technology_expansion: bool = False
    use_sensitivity_hydro: bool = False
    use_sensitivity_carbon_overshoot_cost: bool = False
    use_sensitivity_discount_rate: bool = False
    use_sensitivity_demand: bool = False
    use_sensitivity_all_budgets: bool = False
    use_sensitivity_ts: bool = False
    use_sensitivity_biomass: bool = False
    use_sensitivity_ter: bool = False
    technologies_ter_scenario: list = []

    @property
    def conduct_scenario_analysis(self) -> bool:
        """Returns True if any sensitivity toggle is enabled."""
        return any(
            value for key, value in self.__dict__.items() 
            if key.startswith("use_sensitivity_") and value is True
        )

class SectorSettings(Subscriptable):
    """
    Sector settings for ZEN-creator.
    """
    sectors: list = ["electricity",
               "heat",
               "carbon",
               "passenger_transport",
               "truck_transport",
               "hydrogen",
               "refining",
               "methanol",
               "ammonia",
               "cement",
               "aviation",
               "shipping",
               "steel"]
    include_aggregated_transport_sector: bool = True # TODO move somewhere else?

    use_district_heating: bool = True

class Config(Subscriptable):
    """
    Default configuration for ZEN-creator.
    """
    main_settings: MainSettings = MainSettings()
    investment_settings: InvestmentSettings = InvestmentSettings()
    cost_settings: CostSettings = CostSettings()
    emission_settings: EmissionSettings = EmissionSettings()
    data_source_settings: DataSourceSettings = DataSourceSettings()
    availability_settings: AvailabilitySettings = AvailabilitySettings()
    max_load_settings: MaxLoadSettings = MaxLoadSettings()
    sensitivity_settings: SensitivitySettings = SensitivitySettings()
    sector_settings: SectorSettings = SectorSettings()
    time_settings: TimeSettings = TimeSettings()

    def update_from_config(self, config: dict[str, Any]) -> None:
        """
        Updates config values searching through all sub-settings.
        """
        for key, value in config.items():
            found = False
            
            # Iterate over all fields in Config (e.g., main_settings, time_settings)
            for section_name in Config.model_fields:
                section = getattr(self, section_name)
                
                # Check if this section is a Pydantic model and contains the key
                if isinstance(section, BaseModel) and key in section.__class__.model_fields:
                    # Validate and set the new value (Pydantic handles type conversion)
                    setattr(section, key, value)
                    found = True
                    break # Stop looking once found
            
            if not found:
                print(f"Warning: Config key '{key}' not found in any settings category. It was ignored.")


def load_config(file_path: str) -> dict[str, Config]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file not found: {file_path}")

    with open(file_path, 'r') as f:
        all_data = yaml.safe_load(f)

    models = {}
    for model_name in all_data.keys():
        if model_name == "global":
            continue
        config_model = Config()
        global_overrides = all_data.get("global")
        if global_overrides:
            config_model.update_from_config(global_overrides)
        overrides = all_data[model_name]
        config_model.update_from_config(overrides)
        models[model_name] = config_model
    return models
