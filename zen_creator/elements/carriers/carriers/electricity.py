from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.carriers.carrier import Carrier
from zen_creator.utils.attribute import Attribute
from zen_creator.datasets.dataset_collections.dataset_collection_electricity import DatasetCollectionElectricity
class Electricity(Carrier):
    def __init__(self, model: Model):
        super().__init__(name="electricity", model=model)

    # def _set_demand(self) -> Attribute:
    #     attr = super().demand
    #     demand = DatasetCollectionElectricity(self.model.source_path).get_demand()
    #     return attr.set_data(df=demand,unit="GW", source="ENTSOE Transparency Platform")
    
        
        