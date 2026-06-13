from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator import Attribute, Carrier, CarrierConfig


class TemplateCarrierConfig(CarrierConfig):
    """
    Configuration class for the TemplateCarrier.

    This class is used to define the configuration parameters for the
    TemplateCarrier.

    By inheriting from CarrierConfig, these configurations
    are automatically included in the Config under
    Config().data.carrier.<carrier_name>.
    This requires the the class has been imported (i.e. registered) before
    the config is created.

    Note: All configurations must have default values. The name must match
    the name of the carrier class.
    """

    # TODO: state name of the carrier to which the config applies
    name: str = "template_carrier"

    # TODO: add any additional configuration parameters specific to
    # the carrier here
    carrier_setting_1: str = "default_value_1"
    carrier_setting_2: float = 0.8


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
