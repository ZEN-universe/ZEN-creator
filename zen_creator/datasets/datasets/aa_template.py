from dataclasses import dataclass
import pandas as pd
from typing import Optional
from zen_creator.datasets.dataset import Dataset
from zen_creator.utils.attribute import Attribute
from zen_creator.elements.element import Element
from zen_creator.utils.default_config import Config
from pathlib import Path

class Template(Dataset):
    def __init__(self, path: str, config: Optional[Config] = None):
        name = "template"
        super().__init__(name=name, config=config)

    def _get_author(self) -> str:
        return "Jane Doe"

    def _get_publication_year(self) -> int:
        return 2026

    def _get_url(self) -> str:
        return "https://example.com/dataset.csv"
    
    def _get_path(self) -> Path:
        return Path(".")

    def _get_data(self) -> pd.DataFrame:
        return pd.read_csv(self.path)

    # -------- methods ------------------------

    def get_max_load(self, element: Element, **kwargs) -> Attribute:
        """
        Function for creating max_load attribute.

        Functions for other attributes should follow the same naming 
        convention i.e. get_<attribute_name>. 

        This function uses information from self.data and returns an object
        of class Attribute. Any internal functions which are called by this 
        function should begin with an underscore to clearly mark them as
        internal.
        """
        attr = Attribute("max_load", element)
        data = self.data #use the dataset property to access the dataset
        unit = self._max_load_unit()
        attr.set_data(default_value= data, df = data, unit = unit)
        return attr
    
    def _max_load_unit():
        return "MW"