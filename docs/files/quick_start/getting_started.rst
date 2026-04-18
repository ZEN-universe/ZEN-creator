.. _getting_started.getting_started:

#################
Getting Started
#################

This page introduces the main model object in ``ZEN-creator`` and shows the two
most common ways to create it.

The Model class
===============

The main entry point for working with ZEN-creator is the
:class:`~zen_creator.model.Model` class. A ``Model`` object stores 
the input data for ZEN-garden in a structured and easy-to-access way.

The ``Model`` object is programmed in a modular way that makes it easy for 
users of ZEN-creator to load, create, manipulate, and save the ZEN-garden
input files. It further includes validation schemes to ensure that the 
final saved outcome remains a valid and complete input for ZEN-garden. 

The model object contains three possible constructors that can be useful
to users with different goals. The three constructors are:

1. The ``Model()`` constructor simply creates a blank model object that 
   contains no input data. This constructor is ideal for users that would like
   to develop new input data from scratch; however, it is very low-level 
   so an advanced understanding of ZEN-creator and its requirements is 
   necessary to build a model from this constructor.
2. The ``Model.from_existing()`` constructor allows users to import an
   existing ZEN-garden input data file tree into a ``Model`` object. The 
   main advantage of this is that it then allows users to manipulate the 
   existing input data using the functionality and data structures provided 
   by ZEN-creator. This constructor is therefore useful for all users 
   who have access to an existing model and who would like to modify that 
   model.

   Example:

   .. code-block:: python

      from pathlib import Path
      from zen_creator.model import Model, compare_trees

      path_to_existing = Path("./path/to/existing/model") # the exiting model
      output_path = Path("./outputs") # outputs will be saved here
      
      # load the model
      model = Model.from_existing(path_to_existing)

      # update the model here with any desired changes
      model.name = "my_updated_model"
      model.output_folder = output_path

      # save the new model
      model.write()

      #compare with the previous version if desired
      compare_trees(path_to_existing, model.output_path)


3. The ``Model.from_config()`` constructor allows users to create a model
   object from settings in a config file. This requires that a prior setup 
   of model data and options. It is therefore most useful for collaborative
   projects in which multiple people co-develop the model.

   Example:

   .. code-block:: python

      from pathlib import Path
      from zen_creator.model import Model

      model = Model.from_config(Path("./config.yaml"))
      model.write()

Typical workflow
================

A simple workflow usually looks like this:

1. Load a model with ``from_existing`` or ``from_config``.
2. Update the model as needed.
3. Call ``model.write()`` to save the modified model.


Model Structure
=================

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
           +remove_sector() None
           +add_element_by_name() None
           +remove_element_by_name() None
           +build() None
           +validate() None
           +write() None
       }


Model attributes
----------------

.. list-table:: Model attributes
   :header-rows: 1

   * - Attribute
     - Description
   * - ``name``
     - The model name used in output files and documentation.
   * - ``config``
     - The configuration object that defines model setup and included data.
   * - ``elements``
     - The complete collection of elements that make up the model.
   * - ``source_path``
     - The folder containing the source input data for the model.
   * - ``output_folder``
     - The folder where generated model files are written.
   * - ``output_path``
     - The resolved path to the model output location.
   * - ``energy_system``
     - The energy system element associated with the model.
   * - ``carriers``
     - The carrier elements available in the model.
   * - ``technologies``
     - The technology elements available in the model.
   * - ``storage_technologies``
     - The storage technology elements available in the model.
   * - ``conversion_technologies``
     - The conversion technology elements available in the model.
   * - ``transport_technologies``
     - The transport technology elements available in the model.
   * - ``retrofitting_technologies``
     - The retrofitting technology elements available in the model.



Model methods
-------------

.. list-table:: Model methods
   :header-rows: 1

   * - Method
     - Description
   * - ``from_config()``
     - Create a model from a configuration file.
   * - ``from_existing()``
     - Load an existing model directory and reuse its current values.
   * - ``add_sector_by_name()``
     - Add a sector to the model by its name.
   * - ``remove_sector()``
     - Remove a sector from the model.
   * - ``add_element_by_name()``
     - Add an element to the model by its name.
   * - ``remove_element_by_name()``
     - Remove an element from the model by its name.
   * - ``build()``
     - Build the model by applying the class-specific element logic.
   * - ``validate()``
     - Validate the model before writing output files.
   * - ``write()``
     - Write the model output to disk.