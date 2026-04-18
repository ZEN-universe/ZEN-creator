.. _api.attribute:

Attribute
=========

Overview
--------

``Attribute`` stores values, metadata, units, and provenance for one model
attribute.

Use Cases
---------

- Set and validate default values for element attributes.
- Manage tabular and yearly varying data with source information.

Examples
--------

.. code-block:: python

   from zen_creator import Attribute

   # Usually created through element classes.
   class MyAttribute(Attribute):
       pass

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.Attribute.__init__

.. rubric:: Constructors

.. automethod:: zen_creator.Attribute.__init__

.. rubric:: Member Reference

.. autoclass:: zen_creator.Attribute
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __init__
   :no-index: