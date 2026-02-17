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
           +source_path: Path
           +elements: dict
           +out_path: Path <<property>>
           +energy_system: EnergySystem <<cached_property>>
           +carriers: dict <<property>>
           +technologies: dict <<property>>
           +storage_technologies: dict <<property>>
           +conversion_technologies: dict <<property>>
           +transport_technologies: dict <<property>>
           +retrofitting_technologies: dict <<property>>
           +add_sector() None
           +remove_sector() None
           +add_element() None
           +remove_element() None
           +validate() None
           +write() None
        }
        class Sector {
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
           +model: Model
           +config: Config 
           +source_path: Path
           +folder_path: Path
           +save_attributes() None
       }
       class Technology {
           +lifetime() Attribute*
           +reference_carrier() Attribute*
           +capacity_addition_min() Attribute
           +capacity_addition_max() Attribute
           +capacity_addition_unbounded() Attribute
           +capacity_existing() Attribute
           +capacity_limit() Attribute 
           +min_load() Attribute
           +max_load() Attribute
           +opex_specific_variable() Attribute
           +opex_specific_fixed() Attribute
           +carbon_intensity_technology() Attribute
           +construction_time() Attribute
           +capacity_investment_existing() Attribute
           +max_diffusion_rate() Attribute
       }
       class Carrier {
           +demand() Attribute
           +availability_import() Attribute
           +availability_export() Attribute
           +availability_import_yearly() Attribute
           +availability_export_yearly() Attribute
           +price_import() Attribute
           +price_export() Attribute
           +carbon_intensity_carrier_import() Attribute
           +carbon_intensity_carrier_import() Attribute
           +max_diffusion_rate() Attribute
       }
       class ConversionTechnology {
           +input_carrier() Attribute*
           +output_carrier() Attribute*
           +conversion_factor() Attribute*
           +capex_specific_conversion() Attribute
       }
       class StorageTechnology {
           +efficiency_charge() Attribute
           +efficiency_discharge() Attribute
           +self_discharge() Attribute
           +capex_specific_storage() Attribute
           +capacity_addition_min_energy() Attribute
           +capacity_addition_max_energy() Attribute
           +capacity_limit_energy() Attribute
           +max_load_energy() Attribute
           +capacity_investment_existing_energy() Attribute
           +opex_specific_fixed_energy() Attribute
           +energy_to_power_ratio_min() Attribute
           +energy_to_power_ratio_max() Attribute
           +flow_storage_inflow() Attribute
       }
       class RetrofittingTechnology {
       }
       class TransportTechnology {
           +transport_loss_factor_linear() Attribute
           +capex_per_distance_transport() Attribute
           +distance() Attribute
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
           +model: Model 
           +source_path: Path
           +author() str*
           +publication_year() int*
           +url() str*
           +load_data() None*
           +doi() str
           +metadata() dict
           +get\_&lt;attribute_name&gt;() Attribute
        }
        class DatasetCollection {
           +name: str
           +datasets: list
           +metadata() dict
           +Attribute get\_&lt;attribute_name&gt;()
        }
        class FinancialDataset{
            +money_year_source() int*
            +unit() str*
            +convert_to_money_year() float 
            +cost_of_capital() float
        }

        <<abstract>> DatasetCollection
        <<abstract>> Dataset
        <<abstract>> FinancialDataset

        DatasetCollection o-- Dataset
        Dataset <|-- FinancialDataset
       


