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

The code below shows an example of how to implement a subclass of the
``StorageTechnology`` abstract class. Please read the docstrings
carefully as they contain detailed information on required methods and
syntax.

.. literalinclude:: ../../../zen_creator/elements/storage_technologies/aa_template.py
   :language: python

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