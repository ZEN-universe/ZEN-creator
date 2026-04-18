EnergySystem
============

Overview
--------

``EnergySystem`` stores system-level settings and attributes used by the model.

Use Cases
---------

- Configure global model behavior and system assumptions.
- Read, modify, and write the ``energy_system`` data structure.

Examples
--------

.. code-block:: python

   from zen_creator import EnergySystem

   # Typically extended in project-specific implementations.
   class MyEnergySystem(EnergySystem):
       pass

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.EnergySystem.__init__

.. rubric:: Constructors

.. automethod:: zen_creator.EnergySystem.__init__

.. rubric:: Member Reference

.. autoclass:: zen_creator.EnergySystem
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __init__
   :no-index: