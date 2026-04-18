Config
======

Overview
--------

``Config`` stores the model configuration used to initialize model structure,
input paths, and selected element sets.

Use Cases
---------

- Load model settings from YAML files.
- Pass validated configuration objects into ``Model.from_config``.

Examples
--------

.. code-block:: python

   from pathlib import Path
   from zen_creator import Config

   config = Config.load_from_yaml(Path("./config.yaml"))

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.Config.__init__

.. rubric:: Constructors

.. automethod:: zen_creator.Config.__init__

.. rubric:: Member Reference

.. autoclass:: zen_creator.Config
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __init__
   :no-index: