.. _tutorials_templates.dataset:

##################
Dataset Tutorial
##################

Class
=====

``Dataset`` is the base class for reading one data source (for example a CSV,
Excel file, or API output). In simple terms, this class is where you load data,
clean it, and make it ready for the rest of the model.

Purpose
=======

Create a ``Dataset`` subclass when you want a clear, reusable place for data
loading logic. This keeps data preparation out of element classes and makes your
project easier to test and maintain.

Key Attributes and Methods
==========================

Important attributes:

- ``name``: A unique dataset name.
- ``source_path``: Root folder where raw files are stored.
- ``metadata``: Citation and source information.
- ``path``: Final resolved path to the dataset file.
- ``data``: Loaded data (for example one DataFrame).

Important methods:

- ``_set_metadata()``: Returns citation details for this dataset.
- ``_set_path()``: Resolves where the dataset file is located.
- ``_set_data()``: Loads and optionally cleans the raw data.
- ``get_<attribute_name>()`` methods (example in template): Convert dataset data
   into ``Attribute`` objects for technologies/carriers.

Template (Auto-Synced)
======================

The example below is included directly from the Python template file. Any change
in the template source file is reflected automatically in this documentation.

.. literalinclude:: ../../../zen_creator/datasets/datasets/aa_template.py
   :language: python
