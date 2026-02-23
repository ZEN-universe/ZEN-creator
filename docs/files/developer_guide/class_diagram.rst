################################
ZEN-Creator Class Diagram
################################

Overview
----------
.. mermaid::
   :zoom:

   classDiagram
       class Model {
           +name: str
           +config: Config
           +elements: dict
           +source_path: Path <<property>>
           +out_path: Path <<property>>
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
           +build() None
           +validate() None
           +write() None
        }
        class Sector {
           +name: str <<class attribute>>
           +elements: dict <<property>>
        }
        class Element{
        }
        class DatasetCollection{
        }
        class Dataset{
        }
        class Config{
        }
        class EnergySystem{
           +system_file: SystemFile
           +nodes() None
           +edges() None
           +price_carbon_emissions_annual_overshoot() Attribute
           +carbon_emissions_budget() Attribute
           +carbon_emissions_annual_limit() Attribute
           +price_carbon_emissions_budget_overshoot() Attribute
           +price_carbon_emissions() Attribute
           +carbon_emissions_cumulative_existing() Attribute
           +discount_rate() Attribute
           +knowledge_spillover_rate() Attribute
           +knowledge_depreciation_rate() Attribute
           +market_share_unbounded() Attribute
        }
        class Attribute{
            +name: str
            +default_value
            +unit: str
            +data: DataFrame
            +source: dict
            +set_default_value() None
            +set_unit() None
            +set_data() None
            +set_source() None
            +save_data() None 
            +to_dict() dict

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
        DatasetCollection ..> Attribute
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
           +source_path: Path
           +relative_out_path: Path <<property>>
           +out_path: Path <<property>>
           +attributes: dict <<property>>
           +overwrite_from_existing_model()
           +build()
           +save_attributes()
           +save_data()


           +save_attributes() None
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
           +max_diffusion_rate: Attribute <<property>>
           +max_load:Attribute <<property>>
           +opex_specific_variable: Attribute <<property>>
           +opex_specific_fixed: Attribute <<property>>
           +reference_carrier: Attribute <<property>>
           +_set_lifetime(): Attribute*
           +_set_reference_carrier(): Attribute*
       }
       class Carrier {
           +name: str
           +subpath: str
           +availability_import: Attribute <<property>>
           +availability_export: Attribute <<property>>
           +availability_import_yearly: Attribute <<property>>
           +availability_export_yearly: Attribute <<property>>
           +carbon_intensity_carrier_import: Attribute <<property>>
           +carbon_intensity_carrier_import: Attribute <<property>>
           +demand: Attribute <<property>>
           +max_diffusion_rate: Attribute <<property>>
           +price_import: Attribute <<property>>
           +price_export: Attribute <<property>>
       }
       class ConversionTechnology {
           +name: str
           +subpath: str
           +capex_specific_conversion: Attribute <<property>>
           +conversion_factor: Attribute <<property>>
           +input_carrier: Attribute <<property>>
           +output_carrier: Attribute <<property>>
           +_set_conversion_factor()*:Attribute
           +_set_input_carrier()*: Attribute
           +_set_output_carrier()*: Attribute
       }
       class StorageTechnology {
           +name: str
           +subpath: str
           +efficiency_charge: Attribute <<property>>
           +efficiency_discharge: Attribute <<property>>
           +self_discharge: Attribute <<property>>
           +capex_specific_storage: Attribute <<property>>
           +capacity_addition_min_energy: Attribute <<property>>
           +capacity_addition_max_energy: Attribute <<property>>
           +capacity_limit_energy: Attribute <<property>>
           +max_load_energy: Attribute <<property>>
           +capacity_investment_existing_energy: Attribute <<property>>
           +opex_specific_fixed_energy: Attribute <<property>>
           +energy_to_power_ratio_min: Attribute <<property>>
           +energy_to_power_ratio_max: Attribute <<property>>
           +flow_storage_inflow: Attribute <<property>>
       }
       class RetrofittingTechnology {
       }
       class TransportTechnology {
           +name: str
           +subpath: str
           +transport_loss_factor_linear: Attribute <<property>>
           +capex_per_distance_transport: Attribute <<property>>
           +distance: Attribute <<property>>
       }

       <<abstract>> Technology
       <<abstract>> Element
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
           +author: str <<property>>
           +publication_year: int <<property>>
           +doi: str <<property>>
           +url: str <<property>>
           +path: Path <<property>>
           +data: <<property>>
           +metadata: dict <<property>>
           +_get_author()*: str
           +_get_publication_year()*: int 
           +_get_url()*: str
           +_get_path()*: Path
           +_get_data()*
           +get\_&lt;attribute_name&gt;() Attribute
        }
        class DatasetCollection {
           +name: str
           +data: dict <<property>>
           +metadata: dict
           +_get_data()*
           +Attribute get\_&lt;attribute_name&gt;()
        }
        class TechnoEconomicDataset{
           +name: str
           +available_technologies_finance: list
           +available_technologies_efficiency: list
           +available_technologies_lifetime: list
           +available_technologies_construction: list
           +money_year_source*: int <<abstract_property>>
           +unit*: str <<abstract_property>>
           +convert_to_money_year() float 
           +_get_cost_data*: DataFrame
           +_get_efficiency*: DataFrame
           +_get_construction_time*: DataFrame
           +_get_lifetime*: DataFrame
        }


        <<abstract>> DatasetCollection
        <<abstract>> Dataset
        <<abstract>> TechnoEconomicDataset

        DatasetCollection o-- Dataset
        Dataset <|-- TechnoEconomicDataset

