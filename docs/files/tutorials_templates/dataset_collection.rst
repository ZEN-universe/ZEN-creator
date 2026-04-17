.. _tutorials_templates.dataset_collection:

############################
DatasetCollection Tutorial
############################

Class
=====

``DatasetCollection`` is a class that groups several datasets in one place. In
simple terms, it acts as a coordinator: it decides which dataset should provide
which value.

Purpose
=======

Create a ``DatasetCollection`` subclass when an element value depends on more
than one data source, or when you want one simple access point for dataset
logic.

Key Attributes and Methods
==========================

Important attributes:

- ``name``: A unique collection name.
- ``source_path``: Root folder for all datasets in the collection.
- ``data``: Dictionary mapping dataset names to dataset instances.

Important methods:

- ``_get_data()``: Builds and returns the dataset dictionary.
- ``get_<attribute_name>()`` methods (example in template): Combine dataset
   outputs and return ``Attribute`` objects.
- ``__init__()``: Usually passes ``source_path`` to the base class so all
   datasets can resolve their paths.

Template (Auto-Synced)
======================

The example below is included directly from the Python template file. Any change
in the template source file is reflected automatically in this documentation.

.. literalinclude:: ../../../zen_creator/datasets/dataset_collections/aa_Template.py
   :language: python
