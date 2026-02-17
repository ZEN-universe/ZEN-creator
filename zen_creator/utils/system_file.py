from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from zen_creator.model import Model

from zen_creator.elements.technologies.conversion_technology import ConversionTechnology
from zen_creator.elements.technologies.storage_technology import StorageTechnology
from zen_creator.elements.technologies.transport_technology import TransportTechnology
from zen_creator.elements.technologies.retrofitting_technology import RetrofittingTechnology
from zen_creator.utils.attribute import SystemAttribute


from functools import cached_property
import os
import inspect
import json

class SystemFile:
    def __init__(self, model: Model):
        self.model = model
        self.name = "system"
        self.folder_path = model.out_path  # save in the main output folder
        
    # ---------- System File Attributes ----------
    @cached_property
    def set_conversion_technologies(self) -> list:
        set_conversion_technologies = set(ConversionTechnology.get_all().keys())
        set_retrofitting_technologies = set(RetrofittingTechnology.get_all().keys())
        return SystemAttribute("set_conversion_technologies", value=sorted(list(set_conversion_technologies.difference(set_retrofitting_technologies))), default_value=[],element=self)
    
    @cached_property
    def set_storage_technologies(self) -> list:
        return SystemAttribute("set_storage_technologies", value=sorted(list(StorageTechnology.get_all().keys())), default_value=[],element=self)
    @cached_property
    def set_transport_technologies(self) -> list:
        return SystemAttribute("set_transport_technologies", value=sorted(list(TransportTechnology.get_all().keys())), default_value=[],element=self)
    
    @cached_property
    def set_retrofitting_technologies(self) -> list:
        return SystemAttribute("set_retrofitting_technologies", value=sorted(list(RetrofittingTechnology.get_all().keys())), default_value=[],element=self)
    
    @cached_property
    def set_nodes(self) -> list:
        return SystemAttribute("set_nodes", value=sorted(self.model.energy_system.set_nodes["node"].to_list()), default_value=[],element=self)
    @cached_property
    def reference_year(self) -> int:
        return SystemAttribute("reference_year", value=self.model.config.time_settings.reference_year, element=self)
    
    @cached_property
    def optimized_years(self) -> int:
        return SystemAttribute("optimized_years", value=self.model.config.time_settings.optimized_years, element=self)
    
    @cached_property
    def interval_between_years(self) -> int:
        return SystemAttribute("interval_between_years", value=self.model.config.time_settings.interval_between_years, element=self)
    
    @cached_property
    def aggregated_time_steps_per_year(self) -> int:
        return SystemAttribute("aggregated_time_steps_per_year", value=self.model.config.time_settings.aggregated_time_steps_per_year, element=self)
    
    @cached_property
    def conduct_time_series_aggregation(self) -> bool:
        return SystemAttribute("conduct_time_series_aggregation", value=self.model.config.time_settings.conduct_time_series_aggregation, default_value=False, element=self)
    
    @cached_property
    def use_rolling_horizon(self) -> bool:
        return SystemAttribute("use_rolling_horizon", value=self.model.config.time_settings.use_rolling_horizon, default_value=False, element=self)
    
    @cached_property
    def years_in_rolling_horizon(self) -> int:
        return SystemAttribute("years_in_rolling_horizon", value=self.model.config.time_settings.years_in_rolling_horizon, default_value=1, element=self)
    @cached_property
    def years_in_decision_horizon(self) -> int:
        return SystemAttribute("years_in_decision_horizon", value=self.model.config.time_settings.years_in_decision_horizon, default_value=1, element=self)
    
    @cached_property
    def conduct_scenario_analysis(self) -> bool:
        return SystemAttribute("conduct_scenario_analysis", value=self.model.config.sensitivity_settings.conduct_scenario_analysis, default_value=False, element=self)
    
    # ---------- Methods ----------
    def attributes_to_dict(self) -> dict:
        output = {}
        for attr_name in inspect.getmembers(self.__class__, lambda a: isinstance(a, cached_property)):
            attr = getattr(self, attr_name[0])
            value = attr.value
            default_value = attr.default_value
            if value != default_value:
                output[attr_name[0]] = value
        return output
    
    def save_system_file(self):
        output = self.attributes_to_dict()
        with open(os.path.join(self.folder_path, 'system.json'), 'w') as f:
            json.dump(output, f, indent=4)