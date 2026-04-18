.. _api.config:

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

The code below shows an example of a full ``config.yaml`` file. This file is
used to configure ZEN-creator and is required for it to run.

.. literalinclude:: ../generated/default_config_example.yaml
   :language: yaml

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