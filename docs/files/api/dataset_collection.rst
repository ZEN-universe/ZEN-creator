DatasetCollection
=================

Overview
--------

``DatasetCollection`` coordinates multiple datasets and combines them into
outputs used by model elements.

Use Cases
---------

- Combine multiple data sources into one attribute pipeline.
- Centralize dataset orchestration for reproducible transformations.

Examples
--------

.. code-block:: python

   from zen_creator import DatasetCollection

   # Typically extended in project-specific implementations.
   class MyDatasetCollection(DatasetCollection):
       pass

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.DatasetCollection.__init__

.. rubric:: Constructors

.. automethod:: zen_creator.DatasetCollection.__init__

.. rubric:: Member Reference

.. autoclass:: zen_creator.DatasetCollection
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __init__
   :no-index: