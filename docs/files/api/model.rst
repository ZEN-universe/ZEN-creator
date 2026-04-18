Model
=====

.. currentmodule:: zen_creator.model

.. autoclass:: zen_creator.model.Model
   :show-inheritance:
   :no-members:
   :no-special-members:


.. rubric:: Summary

.. autosummary::
   :nosignatures:

   Model.from_config
   Model.from_existing
   Model.build
   Model.validate
   Model.write


.. rubric:: Constructors

.. automethod:: Model.__init__

.. automethod:: Model.from_config

.. automethod:: Model.from_existing


.. rubric:: Core Methods

.. automethod:: Model.build

.. automethod:: Model.validate

.. automethod:: Model.write

.. automethod:: Model.write_system_file


.. rubric:: Element and Sector Management

.. automethod:: Model.add_sector_by_name

.. automethod:: Model.add_sector

.. automethod:: Model.remove_sector

.. automethod:: Model.add_element_by_name

.. automethod:: Model.add_element

.. automethod:: Model.remove_element_by_name

.. automethod:: Model.remove_element


.. rubric:: Attributes and Properties

Instance attributes
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Attribute
     - Description
   * - ``name``
     - Model name used when writing output paths.
   * - ``config``
     - Configuration object used to initialize model behavior.
   * - ``elements``
     - Dictionary of model elements keyed by element name.

Properties
~~~~~~~~~~

.. autosummary::
   :nosignatures:

   Model.source_path
   Model.output_folder
   Model.output_path
   Model.energy_system
   Model.carriers
   Model.technologies
   Model.storage_technologies
   Model.conversion_technologies
   Model.transport_technologies
   Model.retrofitting_technologies

.. autoproperty:: Model.source_path
  :no-index:

.. autoproperty:: Model.output_folder
  :no-index:

.. autoproperty:: Model.output_path

.. autoproperty:: Model.energy_system
  :no-index:

.. autoproperty:: Model.carriers

.. autoproperty:: Model.technologies

.. autoproperty:: Model.storage_technologies

.. autoproperty:: Model.conversion_technologies

.. autoproperty:: Model.transport_technologies

.. autoproperty:: Model.retrofitting_technologies