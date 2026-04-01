"""Attribute module for managing element attributes with validation and data handling.

This module provides the Attribute class which represents a single attribute of an
element in the ZEN Creator system. It handles default values, units, data frames, and
source tracking with built-in validation for data types and formats.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any, Union

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from zen_creator.elements.element import Element

# Type aliases for better readability
DataFrame = Union[pd.DataFrame, pd.Series]
DefaultValue = Union[float, list, None]


class Attribute:
    """Represents a single attribute of an energy system element.

    An attribute can have default values, time-series data, yearly variations, and
    source information. It includes comprehensive validation to ensure data integrity.

    Attributes:
        name: The name of the attribute.
        element: The element this attribute belongs to.
    """

    # Constants for validation
    _ATTRIBUTES_SUPPORTING_LISTS = {
        "conversion_factor",
        "reference_carrier",
        "input_carrier",
        "output_carrier",
        "retrofit_reference_carrier",
    }

    _ATTRIBUTES_SUPPORTING_BASE_TECHNOLOGY = {"retrofit_flow_coupling_factor"}

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

    _UNIT_REPLACEMENTS = {
        "GW*h": "GWh",
        "MW*h": "MWh",
        "kW*h": "kWh",
        "/h*h": "",
    }

    _default_value: DefaultValue
    _unit: str | None
    _df: DataFrame | None
    _yearly_variations_df: DataFrame | None
    _source: str | dict[str, Any] | None

    def __init__(
        self,
        name: str,
        element: Element,
        unit: str | None = None,
        default_value: DefaultValue = None,
        base_technology: str | None = None,
        df: DataFrame | None = None,
        year_specific_dfs: dict[int, DataFrame] | None = None,
        yearly_variations_df: DataFrame | None = None,
        source: str | dict[str, Any] | None = None,
    ):
        """Initialize an Attribute.

        Args:
            name: The name of the attribute.
            element: The element this attribute belongs to.
            unit: The unit of measurement for this attribute (optional).
            default_value: Default value for the attribute (optional).
            df: Time-series data as a pandas DataFrame or Series (optional).
            yearly_variations_df: Yearly variation factors (optional).
            source: Source information for this attribute (optional).
        """
        self.name: str = name
        self.element: Element = element
        self._default_value: DefaultValue = None
        self._unit = None
        self._df: DataFrame | None = None
        self._yearly_variations_df: DataFrame | None = None
        self._year_specific_dfs: dict[int, DataFrame] = {}
        self._source: str | dict[str, Any] | None = None

        # Use setters to ensure validation is applied during initialization
        self.base_technology = base_technology
        self.default_value = default_value
        self.unit = unit
        self.df = df
        self.year_specific_dfs = year_specific_dfs or {}
        self.yearly_variations_df = yearly_variations_df
        self.source = source
        self.base_technology = base_technology

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
        if isinstance(value, list):
            self._validate_list_default_value(value)
        elif value is not None and not isinstance(
            value, (float, int, np.integer, np.floating)
        ):
            raise ValueError(
                f"Attribute '{self.name}' default value must be a float, int, or list. "
                f"Got {type(value).__name__}."
            )

        self._default_value = value

    @property
    def base_technology(self) -> str | None:
        """Set the base technology for retrofit_flow_coupling_factor."""
        return self._base_technology

    @base_technology.setter
    def base_technology(self, value: str | None) -> None:
        """Set the unit of measurement.

        Args:
            value: The unit string (e.g., 'MW', 'EUR/MW').
        """
        if value is None:
            self._base_technology = value
            return
        if self.name not in self._ATTRIBUTES_SUPPORTING_BASE_TECHNOLOGY:
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
            value: The unit string (e.g., 'MW', 'EUR/MW').
        """
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
                print(
                    f"Warning: Overwriting existing data for attribute '{self.name}'."
                )
            self._validate_dataframe_indices(value, self._ALLOWED_DF_INDEX_NAMES)

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
            if self.year_specific_dfs:
                raise ValueError(
                    f"Cannot set yearly variations data for attribute '{self.name}' "
                    f"when year-specific time series data is present."
                )
            if self._yearly_variations_df is not None:
                print(
                    f"Warning: Overwriting existing yearly variations data for "
                    f"attribute '{self.name}'."
                )
            self._validate_dataframe_indices(
                value, self._ALLOWED_YEARLY_VARIATIONS_INDEX_NAMES
            )

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
        if (self.yearly_variations_df is not None) and value:
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
            self._validate_dataframe_indices(
                df, self._ALLOWED_YEARLY_VARIATIONS_INDEX_NAMES
            )

        self._year_specific_dfs = value

    @property
    def source(self) -> str | dict[str, Any] | None:
        """Get the source information."""
        return self._source

    @source.setter
    def source(self, value: str | dict[str, Any] | None) -> None:
        """Set the source information.

        Args:
            value: Source identifier or metadata dictionary.
        """
        if self._source is not None:
            print(f"Warning: Overwriting existing source for attribute '{self.name}'.")
        self._source = value

    # ---------- Data Manipulation Methods ----------

    def set_data(
        self,
        default_value: DefaultValue = None,
        unit: str | None = None,
        df: DataFrame | None = None,
        yearly_variations_df: DataFrame | None = None,
        source: str | dict[str, Any] | None = None,
    ) -> Attribute:
        """Set multiple attribute properties at once.

        This is a convenience method for setting multiple properties in a chain.
        All parameters are optional; only provided values will be updated.

        Args:
            default_value: Default value for the attribute.
            unit: Unit of measurement.
            df: Time-series data.
            yearly_variations_df: Yearly variation factors.
            source: Source information.

        Returns:
            Self for method chaining.
        """
        if default_value is not None:
            self.default_value = default_value
        if unit is not None:
            self.unit = unit
        if df is not None:
            self.df = df
        if yearly_variations_df is not None:
            self.yearly_variations_df = yearly_variations_df
        if source is not None:
            self.source = source
        return self

    # ---------- Model Data Methods ----------

    def overwrite_from_existing_model(self, existing_element_path: Path) -> None:
        """Load attribute values from an existing model directory.

        This method loads default values from attributes.json and time-series data
        from CSV files in the existing model directory.

        Args:
            existing_element_path: Path to the existing element directory.
        """
        attributes_file = existing_element_path / "attributes.json"
        self._load_attributes_from_json(attributes_file)
        self._load_time_series_data(existing_element_path)
        self._load_yearly_variations_data(existing_element_path)
        self._load_year_specific_time_series_data(existing_element_path)

    def _load_attributes_from_json(self, file_path: Path) -> None:
        """Load attribute defaults from a JSON file.

        Args:
            file_path: Path to the attributes.json file.
        """
        if not file_path.exists():
            return

        with open(file_path, "r") as f:
            attributes_data = json.load(f)

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
        default_value = self._convert_default_value_to_serializable()

        if isinstance(default_value, dict) or (
            isinstance(default_value, list) and self.name == "conversion_factor"
        ):
            return default_value

        # serialize to dictionary
        default_dict = {
            "default_value": default_value,
            "unit": self._format_unit(),
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
            print(
                f"Saving yearly variation data for attribute '{self.name}' of element "
                f"'{element_name}' ..."
            )
            file_path = os.path.join(folder_path, f"{self.name}.csv")
            self.df.to_csv(file_path)

        if self.yearly_variations_df is not None:
            print(
                f"Saving data for attribute '{self.name}' of element "
                f"'{element_name}' ..."
            )
            file_path = os.path.join(folder_path, f"{self.name}_yearly_variation.csv")
            self.yearly_variations_df.to_csv(file_path)
        for year, df in self.year_specific_dfs.items():
            print(
                f"Saving year-specific data for attribute '{self.name}' of element "
                f"'{element_name}' for year {year}..."
            )
            file_path = os.path.join(folder_path, f"{self.name}_{year}.csv")
            df.to_csv(file_path)

    def _convert_default_value_to_serializable(self) -> Any:
        """Convert default value to a serializable format.

        Returns:
            The default value in a format suitable for JSON serialization.

        Raises:
            ValueError: If the default value has an unsupported type.
        """
        if self.default_value == np.inf:
            return "inf"
        elif isinstance(
            self.default_value, (int, float, np.integer, np.floating)
        ) and not isinstance(self.default_value, bool):
            return float(self.default_value)
        elif isinstance(self.default_value, list):
            return self._handle_list_default_value()
        else:
            raise ValueError(
                f"Attribute '{self.name}' has unsupported default value type: "
                f"{type(self.default_value).__name__}."
            )

    def _handle_list_default_value(self) -> Any:
        """Handle serialization of list-type default values.

        Returns:
            Serialized form of the list default value.

        Raises:
            ValueError: If the list default value is not supported.
        """
        if self.name == "conversion_factor":
            return self.default_value
        elif self.name in self._ATTRIBUTES_SUPPORTING_LISTS:
            return {"default_value": self.default_value}
        else:
            raise ValueError(
                f"Attribute '{self.name}' has a list as default value, which is not "
                "supported. Only conversion_factor, reference_carrier, input_carrier, "
                "output_carrier, and retrofit_reference_carrier support list values."
            )

    def _format_unit(self) -> str:
        """Format the unit string by applying standard replacements.

        Returns:
            Formatted unit string.
        """
        if self.unit is None:
            return ""

        unit = self.unit
        for old, new in self._UNIT_REPLACEMENTS.items():
            unit = unit.replace(old, new)

        unit = self._remove_safe_parentheses(unit)
        return unit

    @staticmethod
    def _remove_safe_parentheses(unit):
        """
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

    # ---------- Validation Helpers ----------

    def _validate_list_default_value(self, value: list) -> None:
        """Validate that a list default value is allowed for this attribute.

        Args:
            value: The list value to validate.

        Raises:
            ValueError: If the attribute doesn't support lists or has invalid structure.
        """
        if self.name not in self._ATTRIBUTES_SUPPORTING_LISTS:
            raise ValueError(
                f"Attribute '{self.name}' does not support a list as default value. "
                f"Only {', '.join(sorted(self._ATTRIBUTES_SUPPORTING_LISTS))} support "
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
