ConversionTechnology
====================

Overview
--------

``ConversionTechnology`` describes technologies that convert one carrier into
another (for example electricity to heat).

Use Cases
---------

- Implement conversion technologies with project-specific assumptions.
- Provide conversion-related attributes for model build and export.

Examples
--------

.. code-block:: python

   from zen_creator import ConversionTechnology

   # Typically extended in project-specific implementations.
   class MyConversionTechnology(ConversionTechnology):
       pass

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.ConversionTechnology.__init__

.. rubric:: Constructors

.. automethod:: zen_creator.ConversionTechnology.__init__

.. rubric:: Member Reference

.. autoclass:: zen_creator.ConversionTechnology
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __init__
   :no-index: