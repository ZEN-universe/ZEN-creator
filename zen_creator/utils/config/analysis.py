"""Mirror of the ``analysis`` block of ZEN-garden's config file.

The fields and defaults mirror ``zen_garden.config``. ZEN-creator does not
depend on ZEN-garden, so the mirror is kept in sync by
``tests/unit/test_zen_garden_schema.py``, which compares the field sets
whenever ZEN-garden is importable.
"""

from typing import Literal, Optional

from pydantic import Field

from ._base import Subscriptable


class SubsetsConfig(Subscriptable):
    """Config for the element subsets of the model."""

    set_carriers: list[str] = Field(default_factory=list)
    set_technologies: dict[str, list[str]] | list[str] = Field(
        default_factory=lambda: {
            "set_conversion_technologies": ["set_retrofitting_technologies"],
            "set_transport_technologies": [],
            "set_storage_technologies": [],
        }
    )


class HeaderDataInputsConfig(Subscriptable):
    """Config mapping input file column headers to internal set names."""

    set_nodes: str = "node"
    set_edges: str = "edge"
    set_location: str = "location"
    set_hours: str = "time"
    set_time_steps_operation: str = "time_operation"
    set_time_steps_storage_level: str = "time_storage_level"
    set_years: str = "year"
    set_years_entire_horizon: str = "year_entire_horizon"
    set_carriers: str = "carrier"
    set_input_carriers: str = "carrier"
    set_output_carriers: str = "carrier"
    set_time_steps_storage: str = "time_storage_level"
    set_dependent_carriers: str = "carrier"
    set_elements: str = "element"
    set_conversion_technologies: str = "technology"
    set_transport_technologies: str = "technology"
    set_transport_technologies_loss_exponential: str = "technology"
    set_storage_technologies: str = "technology"
    set_technologies: str = "technology"
    set_technologies_existing: str = "technology_existing"
    set_capacity_types: str = "capacity_type"
    set_retrofitting_technologies: str = "technology"


class TimeSeriesAggregationConfig(Subscriptable):
    """Config for the time series aggregation."""

    clusterMethod: str = "hierarchical"
    solver: str = "highs"
    hoursPerPeriod: int = 1
    extremePeriodMethod: Optional[str] = "None"
    rescaleClusterPeriods: bool = False
    representationMethod: str = "mean"
    resolution: int = 1


class AnalysisConfig(Subscriptable):
    """Config for the analysis block, e.g. objective and output settings."""

    dataset: str = ""
    objective: Literal["total_cost", "total_carbon_emissions"] = "total_cost"
    sense: str = "min"
    subsets: SubsetsConfig = Field(default_factory=SubsetsConfig)
    header_data_inputs: HeaderDataInputsConfig = Field(
        default_factory=HeaderDataInputsConfig
    )
    time_series_aggregation: TimeSeriesAggregationConfig = Field(
        default_factory=TimeSeriesAggregationConfig
    )
    folder_output: str = "./outputs/"
    overwrite_output: bool = True
    output_format: str = "h5"
    output_version: int = 4
    earliest_year_of_data: int = 1900
    zen_garden_version: str | None = None
