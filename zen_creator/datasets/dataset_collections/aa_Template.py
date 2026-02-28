from __future__ import annotations

from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from pathlib import Path

    from zen_creator.datasets.dataset import Dataset
    from zen_creator.elements.element import Element

from zen_creator.datasets.dataset_collection import DatasetCollection
from zen_creator.datasets.datasets.DIW import DIW
from zen_creator.datasets.datasets.potencia import Potencia
from zen_creator.utils.attribute import Attribute


class Template(DatasetCollection):
    """Template class for dataset collections."""

    name = "template"

    def __init__(self, source_path: Path | str):
        super().__init__(source_path=source_path)

    def _get_data(self) -> Dict[str, Dataset]:
        """Load all available data sources."""

        return {
            "DIW Berlin": DIW(self.source_path),
            "potencia": Potencia(self.source_path),
        }

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
        data = self.data["DIW Berlin"]  # use the dataset property to access the dataset
        unit = self._max_load_unit()
        attr.set_data(default_value=0, df=data, unit=unit)
        return attr

    def _max_load_unit(self):
        return "MW"
