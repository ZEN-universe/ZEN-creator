StorageTechnology
=================

Overview
--------

``StorageTechnology`` models technologies that store and release carriers over
time.

Use Cases
---------

- Implement storage-specific constraints and performance assumptions.
- Define charge, discharge, and capacity-related attributes.

Examples
--------

.. code-block:: python

   from zen_creator import StorageTechnology

   # Typically extended in project-specific implementations.
   class MyStorageTechnology(StorageTechnology):
       pass

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.StorageTechnology.__init__

.. rubric:: Constructors

.. automethod:: zen_creator.StorageTechnology.__init__

.. rubric:: Member Reference

.. autoclass:: zen_creator.StorageTechnology
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __init__
   :no-index: