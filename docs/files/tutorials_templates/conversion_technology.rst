.. _tutorials_templates.conversion_technology:

##################################
ConversionTechnology Tutorial
##################################

Class
=====

``ConversionTechnology`` is the base class for technologies that turn one type
of energy/material into another. For example, a heat pump can convert
electricity into heat.

Purpose
=======

Create a ``ConversionTechnology`` subclass when you want to define a specific
converter (for example a boiler, heat pump, or electrolyser), including its key
inputs, outputs, and performance values.

Key Attributes and Methods
==========================

Below is the complete attribute list for ``ConversionTechnology`` (including
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
- ``capex_specific_conversion`` -> ``_set_capex_specific_conversion()``
- ``input_carrier`` -> ``_set_input_carrier()``
- ``output_carrier`` -> ``_set_output_carrier()``
- ``conversion_factor`` -> ``_set_conversion_factor()``
- ``min_full_load_hours_fraction`` -> ``_set_min_full_load_hours_fraction()``

In the base class, only some methods are strictly mandatory (abstract methods),
but any of the ``_set_<attribute_name>()`` methods above can be implemented.
If implemented, they are used during ``model.build()``.

Template (Auto-Synced)
======================

The example below is included directly from the Python template file. Any change
in the template source file is reflected automatically in this documentation.

.. literalinclude:: ../../../zen_creator/elements/conversion_technologies/aa_template.py
   :language: python
