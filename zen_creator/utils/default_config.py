from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field


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

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

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


class SectorConfig(Subscriptable):
    """
    Config for sector settings.
    """

    include: list[str] = Field(default_factory=list)  # list of sectors to include
    exclude: list[str] = Field(default_factory=list)  # list of sectors to exclude


class ElementConfig(Subscriptable):
    """
    Config for element settings.
    """

    include: list[str] = Field(default_factory=list)  # list of elements to include
    exclude: list[str] = Field(default_factory=list)  # list of elements to exclude


class SystemConfig(Subscriptable):
    """
    Config for settings in system.json.
    """

    nodes: list[str]
    set_transport_tehnologies_loss_exponential: list[str] = Field(default_factory=list)
    use_existing_capacities: bool = False
    allow_investment: bool = True
    double_capex_transport: bool = False
    unaggregated_time_steps_per_year: int = 8760
    conduct_time_series_aggregation: bool = False
    aggregated_time_steps_per_year: int = 10
    reference_year: int = 2024
    total_hours_per_year: int = 8760
    optimized_years: int = 1
    interval_between_years: int = 1
    use_rolling_horizon: bool = False
    years_in_rolling_horizon: int = 1
    years_in_decision_horizon: int = 1
    conduct_scenario_analysis: bool = False
    run_default_scenario: bool = True
    clean_sub_scenarios: bool = False
    storage_periodicity: bool = True
    multiyear_periodicity: bool = False
    exclude_parameters_from_TSA: bool = True
    knowledge_depreciation_rate: float = 0.1
    storage_charge_discharge_binary: bool = False


class ENSOEAPIConfig(Subscriptable):
    api_key: str


class DatasetConfig(Subscriptable):
    ensoe_api: ENSOEAPIConfig = Field(default_factory=ENSOEAPIConfig)


class DatasetCollectionConfig(Subscriptable):
    setting: bool = True


class DataConfig(Subscriptable):
    """
    Config for data and datasets.
    """

    datasets: DatasetConfig = Field(default_factory=DatasetConfig)
    dataset_collections: DatasetCollectionConfig = Field(
        default_factory=DatasetCollectionConfig
    )


class Config(Subscriptable):
    """
    Default configuration for ZEN-creator.
    """

    name: str
    source_path: str
    output_folder: str = "./models/"
    sectors: SectorConfig = Field(default_factor=SectorConfig)
    elements: ElementConfig = Field(default_factory=ElementConfig)
    system: SystemConfig = Field(default_factor=SystemConfig)
    data: DataConfig = Field(default_factory=DataConfig)


def load_config(path: str | Path) -> Config:

    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(f"Could not find the configuration file {config_path}.")

    with open(config_path, "r") as f:
        user_dict = yaml.safe_load(f) or {}

    return Config.model_validate(user_dict)
