.. _api.sector:

Sector
======

Overview
--------

``Sector`` groups related elements so they can be added or removed together.

Use Cases
---------

- Organize element sets by domain (for example power or transport).
- Apply consistent sector-level model composition logic.

Examples
--------

.. code-block:: python

   from zen_creator import Sector

   # Typically extended in project-specific implementations.
   class MySector(Sector):
       pass

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.Sector.__init__

.. rubric:: Constructors

.. automethod:: zen_creator.Sector.__init__

.. rubric:: Member Reference

.. autoclass:: zen_creator.Sector
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __init__
   :no-index: