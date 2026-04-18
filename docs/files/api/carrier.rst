Carrier
=======

Overview
--------

``Carrier`` represents energy carriers used across technologies and system
components in a model.

Use Cases
---------

- Define or customize carrier behavior in a project-specific subclass.
- Store carrier-related attributes used by technologies and validation logic.

Examples
--------

.. code-block:: python

   from zen_creator import Carrier

   # Typically extended in project-specific implementations.
   class MyCarrier(Carrier):
       pass

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.Carrier.__init__

.. rubric:: Constructors

.. automethod:: zen_creator.Carrier.__init__

.. rubric:: Member Reference

.. autoclass:: zen_creator.Carrier
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __init__
   :no-index: