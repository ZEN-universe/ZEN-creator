.. _api.dataset_collection:

DatasetCollection
=================

Overview
--------

``DatasetCollection`` coordinates multiple datasets and combines them into
outputs used by model elements.

Use Cases
---------

- Combine multiple data sources into one attribute pipeline.
- Centralize dataset orchestration for reproducible transformations.

Examples
--------

The code below shows an example of how to implement a subclass of the
``DatasetCollection`` abstract class. Please read the docstrings carefully as
they contain detailed information on required methods and syntax.

.. literalinclude:: ../../../zen_creator/datasets/dataset_collections/aa_Template.py
   :language: python

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.DatasetCollection.__init__

.. rubric:: Constructors

.. automethod:: zen_creator.DatasetCollection.__init__

.. rubric:: Member Reference

.. autoclass:: zen_creator.DatasetCollection
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __init__
   :no-index: