from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Dict, Generic, Optional, TypeVar, Union

if TYPE_CHECKING:
    from pathlib import Path

from pathlib import Path

import pandas as pd

from ..datasets.dataset import Dataset

T = TypeVar("T", bound=Union[pd.DataFrame, Dict[str, pd.DataFrame]])


class TechnoEconomicDataset(Dataset[T], Generic[T]):
    """Dataset class for techno-economic source data."""

    name = "techno_economic_dataset"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)

        self.available_technologies_finance: list[str] = []
        self.available_technologies_efficiency: list[str] = []
        self.available_technologies_lifetime: list[str] = []
        self.available_technologies_construction_time: list[str] = []

    @property
    @abstractmethod
    def money_year_source(self) -> int:
        pass

    @property
    @abstractmethod
    def unit(self) -> str:
        pass

    @abstractmethod
    def get_cost_data(
        self, technology: str, variable: str, target_year: int
    ) -> pd.DataFrame:
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
        return list(range(start_year, end_year + 1))

    @staticmethod
    def get_units(unit, is_ccs=False):
        """returns money, energy and power unit."""
        if is_ccs:
            units = {"money": "Euro", "energy": "tCO2", "power": "tCO2/hour"}
        else:
            units = {"money": "Euro", "energy": "kWh", "power": "kW"}
        return units[unit]

    def rename_index(
        self,
        df: pd.DataFrame | pd.Series,
        rename_map: dict[str, str | tuple[str, ...]],
    ) -> pd.DataFrame:
        """
        Rename dataframe index according to a mapping using a vectorized approach.

        Supports:
            old_id -> new_id
            old_id -> (new_id1, new_id2, ...)

        Rows are duplicated if multiple new IDs are assigned.
        """

        import pandas as pd

        # Ensure DataFrame
        if isinstance(df, pd.Series):
            df = df.to_frame()
        df = df.copy()

        # -----------------------------
        # Normalize rename_map: flatten tuples
        # -----------------------------
        records = []
        for old_id, new_ids in rename_map.items():
            if not isinstance(new_ids, tuple):
                new_ids = (new_ids,)
            for new_id in new_ids:
                records.append((old_id, new_id))

        mapping_df = pd.DataFrame(records, columns=["old_id", "new_id"])

        # -----------------------------
        # Merge with the dataframe index
        # -----------------------------
        df = df.reset_index()
        df = df.merge(mapping_df, left_on=df.columns[0], right_on="old_id", how="inner")

        # -----------------------------
        # Handle multiple new_ids per row
        # -----------------------------
        df = df.drop(columns=["old_id"])
        df = df.set_index("new_id")

        return df

    def set_available_technologies(
        self,
        finance: Optional[pd.DataFrame] = None,
        efficiency: Optional[pd.DataFrame] = None,
        lifetime: Optional[pd.DataFrame] = None,
        construction_time: Optional[pd.DataFrame] = None,
    ):
        """Set the available technologies for the data source."""
        if finance is not None:
            self.available_technologies_finance = (
                finance.index.get_level_values("technology").unique().tolist()
            )
        if efficiency is not None:
            self.available_technologies_efficiency = (
                efficiency.index.get_level_values("technology").unique().tolist()
            )
        if lifetime is not None:
            self.available_technologies_lifetime = (
                lifetime.index.get_level_values("technology").unique().tolist()
            )
        if construction_time is not None:
            self.available_technologies_construction_time = (
                construction_time.index.get_level_values("technology").unique().tolist()
            )
