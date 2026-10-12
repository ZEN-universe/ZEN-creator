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
- :ref:`api.settings` holds the project-defined, type-checked settings
  of a model. Projects define ``SettingsCategory`` subclasses (for example
  ``time`` or ``region``), which elements and datasets read during the
  build. A category can control values of the ``Config``, so that each value
  has a single place where it is set. ``ModelSet`` reads a models file that
  declares variants of a dataset as patches of the settings (see
  :ref:`settings_and_models.settings_and_models`).
- :ref:`api.scenario` classes describe the scenario analysis of
  ZEN-garden. A ``Scenario`` varies one attribute and is attached where the
  attribute is set. The ``ScenarioRegistry`` of the model collects all
  entries and writes ``scenarios.yaml`` (see :ref:`scenarios.scenarios`).

.. mermaid::
   :zoom:

   classDiagram
       class Model
       class Config
       class Settings
       class SettingsCategory
       class ScenarioRegistry
       class Scenario
       class Sector
       class Element
       class EnergySystem
       class Attribute
       class Dataset
       class DatasetCollection

       Model --> Config
       Model --> Settings
       Model --> ScenarioRegistry
       Model --> Element
       Model --> EnergySystem
       Settings o-- SettingsCategory
       SettingsCategory ..> Config : controls
       EnergySystem --|> Element
       Sector o-- Element
       Element --> Attribute
       Attribute --> Scenario
       ScenarioRegistry o-- Scenario
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
       DatasetCollection o-- DatasetCollection

A ``DatasetCollection`` may contain other collections. Its metadata is then a
nested dictionary of the metadata of all datasets it contains.

Datasets and dataset collections are singletons: the first call constructs and
loads them, every later call with the same class returns the same object. A
dataset used by many elements is therefore loaded once per process.


.. _logic_structure.model_creation:

Model Creation Sequence
-----------------------

``Model.from_config()`` followed by ``build()`` and ``write()`` runs the
following steps:

1. **Load.** The configuration file is read into a ``Config``, and its
   ``settings:`` block into ``Settings``. Optionally, a patch from a models
   file is merged into the settings first.
2. **Apply settings.** Every settings category writes the configuration values
   it controls.
3. **Create the structure.** The energy system is instantiated from its
   registered name, the sectors are added, then the individually listed
   elements. Excluded sectors and elements are removed last. The scenarios of
   the ``scenarios:`` block of the configuration file are registered.
4. **Build.** ``Model.build()`` builds the energy system and then every
   element (see :ref:`logic_structure.building`).
5. **Global scenarios.** ``Model.apply_global_scenarios()`` runs the
   project's function that adds setting and set scenarios.
6. **Validate and write.** ``Model.write()`` validates the model and writes
   the input folder (see :ref:`logic_structure.output`).


.. _logic_structure.building:

Building Attributes
-------------------

Each element sets its attributes in ``_set_<attribute>()`` methods.
``Element.build()`` calls these methods and stores the returned ``Attribute``.
Attributes without such a method keep their default value.

An attribute may read the value of another attribute, also of another element,
for example a retrofitting technology reading the lifetime of the technology
it retrofits. Reading ``default_value``, ``df``, ``unit`` or another data
field of an attribute that has not been built yet builds it first. The
methods and the attribute names can therefore be written in any order. 
A cyclic dependency between attributes raises an error that shows the chain of 
attributes involved.

Requesting the attribute object itself (``element.lifetime``) or calling
``set_data()`` on it does not trigger a build.


.. _logic_structure.sectors:

Sectors
-------

A ``Sector`` lists the elements that belong to it and the sectors it requires
(``required_sectors``). When the sectors of a model are initialized, every
sector must find its required sectors among the configured sectors.

An element can be declared by several sectors. It is only added to the model
when all of these sectors are included. This models technologies that couple
two sectors, such as a power plant with carbon capture that belongs to both an
electricity and a carbon sector. Removing a sector removes exactly the
elements it declares.


.. _logic_structure.sources:

Source Tracking
---------------

``Attribute.set_data()`` requires a source. It is either a
``SourceInformation`` (a description together with the ``MetaData`` of the
dataset or collection the value comes from) or an ``AssumptionInformation`` (a
description of a modeling choice). Every call appends an entry, so an
attribute that is processed in several steps keeps all of them in order.

When the model is written, the entries of all attributes of an element are
written to ``sources.md`` in the element's folder, with full citations.


.. _logic_structure.output:

Written Files
-------------

``Model.write()`` writes the following files:

.. code-block:: text

   <output_folder>/
     config.yaml                ZEN-garden configuration (analysis, solver,
                                plugins), with analysis.dataset = model name
     <model name>/
       system.yaml              configured system settings and element lists
       scenarios.yaml           if scenarios are defined
       energy_system/
       set_carriers/<carrier>/
       set_technologies/set_conversion_technologies/<technology>/
       set_technologies/set_conversion_technologies/set_retrofitting_technologies/<technology>/
       set_technologies/set_storage_technologies/<technology>/
       set_technologies/set_transport_technologies/<technology>/

Each element folder contains ``attributes.yaml``, the data files of its
attributes, ``sources.md``, and the files of its scenarios.

``system.yaml`` and ``config.yaml`` only contain the values that were
configured, so that ZEN-garden applies its own defaults for everything else.
The technology lists are derived from the elements of the model.