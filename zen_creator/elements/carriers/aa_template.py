from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements import Carrier
from zen_creator.utils.attribute import Attribute


class TemplateCarrier(Carrier):
    """Template class for carriers.

    This template is designed as a starting point for users wishing to implement
    a new carrier. Please read the docstrings and comments carefully for notes
    on how to use the template.

    Carrier objects inherit many default attributes from the base Carrier class,
    so methods below are examples showing how to override defaults when needed.

    All methods and properties that need to be implemented are marked with`TODO`
    comments. You can search for `TODO` in this file to quickly find all the
    places where you need to make changes.
    """

    name: str = "template_carrier"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    # ----Example of optional methods for overriding default attributes ------

    def _set_demand(self) -> Attribute:
        """
        Return the demand of the carrier.

        This method is used to set the self.demand property when the
        model is built. It is optional to implement this method if the
        default value of 0 is suitable for all time steps.
        """
        attr = self.demand
        return attr

    def _set_price_shed_demand(self) -> Attribute:
        """
        Return the price for unmet demand of the carrier.

        This method is used to set the self.price_shed_demand property when the
        model is built.

        It is optional to implement this method if the default value of "inf"
        is suitable for all time steps.
        """
        attr = self.price_shed_demand
        return attr
