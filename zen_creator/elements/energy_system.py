from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.datasets.dataset_collections.edges import Edges
from zen_creator.datasets.datasets.nuts_shp import NUTSshp
from zen_creator.elements.element import Element
from zen_creator.utils.attribute import Attribute


class EnergySystem(Element):
    name = "energy_system"

    def __init__(self, model: Model):
        super().__init__(model=model)

        # copy attributes from superclass
        self._attribute_names = list(self._attribute_names)  # copy to prevent override

        # attributes which are added in this class
        self._subclass_attribute_names = [
            "price_carbon_emissions_annual_overshoot",
            "carbon_emissions_budget",
            "carbon_emissions_annual_limit",
            "price_carbon_emissions_budget_overshoot",
            "price_carbon_emissions",
            "carbon_emissions_cumulative_existing",
            "discount_rate",
            "knowledge_spillover_rate",
            "knowledge_depreciation_rate",
            "market_share_unbounded",
            "set_nodes",
            "set_edges",
        ]
        self._attribute_names.extend(self._subclass_attribute_names)

        # initialize all attributes to default values
        self.set_default_values_energy_system()

    # ---------- Initialization ----------
    def set_default_values_energy_system(self):
        """Initialize all attributes to their default values."""
        self._price_carbon_emissions_annual_overshoot = Attribute(
            "price_carbon_emissions_annual_overshoot",
            default_value=np.inf,
            unit="Euro/tons",
            source="assumption",
            element=self,
        )
        self._carbon_emissions_budget = Attribute(
            "carbon_emissions_budget",
            default_value=np.inf,
            unit="gigatons",
            source="assumption",
            element=self,
        )
        self._carbon_emissions_annual_limit = Attribute(
            "carbon_emissions_annual_limit",
            default_value=np.inf,
            unit="gigatons",
            source="assumption",
            element=self,
        )
        self._price_carbon_emissions_budget_overshoot = Attribute(
            "price_carbon_emissions_budget_overshoot",
            default_value=np.inf,
            unit="Euro/tons",
            source="assumption",
            element=self,
        )
        self._price_carbon_emissions = Attribute(
            "price_carbon_emissions", default_value=0, unit="Euro/tons", element=self
        )
        self._carbon_emissions_cumulative_existing = Attribute(
            "carbon_emissions_cumulative_existing",
            default_value=0,
            unit="gigatons",
            element=self,
        )
        self._discount_rate = Attribute(
            "discount_rate",
            default_value=0.05,
            unit="1",
            source="https://iopscience.iop.org/article/10.1088/1748-9326/ac228a",
            element=self,
        )
        self._knowledge_spillover_rate = Attribute(
            "knowledge_spillover_rate",
            default_value=np.inf,
            unit="1",
            source="assumption",
            element=self,
        )
        self._knowledge_depreciation_rate = Attribute(
            "knowledge_depreciation_rate",
            default_value=0.1,
            unit="1",
            source=(
                "1. Leibowicz, B. D., Krey, V. & Grubler, A. "
                "Representing spatial technology diffusion in an energy system "
                "optimization model. "
                "Technological Forecasting and Social Change 103 (2016)."
            ),
            element=self,
        )
        self._market_share_unbounded = Attribute(
            "market_share_unbounded",
            default_value=0.02,
            unit="1",
            source=(
                "1. Mannhardt, J., Gabrielli, P. & Sansavini, G. "
                "Understanding the vicious cycle of myopic foresight and "
                "constrained technology deployment in transforming the "
                "European energy system. iScience 27, (2024)."
            ),
            element=self,
        )
        self.set_nodes = Attribute(
            "set_nodes",
            default_value=None,
            element=self,
        )
        self.set_edges = Attribute(
            "set_edges",
            default_value=None,
            element=self,
        )

    # ---------- Properties ----------
    @property
    def price_carbon_emissions_annual_overshoot(self) -> Attribute:
        return self._price_carbon_emissions_annual_overshoot

    @price_carbon_emissions_annual_overshoot.setter
    def price_carbon_emissions_annual_overshoot(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._price_carbon_emissions_annual_overshoot = value

    @property
    def carbon_emissions_budget(self) -> Attribute:
        return self._carbon_emissions_budget

    @carbon_emissions_budget.setter
    def carbon_emissions_budget(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._carbon_emissions_budget = value

    @property
    def carbon_emissions_annual_limit(self) -> Attribute:
        return self._carbon_emissions_annual_limit

    @carbon_emissions_annual_limit.setter
    def carbon_emissions_annual_limit(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._carbon_emissions_annual_limit = value

    @property
    def price_carbon_emissions_budget_overshoot(self) -> Attribute:
        return self._price_carbon_emissions_budget_overshoot

    @price_carbon_emissions_budget_overshoot.setter
    def price_carbon_emissions_budget_overshoot(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._price_carbon_emissions_budget_overshoot = value

    @property
    def price_carbon_emissions(self) -> Attribute:
        return self._price_carbon_emissions

    @price_carbon_emissions.setter
    def price_carbon_emissions(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._price_carbon_emissions = value

    @property
    def carbon_emissions_cumulative_existing(self) -> Attribute:
        return self._carbon_emissions_cumulative_existing

    @carbon_emissions_cumulative_existing.setter
    def carbon_emissions_cumulative_existing(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._carbon_emissions_cumulative_existing = value

    @property
    def discount_rate(self) -> Attribute:
        return self._discount_rate

    @discount_rate.setter
    def discount_rate(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._discount_rate = value

    @property
    def knowledge_spillover_rate(self) -> Attribute:
        return self._knowledge_spillover_rate

    @knowledge_spillover_rate.setter
    def knowledge_spillover_rate(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._knowledge_spillover_rate = value

    @property
    def knowledge_depreciation_rate(self) -> Attribute:
        return self._knowledge_depreciation_rate

    @knowledge_depreciation_rate.setter
    def knowledge_depreciation_rate(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._knowledge_depreciation_rate = value

    @property
    def market_share_unbounded(self) -> Attribute:
        return self._market_share_unbounded

    @market_share_unbounded.setter
    def market_share_unbounded(self, value: Attribute) -> None:
        self._validate_attribute(value)
        self._market_share_unbounded = value

    @property
    def set_nodes(self) -> Attribute:
        return self._set_nodes

    @set_nodes.setter
    def set_nodes(self, value: Attribute) -> None:
        self._validate_attribute(value)
        if value.default_value:
            raise ValueError(
                "The attribute 'set_nodes' must not have"
                "a default value. Please set the default value to `[]` and "
                "enter the nodes and coordinates as a `df`."
            )
        self._set_nodes = value

    @property
    def set_edges(self) -> Attribute:
        return self._set_edges

    @set_edges.setter
    def set_edges(self, value: Attribute) -> None:
        self._validate_attribute(value)
        if value.default_value:
            raise ValueError(
                "The attribute 'set_nodes' must not have"
                "a default value. Please set the default value to `[]` and "
                "enter the nodes and coordinates as a `df`."
            )
        self._set_edges = value

    # ---------- Methods ----------

    def _set_set_nodes(self) -> Attribute:
        attr = NUTSshp(source_path=self.source_path).get_set_nodes(self)
        return attr

    def _set_set_edges(self) -> Attribute:
        attr = Edges(source_path=self.source_path).get_set_edges(self)

        # manual connections NO-BE and NO-FR for gas, and SE-LT for electricity
        set_edges = attr.df
        set_edges.loc["NO-FR", :] = ["NO", "FR"]
        set_edges.loc["FR-NO", :] = ["FR", "NO"]
        set_edges.loc["NO-BE", :] = ["NO", "BE"]
        set_edges.loc["BE-NO", :] = ["BE", "NO"]
        set_edges.loc["SE-LT", :] = ["SE", "LT"]
        set_edges.loc["LT-SE", :] = ["LT", "SE"]
        attr.set_data(df=set_edges.drop_duplicates().sort_index())

        # write csv
        return attr
