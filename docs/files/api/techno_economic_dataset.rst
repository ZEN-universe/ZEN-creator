TechnoEconomicDataset
=====================

Overview
--------

``TechnoEconomicDataset`` provides structured techno-economic data handling for
model attributes.

Use Cases
---------

- Store and process techno-economic assumptions.
- Supply validated values to technology attribute pipelines.

Examples
--------

.. code-block:: python

   from zen_creator import TechnoEconomicDataset

   # Typically extended in project-specific implementations.
   class MyTechnoEconomicDataset(TechnoEconomicDataset):
       pass

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.TechnoEconomicDataset.__init__

.. rubric:: Constructors

.. automethod:: zen_creator.TechnoEconomicDataset.__init__

.. rubric:: Member Reference

.. autoclass:: zen_creator.TechnoEconomicDataset
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __init__
   :no-index: