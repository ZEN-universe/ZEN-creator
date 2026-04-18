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

.. code-block:: python

   from zen_creator import Dataset

   # Typically extended in project-specific implementations.
   class MyDataset(Dataset):
       pass

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