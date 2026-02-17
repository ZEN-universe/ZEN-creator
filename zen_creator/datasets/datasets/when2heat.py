from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.datasets.dataset import Dataset
import pandas as pd

class When2Heat(Dataset):
    """Dataset class for When2Heat data."""

    def __init__(self, model: Model):
        super().__init__(name="when2heat", model=model)

    # ------ Metadata properties ------
    @property
    def author(self) -> str:
        return "When2Heat"
    
    @property
    def publication_year(self) -> int:
        return 2023
    
    @property
    def url(self) -> str:
        return "https://data.open-power-system-data.org/when2heat/"
    
    # ----- Methods to get data -----
    def load_heat_demand_profiles(self) -> pd.DataFrame:
        w2h = pd.read_csv(self.model.source_path / "02-carrier" / "heat" / "when2heat_heatRatio.csv")
        return w2h