.. _api.dataset:

Dataset
=======

Overview
--------

``Dataset`` represents a single raw data source and related transformation
logic used to produce model attributes.

Use Cases
---------

- Encapsulate loading and preprocessing of one source dataset.
- Expose attribute-ready outputs to elements and dataset collections.

Examples
--------

The code below shows an example of how to implement a subclass of the
``Dataset`` abstract class. Please read the docstrings carefully as they
contain detailed information on required methods and syntax.

.. literalinclude:: ../../../zen_creator/datasets/datasets/aa_template.py
   :language: python

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.Dataset.__init__

.. rubric:: Constructors

.. automethod:: zen_creator.Dataset.__init__

.. rubric:: Member Reference

.. autoclass:: zen_creator.Dataset
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __init__
   :no-index: