.. _tutorials_templates.transport_technology:

################################
TransportTechnology Tutorial
################################

Class
=====

``TransportTechnology`` is the base class for assets that move energy/material
between places. Common examples are power lines, pipelines, and district heat
connections.

Purpose
=======

Use a ``TransportTechnology`` subclass (sometimes written as
"TransporTechnology" in informal text) when implementing pipes, lines, or other
infrastructure that transports carriers.

Key Attributes and Methods
==========================

Below is the complete attribute list for ``TransportTechnology`` (including
inherited attributes) and the matching builder method name that can be
implemented in your subclass.

- ``capacity_addition_min`` -> ``_set_capacity_addition_min()``
- ``capacity_addition_max`` -> ``_set_capacity_addition_max()``
- ``capacity_addition_unbounded`` -> ``_set_capacity_addition_unbounded()``
- ``capacity_existing`` -> ``_set_capacity_existing()``
- ``capacity_limit`` -> ``_set_capacity_limit()``
- ``min_load`` -> ``_set_min_load()``
- ``max_load`` -> ``_set_max_load()``
- ``opex_specific_variable`` -> ``_set_opex_specific_variable()``
- ``opex_specific_fixed`` -> ``_set_opex_specific_fixed()``
- ``carbon_intensity_technology`` -> ``_set_carbon_intensity_technology()``
- ``construction_time`` -> ``_set_construction_time()``
- ``capacity_investment_existing`` -> ``_set_capacity_investment_existing()``
- ``max_diffusion_rate`` -> ``_set_max_diffusion_rate()``
- ``lifetime`` -> ``_set_lifetime()``
- ``reference_carrier`` -> ``_set_reference_carrier()``
- ``transport_loss_factor_linear`` -> ``_set_transport_loss_factor_linear()``
- ``capex_per_distance_transport`` -> ``_set_capex_per_distance_transport()``
- ``distance`` -> ``_set_distance()``

In the base class, only some methods are strictly mandatory (abstract methods),
but any of the ``_set_<attribute_name>()`` methods above can be implemented.
If implemented, they are used during ``model.build()``.

Template (Auto-Synced)
======================

The example below is included directly from the Python template file. Any change
in the template source file is reflected automatically in this documentation.

.. literalinclude:: ../../../zen_creator/elements/transport_technologies/aa_template.py
   :language: python
