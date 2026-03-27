################################
ZEN-Creator Class Diagram
################################

Overview
--------

.. mermaid::
   :zoom:

   classDiagram
       class Model {
           +name: str
           +config: Config
           +elements: dict[str, Element]
           +source_path: Path <<property>>
           +output_folder: Path <<property>>
           +output_path: Path <<property>>
           +energy_system: EnergySystem <<property>>
           +carriers: dict <<property>>
           +technologies: dict <<property>>
           +storage_technologies: dict <<property>>
           +conversion_technologies: dict <<property>>
           +transport_technologies: dict <<property>>
           +retrofitting_technologies: dict <<property>>
           +from_config() Model <<constructor>>
           +from_existing() Model <<constructor>>
           +add_sector_by_name() None
           +add_sector() None
           +remove_sector() None
           +add_element_by_name() None
           +add_element() None
           +remove_element() None
           +remove_element_by_name() None
           +build() None
           +validate() None
           +write() None
           +write_system_file() None
       }

       class Sector {
           +name: str <<class attribute>>
           +elements: list <<property>>
       }

       class Element {
       }

       class DatasetCollection {
       }

       class Dataset {
       }

       class Config {
       }

       class EnergySystem {
           +price_carbon_emissions_annual_overshoot: Attribute <<property>>
           +carbon_emissions_budget: Attribute <<property>>
           +carbon_emissions_annual_limit: Attribute <<property>>
           +price_carbon_emissions_budget_overshoot: Attribute <<property>>
           +price_carbon_emissions: Attribute <<property>>
           +carbon_emissions_cumulative_existing: Attribute <<property>>
           +discount_rate: Attribute <<property>>
           +knowledge_spillover_rate: Attribute <<property>>
           +knowledge_depreciation_rate: Attribute <<property>>
           +market_share_unbounded: Attribute <<property>>
           +set_nodes: Attribute <<property>>
           +set_edges: Attribute <<property>>
           +set_default_values_energy_system() None
           +write() None
       }

       class Attribute {
           +name: str
           +element: Element
           +default_value <<property>>
           +base_technology <<property>>
           +unit <<property>>
           +df <<property>>
           +yearly_variations_df <<property>>
           +source <<property>>
           +set_data() Attribute
           +overwrite_from_existing_model() None
           +default_to_dict() dict
           +save_data() None
       }

       <<abstract>> Sector
       <<abstract>> Dataset
       <<abstract>> Element
       <<abstract>> DatasetCollection

       DatasetCollection o-- Dataset
       Model --> Sector
       Model --> Element
       Model --> EnergySystem
       Model --> Config
       Element --> Attribute
       EnergySystem --> Attribute
       Dataset ..> Attribute
       DatasetCollection ..> Dataset
       Sector o-- Element


Subclasses of Elements
----------------------

