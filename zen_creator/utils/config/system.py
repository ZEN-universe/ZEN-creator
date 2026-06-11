import json
from pathlib import Path
from typing import Optional

from pydantic import ConfigDict

from ._base import Subscriptable


class SystemConfig(Subscriptable):
    """Config for settings in system.json."""

    model_config = ConfigDict(extra="allow")

    set_nodes: list[str] = []
    set_transport_technologies_loss_exponential: Optional[list[str]] = None
    use_existing_capacities: Optional[bool] = None
    allow_investment: Optional[bool] = None
    double_capex_transport: Optional[bool] = None
    unaggregated_time_steps_per_year: Optional[int] = None
    conduct_time_series_aggregation: Optional[bool] = None
    aggregated_time_steps_per_year: Optional[int] = None
    reference_year: Optional[int] = None
    total_hours_per_year: Optional[int] = None
    optimized_years: Optional[int] = None
    interval_between_years: Optional[int] = None
    use_rolling_horizon: Optional[bool] = None
    years_in_rolling_horizon: Optional[int] = None
    years_in_decision_horizon: Optional[int] = None
    conduct_scenario_analysis: Optional[bool] = None
    run_default_scenario: Optional[bool] = None
    clean_sub_scenarios: Optional[bool] = None
    storage_periodicity: Optional[bool] = None
    multiyear_periodicity: Optional[bool] = None
    exclude_parameters_from_TSA: Optional[bool] = None
    knowledge_depreciation_rate: Optional[float] = None
    storage_charge_discharge_binary: Optional[bool] = None

    @classmethod
    def load_from_existing_model(cls, existing_model_path: Path):
        if not isinstance(existing_model_path, (str, Path)):
            raise TypeError(
                f"Expected path of type `str` or `Path`, "
                f"got {type(existing_model_path)}"
            )

        system_path = Path(existing_model_path) / "system.json"

        if not system_path.exists():
            raise FileNotFoundError(
                f"Could not find the configuration file {system_path}."
            )

        with open(system_path, "r") as f:
            user_dict = json.load(f)

        return cls.model_validate(user_dict)
