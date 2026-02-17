from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.element import Element
from zen_creator.utils.attribute import Attribute

from abc import ABC
import numpy as np


class TransportTechnology(Element, ABC):
    subpath = "set_transport_technologies"
    name = "transport_technology"

    def __init__(self, name: str, model: Model, power_unit: str = "MW"):
        super().__init__(name, model, power_unit=power_unit)

        # copy attributes from superclass
        self._attribute_names = list(self._attribute_names)  # copy to prevent override

        # attributes which are added in this class
        self._subclass_attribute_names = [
            "transport_loss_factor_linear",
            "capex_per_distance_transport",
            "distance",
        ]
        self._attribute_names.extend(self._subclass_attribute_names)

        # initialize all attributes to default values
        self.set_default_values_transport_technology()

    def set_default_values_transport_technology(self):
        """Initialize internal attributes to default values."""
        self._transport_loss_factor_linear = Attribute(
            "transport_loss_factor_linear",
            default_value=0.0,
            unit="1/km",
            element=self,
        )
        self._capex_per_distance_transport = Attribute(
            "capex_per_distance_transport",
            default_value=0.0,
            unit=f"Euro/({self.power_unit})/km",
            element=self,
        )
        self._distance = Attribute(
            "distance", default_value=np.inf, unit="km", element=self
        )

    # ---------- Properties ----------

    @property
    def transport_loss_factor_linear(self) -> Attribute:
        return self._transport_loss_factor_linear

    @transport_loss_factor_linear.setter
    def transport_loss_factor_linear(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._transport_loss_factor_linear = value

    @property
    def capex_per_distance_transport(self) -> Attribute:
        return self._capex_per_distance_transport

    @capex_per_distance_transport.setter
    def capex_per_distance_transport(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._capex_per_distance_transport = value

    @property
    def distance(self) -> Attribute:
        return self._distance

    @distance.setter
    def distance(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._distance = value