.. mermaid::
   :zoom:

   classDiagram
       class Element {
           +subpath: str <<class variable>>
           +name: str
           +model: Model
           +config: Config
           +power_unit: str
           +source_path: Path <<property>>
           +relative_output_path: Path <<property>>
           +output_path: Path <<property>>
           +attributes: dict <<property>>
           +overwrite_from_existing_model() None
           +build() None
           +write() None
           +get_output_path() Path
           +attributes_to_dict() dict
           +save_attributes() None
           +save_data() None
       }

       class Technology {
           +name: str
           +subpath: str
           +capacity_addition_min: Attribute <<property>>
           +capacity_addition_max: Attribute <<property>>
           +capacity_addition_unbounded: Attribute <<property>>
           +capacity_existing: Attribute <<property>>
           +capacity_investment_existing: Attribute <<property>>
           +capacity_limit: Attribute <<property>>
           +carbon_intensity_technology: Attribute <<property>>
           +construction_time: Attribute <<property>>
           +lifetime: Attribute <<property>>
           +min_load: Attribute <<property>>
           +max_load: Attribute <<property>>
           +max_diffusion_rate: Attribute <<property>>
           +opex_specific_variable: Attribute <<property>>
           +opex_specific_fixed: Attribute <<property>>
           +reference_carrier: Attribute <<property>>
           +set_default_values_technology() None
           +_set_lifetime() Attribute*
           +_set_reference_carrier() Attribute*
       }

       class Carrier {
           +name: str
           +subpath: str
           +demand: Attribute <<property>>
           +availability_import: Attribute <<property>>
           +availability_export: Attribute <<property>>
           +availability_import_yearly: Attribute <<property>>
           +availability_export_yearly: Attribute <<property>>
           +price_import: Attribute <<property>>
           +price_export: Attribute <<property>>
           +carbon_intensity_carrier_import: Attribute <<property>>
           +carbon_intensity_carrier_export: Attribute <<property>>
           +price_shed_demand: Attribute <<property>>
           +set_default_values() None
       }

       class ConversionTechnology {
           +name: str
           +subpath: str
           +capex_specific_conversion: Attribute <<property>>
           +input_carrier: Attribute <<property>>
           +output_carrier: Attribute <<property>>
           +conversion_factor: Attribute <<property>>
           +set_default_values_conversion_technology() None
           +_set_input_carrier() Attribute*
           +_set_output_carrier() Attribute*
           +_set_conversion_factor() Attribute*
       }

       class StorageTechnology {
           +name: str
           +subpath: str
           +efficiency_charge: Attribute <<property>>
           +efficiency_discharge: Attribute <<property>>
           +self_discharge: Attribute <<property>>
           +capex_specific_storage: Attribute <<property>>
           +capex_specific_storage_energy: Attribute <<property>>
           +capacity_addition_min_energy: Attribute <<property>>
           +capacity_addition_max_energy: Attribute <<property>>
           +capacity_existing_energy: Attribute <<property>>
           +capacity_limit_energy: Attribute <<property>>
           +min_load_energy: Attribute <<property>>
           +max_load_energy: Attribute <<property>>
           +capacity_investment_existing_energy: Attribute <<property>>
           +opex_specific_fixed_energy: Attribute <<property>>
           +energy_to_power_ratio_min: Attribute <<property>>
           +energy_to_power_ratio_max: Attribute <<property>>
           +flow_storage_inflow: Attribute <<property>>
           +set_default_values_storage_technology() None
       }

       class RetrofittingTechnology {
           +name: str
           +subpath: str
           +retrofit_flow_coupling_factor: Attribute <<property>>
           +retrofit_reference_carrier: Attribute <<property>>
           +set_default_values_retrofitting_technology() None
           +_set_retrofit_flow_coupling_factor() Attribute*
           +_set_retrofit_reference_carrier() Attribute*
       }

       class TransportTechnology {
           +name: str
           +subpath: str
           +transport_loss_factor_linear: Attribute <<property>>
           +capex_per_distance_transport: Attribute <<property>>
           +distance: Attribute <<property>>
           +set_default_values_transport_technology() None
       }

       <<abstract>> Element
       <<abstract>> Technology
       <<abstract>> ConversionTechnology
       <<abstract>> StorageTechnology
       <<abstract>> RetrofittingTechnology
       <<abstract>> TransportTechnology

       Element <|-- Technology
       Element <|-- Carrier
       Technology <|-- ConversionTechnology
       Technology <|-- StorageTechnology
       Technology <|-- TransportTechnology
       ConversionTechnology <|-- RetrofittingTechnology


Dataset Classes
---------------

.. mermaid::
   :zoom:

   classDiagram
       class Dataset {
           +name: str
           +source_path: Path
           +title: str <<property>>
           +author: str <<property>>
           +publication: str <<property>>
           +publication_year: int <<property>>
           +doi: str <<property>>
           +url: str <<property>>
           +path: Path <<property>>
           +data <<property>>
           +metadata: dict <<property>>
           +_set_title() str*
           +_set_author() str*
           +_set_publication() str*
           +_set_publication_year() int*
           +_set_url() str*
           +_set_path() Path*
           +_set_data() *
           +get\_&lt;attribute_name&gt;() Attribute
       }

       class DatasetCollection {
           +name: str
           +source_path: Path
           +data: dict[str, Dataset] <<property>>
           +metadata: dict <<property>>
           +_get_data() dict[str, Dataset]*
       }

       class TechnoEconomicDataset {
           +name: str
           +available_technologies_finance: list
           +available_technologies_efficiency: list
           +available_technologies_lifetime: list
           +available_technologies_construction_time: list
           +money_year_source: int <<abstract_property>>
           +unit: str <<abstract_property>>
           +get_cost_data() DataFrame*
           +get_lifetime() DataFrame*
           +get_efficiency() DataFrame*
           +get_construction_time() DataFrame*
           +get_years() list[int]
           +get_units() str
           +rename_index() DataFrame
           +set_available_technologies() None
       }

       <<abstract>> DatasetCollection
       <<abstract>> Dataset
       <<abstract>> TechnoEconomicDataset

       DatasetCollection o-- Dataset
       Dataset <|-- TechnoEconomicDataset
