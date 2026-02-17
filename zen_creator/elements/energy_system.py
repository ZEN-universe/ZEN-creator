from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.element import Element
from zen_creator.utils.attribute import Attribute
from zen_creator.utils.system_file import SystemFile
from functools import cached_property
import numpy as np
import pandas as pd
import geopandas as gpd
import copy


class EnergySystem(Element):
    name = "energy_system"

    def __init__(self, model: Model):
        super().__init__(name="energy_system", model=model)

        # create energy system description
        self.create_nodes()
        self.create_edges()

        # create system file
        self.system_file = SystemFile(model=model)

    # ---------- Attributes ----------
    @cached_property
    def price_carbon_emissions_annual_overshoot(self) -> Attribute:
        return Attribute(
            "price_carbon_emissions_annual_overshoot",
            default_value=5000,
            unit="Euro/tons",
            source="assumption",
            element=self,
        )

    @cached_property
    def carbon_emissions_budget(self) -> Attribute:
        return Attribute(
            "carbon_emissions_budget",
            default_value=23.152036605496253,
            unit="gigatons",
            source="IEA World Energy Outlook 2021",
            element=self,
        )

    @cached_property
    def carbon_emissions_annual_limit(self) -> Attribute:
        return Attribute(
            "carbon_emissions_annual_limit",
            default_value=np.inf,
            unit="gigatons",
            element=self,
        )

    @cached_property
    def price_carbon_emissions_budget_overshoot(self) -> Attribute:
        return Attribute(
            "price_carbon_emissions_budget_overshoot",
            default_value=5000,
            unit="Euro/tons",
            source="assumption",
            element=self,
        )

    @cached_property
    def price_carbon_emissions(self) -> Attribute:
        return Attribute(
            "price_carbon_emissions", default_value=0, unit="Euro/tons", element=self
        )

    @cached_property
    def carbon_emissions_cumulative_existing(self) -> Attribute:
        return Attribute(
            "carbon_emissions_cumulative_existing",
            default_value=0,
            unit="gigatons",
            element=self,
        )

    @cached_property
    def discount_rate(self) -> Attribute:
        return Attribute(
            "discount_rate",
            default_value=0.05,
            unit="1",
            source="https://iopscience.iop.org/article/10.1088/1748-9326/ac228a",
            element=self,
        )

    @cached_property
    def knowledge_spillover_rate(self) -> Attribute:
        return Attribute(
            "knowledge_spillover_rate", default_value=np.inf, unit="1", element=self
        )

    @cached_property
    def knowledge_depreciation_rate(self) -> Attribute:
        return Attribute(
            "knowledge_depreciation_rate",
            default_value=0.1,
            unit="1",
            source=(
                "1. Leibowicz, B. D., Krey, V. & Grubler, A. "
                "Representing spatial technology diffusion in an energy system optimization model. "
                "Technological Forecasting and Social Change 103 (2016)."
            ),
            element=self,
        )

    @cached_property
    def market_share_unbounded(self) -> Attribute:
        return Attribute(
            "market_share_unbounded",
            default_value=0.02,
            unit="1",
            source=(
                "1. Mannhardt, J., Gabrielli, P. & Sansavini, G. "
                "Understanding the vicious cycle of myopic foresight and constrained technology deployment in transforming the European energy system. "
                "iScience 27, (2024)."
            ),
            element=self,
        )

    # ---------- Methods ----------

    def create_nodes(self):
        set_nodes = [
            "AT",
            "BE",
            "BG",
            "CH",
            "CZ",
            "DE",
            "DK",
            "EE",
            "EL",
            "ES",
            "FI",
            "FR",
            "HR",
            "HU",
            "IE",
            "IT",
            "LT",
            "LU",
            "LV",
            "NL",
            "NO",
            "PL",
            "PT",
            "RO",
            "SE",
            "SI",
            "SK",
            "UK",
        ]
        centroids = pd.read_csv(
            self.source_path
            / "01-energy_system"
            / "nodes_edges"
            / "countries_centroids.csv"
        ).set_index("ISO")
        centroids = centroids.rename({"GR": "EL", "GB": "UK"}, axis=0).sort_index()
        centroids = centroids[
            centroids["COUNTRY"] != "Canarias"
        ]  # kick out canarias that also has ES as code
        centroids = centroids.loc[set_nodes, ["longitude", "latitude"]].rename(
            {"longitude": "lon", "latitude": "lat"}, axis=1
        )
        centroids.index.name = "node"
        centroids.to_csv(self.output_path / "set_nodes.csv")
        centroids = centroids.reset_index()
        self.set_nodes = centroids

    def create_edges(self):
        connectivity_matrix = pd.DataFrame(
            index=self.set_nodes["node"], columns=self.set_nodes["node"], data=0
        )
        # from shapefile
        gdf = gpd.read_file(
            self.source_path
            / "01-energy_system"
            / "nodes_edges"
            / "NUTS_RG_60M_2021_3035.shp"
        )
        countries = gdf[gdf["NUTS_ID"].isin(self.set_nodes["node"])]
        for index, row in countries.iterrows():
            neighbors = countries[countries.geometry.touches(row["geometry"])][
                "NUTS_ID"
            ]
            connectivity_matrix.loc[row["NUTS_ID"], neighbors] = 1
        connectivity_matrix = connectivity_matrix.stack()
        nodes_in_edges = connectivity_matrix[connectivity_matrix == 1].to_frame()
        nodes_in_edges["edge"] = nodes_in_edges.index.map(lambda idx: "-".join(idx))
        nodes_in_edges.index.names = ["node_from", "node_to"]
        set_edges = nodes_in_edges.drop(columns=0)
        set_edges_touching = set_edges.reset_index().set_index("edge")
        # nodes from ENTSOE TYNDP 2020-scenario.xlsx
        # load nodes and edges
        additional_set_edges = pd.DataFrame(columns=["node_from", "node_to"])
        nodes = pd.read_csv(
            self.source_path / "01-energy_system" / "nodes_edges" / "Nodes_Dict.csv",
            delimiter=";",
        )
        edges = pd.read_csv(
            self.source_path / "01-energy_system" / "nodes_edges" / "Lines_Dict.csv",
            delimiter=";",
        )
        edges = edges[~edges["line_id"].str.contains("Exp")]
        # iterate through nodes to find corresponding edges
        set_nodes = copy.deepcopy(self.set_nodes["node"])
        set_nodes[set_nodes == "EL"] = "GR"
        for node in set_nodes:
            node_ids = nodes["node_id"][nodes["country"] == node].reset_index(drop=True)
            connected_node_id_from_node = []
            connected_node_id_to_node = []
            for node_id in node_ids:
                connected_node_id_from_node.extend(
                    list(edges["node_b"][(edges["node_a"] == node_id)])
                )
                connected_node_id_to_node.extend(
                    list(edges["node_a"][(edges["node_b"] == node_id)])
                )
            # append to set_edges
            set_edges_temp_from_node = pd.DataFrame(columns=["node_from", "node_to"])
            connected_node_from_node = nodes["country"][
                nodes["node_id"].apply(lambda n: n in connected_node_id_from_node)
            ]
            # only nodes which are in self.set_nodes
            set_edges_temp_from_node["node_to"] = connected_node_from_node[
                connected_node_from_node.isin(set_nodes)
            ]
            set_edges_temp_from_node["node_from"] = node
            set_edges_temp_to_node = pd.DataFrame(columns=["node_from", "node_to"])
            connected_node_to_node = nodes["country"][
                nodes["node_id"].apply(lambda n: n in connected_node_id_to_node)
            ]
            # only nodes which are in self.set_nodes
            set_edges_temp_to_node["node_from"] = connected_node_to_node[
                connected_node_to_node.isin(set_nodes)
            ]
            set_edges_temp_to_node["node_to"] = node
            additional_set_edges = pd.concat(
                [additional_set_edges, set_edges_temp_from_node, set_edges_temp_to_node]
            )
        # remove edges where node_from = node_to
        additional_set_edges = additional_set_edges[
            additional_set_edges["node_from"] != additional_set_edges["node_to"]
        ]
        # manual connections NO-BE and NO-FR for gas, and SE-LT for electricity
        manual_additional_edges = pd.DataFrame(
            data=[["NO", "FR"], ["NO", "BE"], ["SE", "LT"]],
            columns=["node_from", "node_to"],
        )
        additional_set_edges = pd.concat(
            [additional_set_edges, manual_additional_edges]
        )
        # flip direction of edge
        additional_set_edges_flipped = additional_set_edges.rename(
            columns={"node_from": "node_to", "node_to": "node_from"}
        )
        additional_set_edges = pd.concat(
            [additional_set_edges, additional_set_edges_flipped]
        ).drop_duplicates()
        # substitute greece
        additional_set_edges[additional_set_edges == "GR"] = "EL"
        # set edge name
        additional_set_edges["edge"] = additional_set_edges.apply(
            lambda row: row["node_from"] + "-" + row["node_to"], axis=1
        )
        additional_set_edges = additional_set_edges.set_index("edge")
        additional_set_edges = additional_set_edges.loc[
            additional_set_edges.index.difference(set_edges_touching.index)
        ]
        set_edges = pd.concat([set_edges_touching, additional_set_edges])
        self.set_edges = set_edges.sort_index()
        self.set_edges_offshore = additional_set_edges.sort_index()
        # write csv
        self.set_edges.to_csv(self.output_path / "set_edges.csv")
