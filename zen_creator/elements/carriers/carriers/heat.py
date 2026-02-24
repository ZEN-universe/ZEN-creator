from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.carriers.carrier import Carrier
from zen_creator.utils.attribute import Attribute
from zen_creator.datasets.dataset_collections.dataset_collection_heat import DatasetCollectionHeat
import pandas as pd

class Heat(Carrier):
    
    def __init__(self, model: Model):
        super().__init__(name = "heat", model=model)

    # def _set_demand(self) -> Attribute:
    #     attr = super().demand
    #     demand_data = DatasetCollectionHeat(self.model.source_path).get_demand()
    #     return attr.set_data(df=demand_data,unit="GW", source="EU Building Observatory and When2Heat Dataset")
    
    