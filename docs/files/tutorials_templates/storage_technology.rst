.. _tutorials_templates.storage_technology:

##############################
StorageTechnology Tutorial
##############################

Class
=====

``StorageTechnology`` is the base class for assets that store energy and release
it later. Typical examples are batteries and thermal storage.

Purpose
=======

Create a ``StorageTechnology`` subclass when you need to represent charging,
discharging, and storage-related limits in a clear and reusable way.

Key Attributes and Methods
==========================

Below is the complete attribute list for ``StorageTechnology`` (including
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
- ``efficiency_charge`` -> ``_set_efficiency_charge()``
- ``efficiency_discharge`` -> ``_set_efficiency_discharge()``
- ``self_discharge`` -> ``_set_self_discharge()``
- ``capex_specific_storage`` -> ``_set_capex_specific_storage()``
- ``capex_specific_storage_energy`` -> ``_set_capex_specific_storage_energy()``
- ``capacity_addition_min_energy`` -> ``_set_capacity_addition_min_energy()``
- ``capacity_addition_max_energy`` -> ``_set_capacity_addition_max_energy()``
- ``capacity_existing_energy`` -> ``_set_capacity_existing_energy()``
- ``capacity_limit_energy`` -> ``_set_capacity_limit_energy()``
- ``min_load_energy`` -> ``_set_min_load_energy()``
- ``max_load_energy`` -> ``_set_max_load_energy()``
- ``capacity_investment_existing_energy`` ->
   ``_set_capacity_investment_existing_energy()``
- ``opex_specific_fixed_energy`` -> ``_set_opex_specific_fixed_energy()``
- ``energy_to_power_ratio_min`` -> ``_set_energy_to_power_ratio_min()``
- ``energy_to_power_ratio_max`` -> ``_set_energy_to_power_ratio_max()``
- ``flow_storage_inflow`` -> ``_set_flow_storage_inflow()``

In the base class, only some methods are strictly mandatory (abstract methods),
but any of the ``_set_<attribute_name>()`` methods above can be implemented.
If implemented, they are used during ``model.build()``.

Template (Auto-Synced)
======================

The example below is included directly from the Python template file. Any change
in the template source file is reflected automatically in this documentation.

.. literalinclude:: ../../../zen_creator/elements/storage_technologies/aa_template.py
   :language: python
