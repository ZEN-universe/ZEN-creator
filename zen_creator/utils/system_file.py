from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zen_creator.model import Model

import json

from zen_creator.utils.attribute import SystemAttribute


class SystemFile:
    def __init__(self, model: Model):
        self.model = model
        self.name = "system"
        self.output_path = model.output_path  # save in the main output folder

        # attributes which are added in this class
        self._attribute_names = [
            "set_conversion_technologies",
            "set_storage_technologies",
            "set_transport_technologies",
            "set_retrofitting_technologies",
            "set_nodes",
            "reference_year",
            "optimized_years",
            "interval_between_years",
            "aggregated_time_steps_per_year",
            "conduct_time_series_aggregation",
            "use_rolling_horizon",
            "years_in_rolling_horizon",
            "years_in_decision_horizon",
            "conduct_scenario_analysis",
        ]

    # ---------- Properties ----------
    @property
    def set_conversion_technologies(self) -> SystemAttribute:

        set_conversion_technologies = set(self.model.conversion_technologies.keys())
        set_retrofitting_technologies = set(self.model.retrofitting_technologies.keys())
        attr = SystemAttribute(
            "set_conversion_technologies",
            value=sorted(
                list(
                    set_conversion_technologies.difference(
                        set_retrofitting_technologies
                    )
                )
            ),
            default_value=[],
            element=self,
        )
        return attr

    @property
    def set_storage_technologies(self) -> SystemAttribute:
        return SystemAttribute(
            "set_storage_technologies",
            value=sorted(list(self.model.storage_technologies.keys())),
            default_value=[],
            element=self,
        )

    @property
    def set_transport_technologies(self) -> SystemAttribute:
        return SystemAttribute(
            "set_transport_technologies",
            value=sorted(list(self.model.transport_technologies.keys())),
            default_value=[],
            element=self,
        )

    @property
    def set_retrofitting_technologies(self) -> SystemAttribute:
        return SystemAttribute(
            "set_retrofitting_technologies",
            value=sorted(list(self.model.retrofitting_technologies.keys())),
            default_value=[],
            element=self,
        )

    @property
    def set_nodes(self) -> SystemAttribute:
        return SystemAttribute(
            "set_nodes",
            value=sorted(self.model.energy_system.set_nodes.df.index.to_list()),
            default_value=[],
            element=self,
        )

    @property
    def reference_year(self) -> SystemAttribute:
        return SystemAttribute(
            "reference_year",
            value=self.model.config.time_settings.reference_year,
            element=self,
        )

    @property
    def optimized_years(self) -> SystemAttribute:
        return SystemAttribute(
            "optimized_years",
            value=self.model.config.time_settings.optimized_years,
            element=self,
        )

    @property
    def interval_between_years(self) -> SystemAttribute:
        return SystemAttribute(
            "interval_between_years",
            value=self.model.config.time_settings.interval_between_years,
            element=self,
        )

    @property
    def aggregated_time_steps_per_year(self) -> SystemAttribute:
        return SystemAttribute(
            "aggregated_time_steps_per_year",
            value=self.model.config.time_settings.aggregated_time_steps_per_year,
            element=self,
        )

    @property
    def conduct_time_series_aggregation(self) -> SystemAttribute:
        return SystemAttribute(
            "conduct_time_series_aggregation",
            value=self.model.config.time_settings.conduct_time_series_aggregation,
            default_value=False,
            element=self,
        )

    @property
    def use_rolling_horizon(self) -> SystemAttribute:
        return SystemAttribute(
            "use_rolling_horizon",
            value=self.model.config.time_settings.use_rolling_horizon,
            default_value=False,
            element=self,
        )

    @property
    def years_in_rolling_horizon(self) -> SystemAttribute:
        return SystemAttribute(
            "years_in_rolling_horizon",
            value=self.model.config.time_settings.years_in_rolling_horizon,
            default_value=1,
            element=self,
        )

    @property
    def years_in_decision_horizon(self) -> SystemAttribute:
        return SystemAttribute(
            "years_in_decision_horizon",
            value=self.model.config.time_settings.years_in_decision_horizon,
            default_value=1,
            element=self,
        )

    @property
    def conduct_scenario_analysis(self) -> SystemAttribute:
        return SystemAttribute(
            "conduct_scenario_analysis",
            value=self.model.config.sensitivity_settings.conduct_scenario_analysis,
            default_value=False,
            element=self,
        )

    # ---------- Methods ----------
    def attributes_to_dict(self) -> dict:
        """Convert all attributes to a dictionary, excluding defaults."""
        output = {}
        for attr_name in self._attribute_names:
            attr = getattr(self, attr_name)
            value = attr.value
            default_value = attr.default_value
            if value != default_value:
                output[attr_name] = value
        return output

    def write(self):
        """Save system attributes to JSON file."""
        output = self.attributes_to_dict()
        with open(self.output_path / "system.json", "w") as f:
            json.dump(output, f, indent=4)
