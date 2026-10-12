"""Mirror of ZEN-garden's system file.

The fields and defaults mirror ``zen_garden.config``. ZEN-creator does not
depend on ZEN-garden, so the mirror is kept in sync by
``tests/unit/test_zen_garden_schema.py``, which compares the field sets
whenever ZEN-garden is importable.
"""

import json
from pathlib import Path
from typing import Any

import yaml
from pydantic import Field

from ._base import Subscriptable

# accepted names of a model's system file, in the order they are looked for.
# ZEN-garden deprecated the json format in favor of yaml.
SYSTEM_FILE_NAMES = ("system.yaml", "system.yml", "system.json")

# system fields that ZEN-creator derives from the elements of the model, so
# they are written by Model.write_system_file rather than configured
ELEMENT_DERIVED_FIELDS = (
    "set_carriers",
    "set_technologies",
    "set_conversion_technologies",
    "set_storage_technologies",
    "set_transport_technologies",
    "set_retrofitting_technologies",
)


def find_system_file(existing_model_path: str | Path) -> Path:
    """Return the system file of a model, preferring yaml over json.

    Raises:
        FileNotFoundError: If the model has no system file.
    """
    model_path = Path(existing_model_path)
    for name in SYSTEM_FILE_NAMES:
        system_path = model_path / name
        if system_path.exists():
            return system_path

    raise FileNotFoundError(
        f"Could not find a system file in {model_path}. Expected one of: "
        f"{', '.join(SYSTEM_FILE_NAMES)}."
    )


def read_system_file(system_path: Path) -> dict[str, Any]:
    """Read a system file in either yaml or json format."""
    with open(system_path, "r", encoding="utf-8") as f:
        if system_path.suffix.lower() in {".yaml", ".yml"}:
            return yaml.safe_load(f) or {}
        return json.load(f)


class SystemConfig(Subscriptable):
    """Config for the settings of ZEN-garden's system file."""

    set_carriers: list[str] = Field(default_factory=list)
    set_capacity_types: list[str] = Field(default_factory=lambda: ["power", "energy"])
    set_technologies: list[str] = Field(default_factory=list)
    set_conversion_technologies: list[str] = Field(default_factory=list)
    set_storage_technologies: list[str] = Field(default_factory=list)
    set_retrofitting_technologies: list[str] = Field(default_factory=list)
    storage_periodicity: bool = True
    multiyear_periodicity: bool = False
    set_transport_technologies: list[str] = Field(default_factory=list)
    set_transport_technologies_loss_exponential: list[str] = Field(default_factory=list)
    double_capex_transport: bool = False
    set_nodes: list[str] = Field(default_factory=list)
    coords: dict[str, dict[str, float]] = Field(default_factory=dict)
    exclude_parameters_from_TSA: bool = True
    conduct_scenario_analysis: bool = False
    run_default_scenario: bool = True
    clean_sub_scenarios: bool = False
    total_hours_per_year: int = 8760
    knowledge_depreciation_rate: float = 0.1
    reference_year: int = 2024
    unaggregated_time_steps_per_year: int = 8760
    aggregated_time_steps_per_year: int = 8760
    conduct_time_series_aggregation: bool = False
    optimized_years: int = 1
    interval_between_years: int = 1
    use_rolling_horizon: bool = False
    years_in_rolling_horizon: int = 1
    years_in_decision_horizon: int = 1
    use_capacities_existing: bool = True
    allow_investment: bool = True
    storage_charge_discharge_binary: bool = False

    @classmethod
    def load_from_existing_model(cls, existing_model_path: Path):
        if not isinstance(existing_model_path, (str, Path)):
            raise TypeError(
                f"Expected path of type `str` or `Path`, "
                f"got {type(existing_model_path)}"
            )

        system_path = find_system_file(existing_model_path)

        return cls.model_validate(read_system_file(system_path))
