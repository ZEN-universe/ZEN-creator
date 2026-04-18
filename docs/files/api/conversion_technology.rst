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

The code below shows an example of how to implement a subclass of the
``ConversionTechnology`` abstract class. Please read the docstrings
carefully as they contain detailed information on required methods and
syntax.

.. literalinclude:: ../../../zen_creator/elements/conversion_technologies/aa_template.py
   :language: python

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