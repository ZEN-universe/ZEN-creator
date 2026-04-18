################################
ZEN-Creator Logic and Structure
################################

One of the core objectives of ZEN-creator is to provide a platform
based on which modeling teams can collaboratively develop and maintain
input data for ZEN-garden models. To achieve this, ZEN-creator provides
a structured representation of ZEN-garden input data and a series of
abstract classes that can ensure all developers agree on the same data
structures and workflows.

This section describes the logic and structure of the ZEN-creator
codebase, in particular the core classes and their relationships. Further
details on how to implement each of the required abstract classes can be
found in the API Reference section of the documentation.

For a quick jump to the in-page diagrams, see :ref:`logic_structure.core_architecture_diagram`,
:ref:`logic_structure.element_hierarchy_diagram`, and
:ref:`logic_structure.dataset_hierarchy`.

.. _logic_structure.core_architecture_diagram:

Core Architecture
-----------------

ZEN-creator is built around a structured object model for
constructing, modifying, validating, and writing ZEN-garden input data.

The code is organized into clear layers, each with a specific job:

- :ref:`api.model` is an object representation of the
  complete ZEN-garden input data. It serves as the main entry point for
  users of ZEN-creator and provides a high-level interface for working
  with ZEN-garden input data.
- :ref:`api.element` is an abstract class that
  represents technologies, carriers, and the energy system. A model
  consists of multiple elements. Abstract subclasses of Element represent
  different components of a ZEN-garden model (energy system, carrier,
  conversion technology, storage technology, transport technology, and
  retrofitting technology). On collaborative projects, these abstract
  classes can be implemented to store input assumptions for the different
  elements in consistent ways across developers. Furthermore, the abstract
  classes provide templates for how ZEN-creator expects the assumptions
  underlying each element to be stored. These abstract classes therefore
  ensure compatibility with the rest of the ZEN-creator codebase, and
  each element can have multiple attributes. 
  :ref:`logic_structure.element_hierarchy_diagram`
  shows the inheritance hierarchy of the element classes.
- :ref:`api.sector` is a convenience class that can be
  used to group elements together. It is not required, but it can be
  useful for users who want to organize their model in a particular way.
  For example, users may want to group all electricity generation
  technologies so that they can be collectively referred to together.
- :ref:`api.attribute` is a class that stores
  all of the data for a single attribute of an element (e.g.
  "conversion_factor" for a conversion technology). It includes methods
  for setting and validating attribute values as well as tracking the
  data source where the assumptions for an attribute come from.
- :ref:`api.dataset` and
  :ref:`api.dataset_collection`
  are abstract classes that provide a template for how raw datasets
  should be processed into attribute values. They include abstract methods
  for loading raw data, transforming it into the desired format,
  validating the final output, and storing citation information. These
  classes are designed to be implemented by users of ZEN-creator to
  ensure that all raw data is processed in a consistent way across
  developers. The ``Dataset`` class should be used whenever an attribute
  consists of data from a single dataset. The ``DatasetCollection`` class
  should be used when an attribute consists of data from multiple
  datasets. :ref:`logic_structure.dataset_hierarchy` shows the relationship 
  between the data classes.
- :ref:`api.config` is a class that
  stores all configurations of ZEN-creator. The config can be used to
  tell ZEN-creator which elements (carriers and technologies) to include
  in the final model or which datasets/sources to use. The ``Config``
  class can be inherited and extended by projects to allow additional
  dataset or element options to be included. The ``Config`` class can be
  used in the ``Model.from_config()`` constructor to allow users to
  create a model without writing any code directly. 

.. mermaid::
   :zoom:

   classDiagram
       class Model
       class Config
       class Sector
       class Element
       class EnergySystem
       class Attribute
       class Dataset
       class DatasetCollection

       Model --> Config
       Model --> Element
       Model --> EnergySystem
       EnergySystem --|> Element
       Sector o-- Element
       Element --> Attribute
       DatasetCollection o-- Dataset
       Dataset ..> Attribute


.. _logic_structure.element_hierarchy_diagram:

Element Hierarchy
-----------------

Technology and carrier classes follow a simple inheritance hierarchy.

.. mermaid::
   :zoom:

   classDiagram
       class Element
       class Technology
       class Carrier
       class EnergySystem
       class ConversionTechnology
       class StorageTechnology
       class TransportTechnology
       class RetrofittingTechnology

       <<abstract>> Element
       <<abstract>> Technology
       <<abstract>> ConversionTechnology
       <<abstract>> StorageTechnology
       <<abstract>> TransportTechnology
       <<abstract>> RetrofittingTechnology

       Element <|-- Technology
       Element <|-- Carrier
       Element <|-- EnergySystem
       Technology <|-- ConversionTechnology
       Technology <|-- StorageTechnology
       Technology <|-- TransportTechnology
       ConversionTechnology <|-- RetrofittingTechnology

.. _logic_structure.dataset_hierarchy:

Dataset Hierarchy
-----------------

Data classes separate raw data processing from element logic, so element
subclasses can stay focused on model behavior.

.. mermaid::
   :zoom:

   classDiagram
       class Dataset
       class DatasetCollection

       <<abstract>> Dataset
       <<abstract>> DatasetCollection

       DatasetCollection o-- Dataset