TransportTechnology
===================

Overview
--------

``TransportTechnology`` models technologies that transport carriers across
locations.

Use Cases
---------

- Define transport losses, distances, and transport-specific costs.
- Represent networked carrier transport components.

Examples
--------

.. code-block:: python

   from zen_creator import TransportTechnology

   # Typically extended in project-specific implementations.
   class MyTransportTechnology(TransportTechnology):
       pass

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.TransportTechnology.__init__

.. rubric:: Constructors

.. automethod:: zen_creator.TransportTechnology.__init__

.. rubric:: Member Reference

.. autoclass:: zen_creator.TransportTechnology
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __init__
   :no-index: