from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.datasets.datasets import TemplateDataset
from zen_creator.datasets.datasets.metadata import MetaData, SourceInformation
from zen_creator.elements import TransportTechnology
from zen_creator.utils.attribute import Attribute


class TemplateTransportTechnology(TransportTechnology):
    """Template class for transport technologies.

    This template is designed as a starting point for users wishing to implement
    a new transport technology. Please read the docstrings and comments carefully
    for notes on how to use the template.

    All methods and properties that need to be implemented are marked with`TODO`
    comments. You can search for `TODO` in this file to quickly find all the
    places where you need to make changes.
    """

    name: str = "template_transport_technology"

    def __init__(self, model: Model, power_unit: str = "MW"):
        super().__init__(model=model, power_unit=power_unit)

    # ---------- Required methods that are called during object construction ----------

    def _set_reference_carrier(self) -> Attribute:
        """
        Return the reference carrier of the technology.

        This method is used to set the self.reference_carrier property when the
        technology is constructed.

        TODO: This method must be implemented. It should return an Attribute object
        containing the reference carrier of the technology.
        """
        return Attribute(name="reference_carrier", default_value=["heat"], element=self)

    # ---------- Required methods that are called during object build ----------

    def _set_lifetime(self) -> Attribute:
        """
        Return the lifetime of the technology.

        This method is used to set the self.lifetime property when the
        technology is built.

        TODO: This method must be implemented. It should return an Attribute object
        containing the lifetime of the technology.
        """

        attr = self._lifetime
        return attr.set_data(
            default_value=25,
            source=SourceInformation(
                description="Description of assumption.",
                metadata=MetaData(
                    name="datasource1",
                    title="Study of lifetime of template transport technology.",
                    author=["ZEN Creator"],
                    publication="ZEN Creator Journal",
                    publication_year=2026,
                    url="",
                ),
            ),
        )

    # ----Example of an optional method for creating an attribute using a dataset ------

    def _set_max_load(self) -> Attribute:
        """
        Return the max load of the technology.

        This method is used to set the self.max_load property when the
        technology is built.

        This method is an example of how to create an attribute using information from
        a dataset. It is not required for all technologies. Use this syntax
        when attributes need to be initialized with data from a dataset.

        Attributes should be returned directly from the dataset method
        "get_<attribute_name>" of the relevant dataset. In this example, we
        assume that the dataset has a method "get_max_load" which returns an
        Attribute object containing the max load of the technology.

        Data processing should be done directly in the dataset classes whenever
        possible, rather than in this method. The main purpose of this method
        is to provide an easily readable map that directs to the relevant
        datasets or datasetcollections.
        """

        attr = TemplateDataset(self.model.config.source_path).get_max_load(element=self)

        return attr
