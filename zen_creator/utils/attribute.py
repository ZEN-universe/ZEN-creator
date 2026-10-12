"""Attribute module for managing element attributes with validation and data handling.

This module provides the Attribute class which represents a single attribute of an
element in the ZEN Creator system. It handles default values, units, data frames, and
source tracking with built-in validation for data types and formats.
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any, Union

import numpy as np
import pandas as pd

from zen_creator.datasets.datasets.metadata import (
    AssumptionInformation,
    SourceInformation,
)
from zen_creator.utils.file_io import find_data_file, read_data_file
from zen_creator.utils.scenario import Scenario

if TYPE_CHECKING:
    from zen_creator.elements.element import Element

logger = logging.getLogger(__name__)

# Type aliases for better readability
DataFrame = Union[pd.DataFrame, pd.Series]
DefaultValue = Union[float, list, None]
SourceLike = Union[SourceInformation, AssumptionInformation]

# Constants for validation
_ATTRIBUTES_SUPPORTING_LISTS = {
    "conversion_factor",
    "reference_carrier",
    "input_carrier",
    "output_carrier",
    "retrofit_reference_carrier",
}

_ATTRIBUTES_SUPPORTING_BASE_TECHNOLOGY = {"retrofit_flow_coupling_factor"}

_ATTRIBUTES_REQUIRING_INT = {
    "lifetime",
    "construction_time",
}

_ATTRIBUTES_REQUIRING_UNIT_ONE = {
    "lifetime",
    "construction_time",
    "min_load",
    "max_load",
    "max_diffusion_rate",
}
# Attributes whose df must be a Series named after the attribute (or a DataFrame
# with a column named after it). Unlike most attributes, whose df columns may be
# a subset of nodes, edges, or time steps, these are always long-format capacity
# series, so the name can be checked.
_ATTRIBUTES_REQUIRING_NAMED_DF = {"capacity_existing", "capacity_existing_energy"}

_ALLOWED_DF_INDEX_NAMES = {
    "time",
    "year",
    "node",
    "location",
    "edge",
    "carrier",
    "technology",
    "year_construction",
}

_ALLOWED_YEARLY_VARIATIONS_INDEX_NAMES = {
    "year",
    "node",
    "location",
    "edge",
    "carrier",
    "technology",
}

_INT_INDEX_NAMES = {"year", "year_construction", "time"}

_UNIT_REPLACEMENTS = {
    "GW*h": "GWh",
    "MW*h": "MWh",
    "kW*h": "kWh",
    "/h*h": "",
}

# Fields that carry an attribute's actual computed value. Reading one of
# these (e.g. `element.lifetime.default_value`) is what triggers auto-build
# of an unbuilt attribute, see Attribute.__getattribute__. Fetching the
# Attribute object itself (`element.lifetime`) or calling a method on it
# (`.set_data(...)`) does not, since neither consumes the value.
_DATA_FIELDS = frozenset(
    {
        "default_value",
        "unit",
        "base_technology",
        "df",
        "year_specific_dfs",
        "yearly_variations_df",
        "sources",
    }
)


class Attribute:
    """Represents a single attribute of an energy system element.

    An attribute can have default values, time-series data, yearly variations, and
    source information. It includes comprehensive validation to ensure data integrity.

    Attributes:
        name: The name of the attribute.
        element: The element this attribute belongs to.
    """

    def __init__(
        self,
        name: str,
        element: Element,
        default_value: DefaultValue = None,
        unit: str | None = None,
        base_technology: str | None = None,
        df: DataFrame | None = None,
        year_specific_dfs: dict[int, DataFrame] | None = None,
        yearly_variations_df: DataFrame | None = None,
        sources: list[SourceLike] | None = None,
    ):
        """Initialize an Attribute.

        Args:
            name: The name of the attribute.
            element: The element this attribute belongs to.
            default_value: Default value for the attribute (optional).
            unit: The unit of measurement for this attribute (optional).
            base_technology: Base technology for retrofit_flow_coupling_factor
                (optional).
            df: Time-series data as a pandas DataFrame or Series (optional).
            year_specific_dfs: Year-specific data frames (optional).
            yearly_variations_df: Yearly variation factors (optional).
            sources: Ordered source information entries for this attribute (optional).
        """
        self.name: str = name
        self.element: Element = element
        self._default_value: DefaultValue = None
        self._unit: str | None = None
        self._df: DataFrame | None = None
        self._yearly_variations_df: DataFrame | None = None
        self._year_specific_dfs: dict[int, DataFrame] = {}
        self._sources: list[SourceLike] = []
        self.scenarios: dict[str, Scenario] = {}

        # Use setters to ensure validation is applied during initialization
        self.base_technology = base_technology
        self.default_value = default_value
        self.unit = unit
        self.df = df
        self.year_specific_dfs = year_specific_dfs or {}
        self.yearly_variations_df = yearly_variations_df
        self.sources = sources or []
        self.base_technology = base_technology

    def __getattribute__(self, name: str):
        """Return the requested field, auto-building an unbuilt attribute first.

        Only fields in ``_DATA_FIELDS`` (the actual data - default_value, df,
        etc.) trigger anything; fetching the Attribute object itself or
        calling a method on it never does, since neither of those consumes a value.

        For a data field belonging to an unbuilt attribute with a
        ``_set_<name>`` setter, that setter is run now (via
        ``Element._build_attribute``).

        Because a setter may replace rather than mutate the Attribute object
        (``setattr(element, name, new_attribute)``), ``self`` can end up
        stale - e.g. a reference captured before the (re)build. So the field
        is always read off whatever is currently registered on the element,
        redirecting there if it differs from ``self``.
        """
        if name in _DATA_FIELDS:
            element = object.__getattribute__(self, "element")
            attr_name = object.__getattribute__(self, "name")
            stack = element.model._build_stack
            is_self_reference = bool(stack) and stack[-1] == (element, attr_name)

            if (
                not is_self_reference
                and attr_name not in element._built_attribute_names
            ):
                if getattr(type(element), f"_set_{attr_name}", None) is not None:
                    # the stack is empty when the field is read outside a build
                    trigger = (
                        f" (triggered by '{stack[-1][0].name}._set_{stack[-1][1]}')"
                        if stack
                        else ""
                    )
                    logger.info(
                        f"Auto-building '{attr_name}' of '{element.name}'{trigger}"
                    )
                    element._build_attribute(attr_name)

            current = getattr(element, attr_name)
            if current is not self:
                return object.__getattribute__(current, name)

        return object.__getattribute__(self, name)

    # ---------- Properties ----------

    @property
    def default_value(self) -> DefaultValue:
        """Get the default value of this attribute."""
        return self._default_value

    @default_value.setter
    def default_value(self, value: DefaultValue) -> None:
        """Set the default value with validation.

        Args:
            value: The new default value.

        Raises:
            ValueError: If the value type is not valid for this attribute.
        """
        self._validate_default_value(value)
        self._default_value = value

    def _validate_default_value(self, value: DefaultValue) -> None:
        """Validate a default value for this attribute.

        Used both for the attribute's own default value and for the default
        values of its scenario variations, so the two follow the same rules.

        Args:
            value: The default value to validate.

        Raises:
            ValueError: If the value type is not valid for this attribute.
        """
        if isinstance(value, list):
            self._validate_list_default_value(value)
        elif self.name in _ATTRIBUTES_REQUIRING_INT:
            is_whole_number = isinstance(value, (int, np.integer)) or (
                isinstance(value, (float, np.floating)) and float(value).is_integer()
            )
            if not is_whole_number and value is not np.nan:
                raise ValueError(
                    f"Attribute '{self.name}' of {self.element.name} default value "
                    f"must be a whole number. Got {type(value).__name__} ({value})."
                )
        elif self.name in _ATTRIBUTES_SUPPORTING_LISTS:
            raise ValueError(
                f"Attribute '{self.name}' default value must be a list. "
                f"Got {type(value).__name__}."
            )
        elif value is not None and not isinstance(
            value, (float, int, np.integer, np.floating)
        ):
            raise ValueError(
                f"Attribute '{self.name}' default value must be a float, int, or list. "
                f"Got {type(value).__name__}."
            )

    @property
    def base_technology(self) -> str | None:
        """Set the base technology for retrofit_flow_coupling_factor."""
        return self._base_technology

    @base_technology.setter
    def base_technology(self, value: str | None) -> None:
        """Set the base technology for retrofit_flow_coupling_factor with validation.

        Args:
            value: The base technology name as a string.
        """
        if value is None:
            self._base_technology = value
            return
        if self.name not in _ATTRIBUTES_SUPPORTING_BASE_TECHNOLOGY:
            raise ValueError(
                f"Attribute '{self.name}' cannot have a 'base_technology'."
            )
        if not isinstance(value, str):
            raise ValueError(
                f"Attribute '{self.name}' base_technology must be a str. "
                f"Got {type(value).__name__}."
            )

        self._base_technology = value

    @property
    def unit(self) -> str | None:
        """Get the unit of measurement."""
        return self._unit

    @unit.setter
    def unit(self, value: str | None) -> None:
        """Set the unit of measurement.

        Args:
            value: The unit string (e.g., 'MW', 'Euro/MW').

        Raises:
            ValueError: If the unit does not match what this attribute requires.
        """
        if value is not None and "year" in value:
            raise ValueError(
                f"Attribute '{self.name}' unit should not contain 'year'. "
                f"Got '{value}'."
            )
        if (
            value is not None
            and self.name in _ATTRIBUTES_REQUIRING_UNIT_ONE
            and value != "1"
        ):
            raise ValueError(
                f"Attribute '{self.name}' unit must be '1'. Got '{value}'."
            )

        # if self.name == "opex_specific_fixed" and value is not None:
        #     power_unit = self.element.power_unit
        #     allowed_units = {f"Euro/{power_unit}", f"Euro/({power_unit})"}
        #     if value not in allowed_units:
        #         raise ValueError(
        #             f"Attribute '{self.name}' unit must be 'Euro/{power_unit}'. "
        #             f"Got '{value}'."
        #         )
        self._unit = value

    @property
    def df(self) -> DataFrame | None:
        """Get the time-series data."""
        return self._df

    @df.setter
    def df(self, value: DataFrame | None) -> None:
        """Set the time-series data with validation.

        Args:
            value: A pandas DataFrame or Series with validated index names.

        Raises:
            ValueError: If any index name is not allowed.
        """
        if value is not None:
            if self._df is not None:
                logger.warning(
                    f"Overwriting existing data for attribute '{self.name}' "
                    f"of element '{self.element.name}'."
                )
            self._validate_dataframe_indices(value, _ALLOWED_DF_INDEX_NAMES)
            value = self._validate_integer_indices(value)
            self._validate_dataframe_name(value)

        self._df = value

    @property
    def yearly_variations_df(self) -> DataFrame | None:
        """Get the yearly variations data."""
        return self._yearly_variations_df

    @yearly_variations_df.setter
    def yearly_variations_df(self, value: DataFrame | None) -> None:
        """Set the yearly variations data with validation.

        Args:
            value: A pandas DataFrame or Series with validated index names.

        Raises:
            ValueError: If any index name is not allowed.
        """
        if value is not None:
            if self._year_specific_dfs:
                raise ValueError(
                    f"Cannot set yearly variations data for attribute '{self.name}' "
                    f"of element '{self.element.name}' "
                    f"when year-specific time series data is present."
                )
            if self._yearly_variations_df is not None:
                logger.warning(
                    f"Overwriting existing yearly variations data for "
                    f"attribute '{self.name}' of element '{self.element.name}'."
                )
            self._validate_dataframe_indices(
                value, _ALLOWED_YEARLY_VARIATIONS_INDEX_NAMES
            )
            value = self._validate_integer_indices(value)

        self._yearly_variations_df = value

    @property
    def year_specific_dfs(self) -> dict[int, DataFrame]:
        """Get the year-specific time series data."""
        return self._year_specific_dfs

    @year_specific_dfs.setter
    def year_specific_dfs(self, value: dict[int, DataFrame]) -> None:
        """Set the year-specific time series data with validation.

        Args:
            value: A dictionary mapping years to pandas DataFrames.
                The keys of the dictionary should be
                integers representing years, and the values should be
                DataFrames with appropriate indices.

        Raises:
            ValueError: If any index name is not allowed.
        """
        if (self._yearly_variations_df is not None) and value:
            raise ValueError(
                f"Cannot set year-specific data for attribute"
                f"'{self.name}' when yearly variations data is present."
            )
        if not isinstance(value, dict):
            raise ValueError(
                f"year_specific_dfs must be a dictionary mapping years to "
                f"DataFrames. Got {type(value).__name__}."
            )
        for year, df in value.items():
            if not isinstance(year, int):
                raise ValueError(
                    f"Year key '{year}' in year_specific_dfs must be an integer."
                )
            self._validate_dataframe_indices(df, _ALLOWED_YEARLY_VARIATIONS_INDEX_NAMES)

            value[year] = self._validate_integer_indices(df)

        self._year_specific_dfs = value

    @property
    def sources(self) -> list[SourceLike]:
        """Get the ordered source information entries."""
        return self._sources

    @sources.setter
    def sources(self, value: list[SourceLike]) -> None:
        """Set ordered source information entries.

        Args:
            value: Ordered list of SourceInformation/AssumptionInformation objects.
        """
        if not isinstance(value, list):
            raise ValueError(
                f"Attribute '{self.name}' sources must be a list. "
                f"Got {type(value).__name__}."
            )

        for i, source_info in enumerate(value):
            if not isinstance(source_info, (SourceInformation, AssumptionInformation)):
                raise ValueError(
                    f"Entry {i} in sources for attribute '{self.name}' must be a "
                    f"SourceInformation or AssumptionInformation object. "
                    f"Got {type(source_info).__name__}."
                )

        self._sources = list(value)

    def add_source(self, source: SourceLike) -> None:
        """Append a source entry while preserving insertion order.

        Args:
            source: Source or assumption information to append.
        """
        if not isinstance(source, (SourceInformation, AssumptionInformation)):
            raise ValueError(
                f"Source for attribute '{self.name}' must be a SourceInformation "
                f"or AssumptionInformation object. Got {type(source).__name__}."
            )
        self._sources.append(source)

    # ---------- Data Manipulation Methods ----------

    def set_data(
        self,
        source: SourceLike,
        default_value: DefaultValue = None,
        unit: str | None = None,
        df: DataFrame | None = None,
        yearly_variations_df: DataFrame | None = None,
        base_technology: str | None = None,
        scenarios: Scenario | list[Scenario] | None = None,
    ) -> Attribute:
        """Set multiple attribute properties at once.

        This is a convenience method for setting multiple properties in a chain.
        The source parameter is mandatory. It should contain a SourceInformation
        object that includes a description of changes and the corresponding
        Dataset/DatasetCollection MetaData to ensure proper source tracking, or an
        AssumptionInformation object when the value stems from a modeling choice
        rather than an external data source.

        Args:
            default_value: Default value for the attribute.
            unit: Unit of measurement.
            df: Time-series data.
            yearly_variations_df: Yearly variation factors.
            base_technology: Name of the base technology.
            source: Source information to append to the ordered source list.
            scenarios: Variations of this attribute in a scenario analysis.

        Returns:
            Self for method chaining.

        Examples:
            >>> attribute.set_data(
            ...     source=source,
            ...     default_value=3.0,
            ...     unit="Euro/MWh",
            ...     scenarios=[
            ...         Scenario("cheap", default_value=1.5),
            ...         Scenario("sweep", default_op=[0.5, 1.5]),
            ...     ],
            ... )
        """
        if default_value is not None:
            self.default_value = default_value
        if unit is not None:
            self.unit = unit
        if df is not None:
            self.df = df
        if yearly_variations_df is not None:
            self.yearly_variations_df = yearly_variations_df
        if base_technology is not None:
            self.base_technology = base_technology
        if scenarios is not None:
            self.add_scenarios(scenarios)
        self.add_source(source)
        return self

    def add_scenarios(self, scenarios: Scenario | list[Scenario]) -> None:
        """Attach scenario variations to this attribute.

        The variations are registered with the model right away, so that the
        scenario file is complete before the model is written.

        Args:
            scenarios: A single variation or a list of variations.

        Raises:
            ValueError: If a scenario is already attached to this attribute, or
                if a variation's data does not follow the same rules as the
                attribute's own data.
        """
        if isinstance(scenarios, Scenario):
            scenarios = [scenarios]

        for scenario in scenarios:
            if not isinstance(scenario, Scenario):
                raise ValueError(
                    f"Scenario of attribute '{self.name}' must be a Scenario "
                    f"object. Got {type(scenario).__name__}."
                )
            self._validate_scenario(scenario)
            if scenario.name in self.scenarios:
                raise ValueError(
                    f"Scenario '{scenario.name}' is already defined for attribute "
                    f"'{self.name}' of element '{self.element.name}'."
                )

            self.scenarios[scenario.name] = scenario
            self.element.model.scenarios.register_scenario(
                self.element.scenario_key, self.name, scenario
            )

    def _validate_scenario(self, scenario: Scenario) -> None:
        """Validate a scenario variation against the rules of this attribute.

        Reuses the same validation as the attribute's own default value and
        data, so a variation cannot hold data the attribute would otherwise
        reject.

        Args:
            scenario: The scenario variation to validate.

        Raises:
            ValueError: If the variation's default value or data is invalid
                for this attribute.
        """
        if scenario.default_value is not None:
            self._validate_default_value(scenario.default_value)
        if scenario.df is not None:
            self._validate_dataframe_indices(scenario.df, _ALLOWED_DF_INDEX_NAMES)
            scenario.df = self._validate_integer_indices(scenario.df)
        if scenario.yearly_variations_df is not None:
            self._validate_dataframe_indices(
                scenario.yearly_variations_df, _ALLOWED_YEARLY_VARIATIONS_INDEX_NAMES
            )
            scenario.yearly_variations_df = self._validate_integer_indices(
                scenario.yearly_variations_df
            )

    # ---------- Model Data Methods ----------

    def overwrite_from_existing_model(self, existing_element_path: Path) -> None:
        """Load attribute values from an existing model directory.

        This method loads default values from the attributes file and
        time-series data from CSV files in the existing model directory.

        Args:
            existing_element_path: Path to the existing element directory.
        """
        self._load_attributes_from_file(existing_element_path)
        self._load_time_series_data(existing_element_path)
        self._load_yearly_variations_data(existing_element_path)
        self._load_year_specific_time_series_data(existing_element_path)

    def _load_attributes_from_file(self, element_path: Path) -> None:
        """Load attribute defaults from the attributes file.

        Args:
            element_path: Path to the existing element directory.
        """
        file_path = find_data_file(element_path, "attributes")
        if file_path is None:
            return

        attributes_data = read_data_file(file_path)

        if self.name not in attributes_data:
            return

        attr_data = attributes_data[self.name]
        if "default_value" in attr_data:
            if attr_data["default_value"] == "inf":
                self.default_value = np.inf
            else:
                self.default_value = attr_data["default_value"]
        if "unit" in attr_data:
            self.unit = attr_data["unit"]
        if "base_technology" in attr_data:
            self.base_technology = attr_data["base_technology"]
        if self.name == "conversion_factor":
            self.default_value = attr_data

    def _load_time_series_data(self, data_dir: Path) -> None:
        """Load time-series data from a CSV file.

        Args:
            data_dir: Directory containing the data file.
        """
        data_file = data_dir / f"{self.name}.csv"
        if data_file.exists():
            self.df = pd.read_csv(data_file, index_col=0)

    def _load_yearly_variations_data(self, data_dir: Path) -> None:
        """Load yearly variation data from a CSV file.

        Args:
            data_dir: Directory containing the yearly variations file.
        """
        variations_file = data_dir / f"{self.name}_yearly_variation.csv"
        if variations_file.exists():
            self.yearly_variations_df = pd.read_csv(variations_file, index_col=0)

    def _load_year_specific_time_series_data(self, data_dir: Path) -> None:
        """Load year-specific time-series data from CSV files.

        The csv files must have the name format "{attribute_name}_{year}.csv",
        e.g. "capacity_addition_max_2030.csv".

        Args:
            data_dir: Directory containing the year-specific data files.
        """
        for file in data_dir.glob(f"{self.name}_*.csv"):
            year_str = file.stem.split("_")[-1]
            if year_str.isdigit():
                year = int(year_str)
                self.year_specific_dfs[year] = pd.read_csv(file, index_col=0)

    # ---------- Output Methods ----------

    def default_to_dict(self) -> dict | list[dict]:
        """Convert the default value and unit to a dictionary representation.

        Returns:
            Dictionary with 'default_value' and 'unit' keys.

        Raises:
            ValueError: If the default value type is not serializable.
        """
        return self._default_to_dict(self.default_value, self.unit)

    def scenario_default_to_dict(self, scenario: Scenario) -> dict | list[dict]:
        """Convert the default value of a scenario variation.

        Args:
            scenario: The variation whose default value is serialized.

        Returns:
            Dictionary with 'default_value' and 'unit' keys.
        """
        unit = scenario.unit if scenario.unit is not None else self.unit

        return self._default_to_dict(scenario.default_value, unit)

    def _default_to_dict(
        self, default_value: DefaultValue, unit: str | None
    ) -> dict | list[dict]:
        """Convert a default value and unit to a dictionary representation.

        Args:
            default_value: The default value to serialize.
            unit: The unit of the default value.

        Returns:
            Dictionary with 'default_value' and 'unit' keys.

        Raises:
            ValueError: If the default value type is not serializable.
        """
        default_value = self._convert_default_value_to_serializable(default_value)

        if isinstance(default_value, dict) or (
            isinstance(default_value, list) and self.name == "conversion_factor"
        ):
            return default_value

        # serialize to dictionary
        default_dict = {
            "default_value": default_value,
            "unit": self._format_unit(unit),
        }

        # add base_technology if necessary
        if self.base_technology is not None:
            default_dict["base_technology"] = self.base_technology

        return default_dict

    def save_data(self, folder_path: str, element_name: str) -> None:
        """Save time-series data to a CSV file.

        Args:
            folder_path: Directory where the file will be saved.
            element_name: Name of the element (for logging purposes).
        """
        if self.df is not None:
            logger.info(
                f"Saving yearly variation data for attribute '{self.name}' of element "
                f"'{element_name}' ..."
            )
            file_path = os.path.join(folder_path, f"{self.name}.csv")
            self.df.to_csv(file_path)

        if self.yearly_variations_df is not None:
            logger.info(
                f"Saving data for attribute '{self.name}' of element "
                f"'{element_name}' ..."
            )
            file_path = os.path.join(folder_path, f"{self.name}_yearly_variation.csv")
            self.yearly_variations_df.to_csv(file_path)
        for year, df in self.year_specific_dfs.items():
            logger.info(
                f"Saving year-specific data for attribute '{self.name}' of element "
                f"'{element_name}' for year {year}..."
            )
            file_path = os.path.join(folder_path, f"{self.name}_{year}.csv")
            df.to_csv(file_path)

        for scenario in self.scenarios.values():
            for file_name, df in scenario.data_files(self.name).items():
                logger.info(
                    f"Saving data of scenario '{scenario.name}' for attribute "
                    f"'{self.name}' of element '{element_name}' ..."
                )
                file_path = os.path.join(folder_path, f"{file_name}.csv")
                df.to_csv(file_path)

    def _convert_default_value_to_serializable(
        self, default_value: DefaultValue
    ) -> Any:
        """Convert default value to a serializable format.

        Args:
            default_value: The default value to convert.

        Returns:
            The default value in a format suitable for JSON serialization.

        Raises:
            ValueError: If the default value has an unsupported type.
        """
        if default_value == np.inf:
            return "inf"
        elif isinstance(
            default_value, (int, float, np.integer, np.floating)
        ) and not isinstance(default_value, bool):
            return float(default_value)
        elif isinstance(default_value, list):
            return self._handle_list_default_value(default_value)
        else:
            raise ValueError(
                f"Attribute '{self.name}' has unsupported default value type: "
                f"{type(default_value).__name__}."
            )

    def _handle_list_default_value(self, default_value: list) -> Any:
        """Handle serialization of list-type default values.

        Args:
            default_value: The list default value to serialize.

        Returns:
            Serialized form of the list default value.

        Raises:
            ValueError: If the list default value is not supported.
        """
        if self.name == "conversion_factor":
            return [
                {
                    carrier: {**factor, "default_value": float(factor["default_value"])}
                    for carrier, factor in entry.items()
                }
                for entry in default_value
            ]
        elif self.name in _ATTRIBUTES_SUPPORTING_LISTS:
            return {"default_value": default_value}
        else:
            raise ValueError(
                f"Attribute '{self.name}' has a list as default value, which is not "
                "supported. Only conversion_factor, reference_carrier, input_carrier, "
                "output_carrier, and retrofit_reference_carrier support list values."
            )

    def _format_unit(self, unit: str | None) -> str:
        """Format the unit string by applying standard replacements.

        Args:
            unit: The unit string to format.

        Returns:
            Formatted unit string.
        """
        if unit is None:
            return ""

        for old, new in _UNIT_REPLACEMENTS.items():
            unit = unit.replace(old, new)

        unit = self._remove_safe_parentheses(unit)
        return unit

    @staticmethod
    def _remove_safe_parentheses(unit):
        r"""
        Remove parentheses around substrings that don't contain '(', ')', '*' or '/'.

        Pattern explanation:
        \(          : Match literal opening parenthesis
        (           : Start capturing group #1 (the content inside)
        [^()*/]* : Match 0+ chars that are NOT '(', ')', '*', or '/'
        )           : End capturing group
        \)          : Match literal closing parenthesis
        """
        pattern = r"\(([^()*/]*)\)"

        while True:
            new_unit = re.sub(pattern, r"\1", unit)

            if new_unit == unit:
                break

            unit = new_unit

        return unit

    def sources_to_str(self) -> str:
        """Serialize the ordered sources into a readable numbered string.

        Returns:
            A multi-line string where each source is prefixed with its insertion
            order so the sequence of additions remains visible.
        """
        if not self._sources:
            return ""

        blocks: list[str] = []
        for index, source in enumerate(self._sources, start=1):
            blocks.append(f"Step {index}\n{source.to_str()}")

        return "\n\n----\n\n".join(blocks)

    # ---------- Validation Helpers ----------

    def _validate_list_default_value(self, value: list) -> None:
        """Validate that a list default value is allowed for this attribute.

        Args:
            value: The list value to validate.

        Raises:
            ValueError: If the attribute doesn't support lists or has invalid structure.
        """
        if self.name not in _ATTRIBUTES_SUPPORTING_LISTS:
            raise ValueError(
                f"Attribute '{self.name}' does not support a list as default value. "
                f"Only {', '.join(sorted(_ATTRIBUTES_SUPPORTING_LISTS))} support "
                "lists."
            )

        if self.name == "conversion_factor":
            for i, entry in enumerate(value):
                if not isinstance(entry, dict):
                    raise ValueError(
                        f"Entry {i} in conversion_factor list must be a dict, "
                        f"got {type(entry).__name__}."
                    )
                for name, factor in entry.items():
                    if "default_value" not in factor or "unit" not in factor:
                        raise ValueError(
                            f"Entry {name} in conversion_factor list must contain "
                            "'default_value' and 'unit' keys."
                        )
                    if not isinstance(factor["default_value"], (int, float)):
                        raise ValueError(
                            f"Entry {name} in conversion_factor list must have a "
                            "'default_value' of type int or float, got "
                            f"{type(factor['default_value']).__name__}."
                        )
                    if not isinstance(factor["unit"], str):
                        raise ValueError(
                            f"Entry {name} in conversion_factor list must have a "
                            "'unit' of type str, got "
                            f"{type(factor['unit']).__name__}."
                        )

    def _validate_dataframe_name(self, value: DataFrame) -> None:
        """Validate that a capacity_existing(_energy) df is labeled with its name.

        Args:
            value: The DataFrame or Series to validate.

        Raises:
            ValueError: If a Series isn't named after the attribute, or a
                DataFrame has no column named after the attribute.
        """
        # TODO implement for all attributes, not just capacity_existing(_energy)
        # figure out how to handle the case where a DataFrame has multiple columns,
        # which are a subset of the nodes/edges/time steps.
        # In that case, we can't check the name.
        if self.name not in _ATTRIBUTES_REQUIRING_NAMED_DF:
            return

        if isinstance(value, pd.Series):
            if value.name != self.name:
                raise ValueError(
                    f"df for attribute '{self.name}' of element '{self.element.name}' "
                    f"must be a Series named '{self.name}'. Got '{value.name}'."
                )
        elif self.name not in value.columns:
            raise ValueError(
                f"df for attribute '{self.name}' of element '{self.element.name}' "
                f"must have a column named '{self.name}'. Got columns "
                f"{list(value.columns)}."
            )

    def _validate_dataframe_indices(self, df: DataFrame, allowed_names: set) -> None:
        """Validate DataFrame index names against allowed values.

        Args:
            df: The DataFrame to validate.
            allowed_names: Set of allowed index names.

        Raises:
            ValueError: If any index name is not in the allowed set.
        """
        invalid_indices = set(df.index.names) - allowed_names
        if invalid_indices:
            raise ValueError(
                f"Invalid index names {invalid_indices} in attribute '{self.name}'. "
                f"Allowed names are: {', '.join(sorted(allowed_names))}."
            )

    def _validate_integer_indices(self, df: DataFrame) -> DataFrame:
        """Validate that integer indices are of integer type or can be converted.

        Args:
            df: The DataFrame to validate.

        Raises:
            ValueError: If any integer index is not of integer type or cannot be
                converted.

        Returns:
            df: The validated or converted DataFrame.
        """
        int_indices = [
            name
            for name in df.index.names
            if isinstance(name, str) and name in _INT_INDEX_NAMES
        ]
        for name in int_indices:
            level_values = df.index.get_level_values(name)
            if pd.api.types.is_integer_dtype(level_values):
                continue
            _is_numeric = pd.api.types.is_numeric_dtype(level_values)
            try:
                parsed = level_values.astype(int)
            except (ValueError, TypeError):
                parsed = None
            if parsed is None or (_is_numeric and not parsed.equals(level_values)):
                raise ValueError(
                    f"Index '{name}' in attribute '{self.name}' of "
                    f"element '{self.element.name}' must be of integer "
                    f"type. Got {level_values.dtype} and cannot be converted to "
                    "integer."
                )
            logger.warning(
                f"Index '{name}' in attribute '{self.name}' of "
                f"element '{self.element.name}' is of type "
                f"{level_values.dtype} instead of integer, but parses cleanly as "
                "integer.\n"
                "Convert the index to integer type to avoid this warning."
            )
            if isinstance(df.index, pd.MultiIndex):
                level_pos = df.index.names.index(name)
                df.index = df.index.set_levels(
                    df.index.levels[level_pos].astype(int).tolist(), level=name
                )
            else:
                df.index = df.index.astype(int)

        return df
