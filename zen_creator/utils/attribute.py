from __future__ import annotations
from typing import Union, TYPE_CHECKING
import pandas as pd
import numpy as np
import re
import os
from pathlib import Path
import json

if TYPE_CHECKING:
    from zen_creator.elements.element import Element

class Attribute:
    def __init__(
        self,
        name: str,
        element: Element,
        unit: str = None,
        default_value: Union[float, list] = None,
        df: Union[pd.DataFrame, pd.Series] = None,
        source: str = None,
    ):
        self.name = name
        self.element = element
        self.default_value = default_value
        self.unit = unit
        self.df = df
        self.source = source
        # self.overwrite_from_existing_model()

    def set_data(
        self,
        default_value: Union[float, list] = None,
        unit: str = None,
        df: Union[pd.DataFrame, pd.Series] = None,
        source: str = None,
    ):
        if default_value is not None:
            self.set_default_value(default_value)
        if unit is not None:
            self.set_unit(unit)
        if df is not None:
            self.set_df(df)
        if source is not None:
            self.set_source(source)
        return self

    def set_default_value(self, default_value: Union[float, list]):
        list_supported = [
            "conversion_factor",
            "reference_carrier",
            "input_carrier",
            "output_carrier",
        ]

        if isinstance(default_value, list):
            if self.name not in list_supported:
                raise ValueError(
                    (
                        f"Attribute '{self.name}' does not support a list as default value. "
                        f"Only {', '.join(list_supported)} support list default values."
                    )
                )

            if self.name == "conversion_factor":
                for v in default_value:
                    if not isinstance(v, dict):
                        raise ValueError(
                            f"Each entry in the default value list for 'conversion_factor' must be a dict."
                        )
                    for n, c in v.items():
                        if "default_value" not in c or "unit" not in c:
                            raise ValueError(
                                f"Each entry in the default value list for 'conversion_factor' must be a dict with 'default_value' and 'unit' keys."
                            )
        elif not isinstance(default_value, (float, int)):
            raise ValueError(
                f"Attribute '{self.name}' default value must be a float, int, or list (for {', '.join(list_supported)})."
            )

        self.default_value = default_value
        return self

    def set_unit(self, unit: str):
        self.unit = unit
        return self

    def set_df(self, df: Union[pd.DataFrame, pd.Series]):
        if self.df is not None:
            print(f"Warning: Overwriting existing data for attribute '{self.name}'.")
        for idx_name in df.index.names:
            if idx_name not in [
                "time",
                "year",
                "node",
                "location",
                "edge",
                "carrier",
                "technology",
                "year_construction",
            ]:
                raise ValueError(
                    f"Index name '{idx_name}' in DataFrame for attribute '{self.name}' is not allowed. Allowed index names are 'time', 'year', 'node', 'location', 'edge', 'carrier', 'technology'."
                )
        # TODO more checks on df?
        self.df = df
        return self

    def get_df(self) -> Union[pd.DataFrame, pd.Series]:
        return self.df

    def set_source(self, source: str):
        if self.source is not None:
            print(f"Warning: Overwriting existing source for attribute '{self.name}'.")
        self.source = source
        return self

    def default_to_dict(self):
        if self.default_value == np.inf:
            default_value = "inf"
        elif isinstance(self.default_value, float) or isinstance(
            self.default_value, int
        ):
            default_value = self.default_value
        elif isinstance(
            self.default_value, (np.float16, np.float32, np.float64)
        ) or isinstance(self.default_value, (np.int8, np.int16, np.int32, np.int64)):
            default_value = float(self.default_value)
        elif isinstance(self.default_value, list):
            if self.name == "conversion_factor":
                return self.default_value
            elif self.name in ["reference_carrier", "input_carrier", "output_carrier"]:
                return {"default_value": self.default_value}
            else:
                raise ValueError(
                    (
                        f"Attribute {self.name} has a list as default value, which is not supported. "
                        f"Only 'conversion_factor', 'reference_carrier', 'input_carrier' and 'output_carrier' support list default values."
                    )
                )
        elif self.default_value is None:
            raise ValueError(f"Attribute {self.name} has no default value set.")
        else:
            raise ValueError(
                f"Attribute {self.name} has default value of unsupported type {type(self.default_value)}."
            )

        return {"default_value": default_value, "unit": self.format_unit()}

    def format_unit(self):
        unit = self.unit
        if "GW*h" in unit:
            unit = unit.replace("GW*h", "GWh")
        if "MW*h" in unit:
            unit = unit.replace("MW*h", "MWh")
        if "kW*h" in unit:
            unit = unit.replace("kW*h", "kWh")
        if "/h*h" in unit:
            unit = unit.replace("/h*h", "")
        unit = self.remove_safe_parentheses(unit)
        return unit

    def save_data(self, folder_path: str, element_name: str):
        if self.df is not None:
            print(
                f"Saving data for attribute '{self.name}' of element '{element_name}' ..."
            )
            file_path = os.path.join(folder_path, f"{self.name}.csv")
            self.df.to_csv(file_path)

    @staticmethod
    def remove_safe_parentheses(unit):
        # Pattern explanation:
        # \(          : Match literal opening parenthesis
        # (           : Start capturing group #1 (the content inside)
        #   [^()*/]* : Match 0+ chars that are NOT '(', ')', '*', or '/'
        # )           : End capturing group
        # \)          : Match literal closing parenthesis
        pattern = r"\(([^()*/]*)\)"

        while True:
            new_unit = re.sub(pattern, r"\1", unit)

            if new_unit == unit:
                break

            unit = new_unit

        return unit

    def overwrite_from_existing_model(self, existing_element_path: Path):
        attributes_file_path = existing_element_path / "attributes.json"
        if attributes_file_path.exists():
            with open(attributes_file_path, "r") as f:
                attributes_data = json.load(f)
            if self.name in attributes_data:
                attr_data = attributes_data[self.name]
                if "default_value" in attr_data:
                    if attr_data["default_value"] == "inf":
                        self.default_value = np.inf
                    else:
                        self.default_value = attr_data["default_value"]
                if "unit" in attr_data:
                    self.unit = attr_data["unit"]
                if self.name in [
                    "conversion_factor",
                    "reference_carrier",
                    "input_carrier",
                    "output_carrier",
                ]:
                    self.default_value = attr_data
        data_file_path = existing_element_path / f"{self.name}.csv"
        if data_file_path.exists():
            df = pd.read_csv(data_file_path, index_col=0)
            self.df = df


class SystemAttribute(Attribute):
    def __init__(
        self,
        name: str,
        element: Element,
        value: Union[float, list, bool] = None,
        default_value: Union[float, list, bool] = None,
    ):
        self.value = value
        super().__init__(name=name, element=element, default_value=default_value)

    def overwrite_from_existing_model(self, existing_element_path: Path):
        system_file_path = existing_element_path / "system.json"
        if system_file_path.exists():

            with open(system_file_path, "r") as f:
                system_data = json.load(f)
            if self.name in system_data:
                self.value = system_data[self.name]
