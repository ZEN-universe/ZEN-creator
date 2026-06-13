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

The code below shows an example of how to implement a subclass of the
``EnergySystem`` abstract class. Please read the docstrings
carefully as they contain detailed information on required methods and
syntax.

.. literalinclude:: ../../../zen_creator/elements/energy_systems/aa_template.py
   :language: python


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