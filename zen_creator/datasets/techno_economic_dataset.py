from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

import pandas as pd
import numpy as np
from zen_creator.datasets.dataset import Dataset
from zen_creator.utils.helpers import get_partial_index

class TechnoEconomicDataset(Dataset):
    """Dataset class for techno-economic source data."""

    name = "techno_economic_dataset"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path = source_path)

        self.available_technologies_finance = []
        self.available_technologies_efficiency = []
        self.available_technologies_lifetime = []
        self.available_technologies_construction_time = []

    @property
    @abstractmethod
    def money_year_source(self) -> int:
        pass
    
    @property
    @abstractmethod
    def unit(self) -> str:
        pass
    
    @abstractmethod
    def get_cost_data(self, technology: str, variable: str) -> pd.DataFrame:
        """Method to get the finance data of a technology."""
        pass

    @abstractmethod
    def get_lifetime(self, technology: str) -> pd.DataFrame:
        """Method to get the lifetime of a technology."""
        pass

    @abstractmethod
    def get_efficiency(self, technology: str) -> pd.DataFrame:
        """Method to get the efficiency of a technology."""
        pass

    @abstractmethod
    def get_construction_time(self, technology: str) -> pd.DataFrame:
        """Method to get the construction time of a technology."""
        pass

    @staticmethod
    def get_years() -> list[int]:
        """Get the list of years for techno-economic data."""
        start_year = 2015
        end_year = 2050
        return list(range(start_year, end_year+1))
    
    @staticmethod
    def get_units(unit,is_ccs=False):
        """ returns money, energy and power unit """
        if is_ccs:
            units = {
                "money": "Euro",
                "energy": "tCO2",
                "power": "tCO2/hour"
            }
        else:
            units = {
                "money": "Euro",
                "energy": "kWh",
                "power": "kW"
            }
        return units[unit]
    
    def rename_index(self,df: pd.DataFrame, rename_map: dict) -> pd.DataFrame:
        """Method to rename index based on a mapping dictionary."""
        df_renamed = df.copy()
        if isinstance(df_renamed, pd.Series):
            df_renamed = df_renamed.to_frame()
        inv_map = {}
        max_len = max([len(v) for v in rename_map.values() if isinstance(v, tuple)] + [1])
        for k, v in rename_map.items():
            inv_map.setdefault(v, []).append(k)
            
        df_renamed["new_ids"] = df_renamed.index.map(lambda idx: get_partial_index(idx, inv_map=inv_map))
        df_renamed = df_renamed[df_renamed["new_ids"].notna()]
        df_renamed = df_renamed.explode("new_ids")
        if max_len < df_renamed.index.nlevels:
            levels_to_unstack = df_renamed.index.names[max_len:df_renamed.index.nlevels]
            existing_levels = [level for level in df_renamed.index.names if level not in levels_to_unstack]
            df_renamed = df_renamed.reset_index()
            df_renamed = df_renamed.set_index(["new_ids"]+levels_to_unstack)
            df_renamed = df_renamed.drop(existing_levels,axis=1)
        else:
            df_renamed = df_renamed.set_index("new_ids")
        return df_renamed

    def set_available_technologies(self, finance: pd.DataFrame = None, efficiency: pd.DataFrame = None, lifetime: pd.DataFrame = None, construction_time: pd.DataFrame = None):
        """Set the available technologies for the data source."""
        if finance is not None:
            self.available_technologies_finance = finance.index.get_level_values("technology").unique().tolist()
        if efficiency is not None:
            self.available_technologies_efficiency = efficiency.index.get_level_values("technology").unique().tolist()
        if lifetime is not None:
            self.available_technologies_lifetime = lifetime.index.get_level_values("technology").unique().tolist()
        if construction_time is not None:
            self.available_technologies_construction_time = construction_time.index.get_level_values("technology").unique().tolist()

    
