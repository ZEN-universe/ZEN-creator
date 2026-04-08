from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.utils.attribute import Attribute

from .energy_system import EnergySystem


class TemplateEnergySystem(EnergySystem):
    """Template class for energy systems.

    This template is a starting point for implementing a custom energy system
    class. You must implement both methods below to provide `set_nodes` and
    `set_edges` for your model.

    Search for `TODO` markers to find sections that should be customized.
    """

    name: str = "template_energy_system"

    def __init__(self, model: Model):
        super().__init__(model=model)

    def _set_set_nodes(self) -> Attribute:
        """Return the set_nodes attribute.

        The attribute `set_nodes` must have a default value of `None`
        so that it does not get written to the `attributes.json` file
        for the energy system. The attribute data should contain
        a dataframe of nodes and their latitute and longitude coordinates.

        The `energy_system.set nodes` attribute defined in
        this function *should not* be used to get a list
        of nodes. Please use model.config.system.set_nodes instead. The node
        list in the configurations is always up to date, while the dataframe
        saved here my contain coordinates for additional nodes.

        TODO: Replace this placeholder with your node-loading logic.
        """
        return Attribute(name="set_nodes", default_value=None, element=self)

    def _set_set_edges(self) -> Attribute:
        """Return the set_edges attribute.

        Return the set_nodes attribute.

        The attribute `set_edges` must have a default value of `None`
        so that it does not get written to the `attributes.json` file
        for the energy system. The attribute data should contain
        a dataframe of edges names and their `to` and `from` nodes.

        TODO: Replace this placeholder with your edge-loading logic.
        """
        return Attribute(name="set_edges", default_value=None, element=self)
