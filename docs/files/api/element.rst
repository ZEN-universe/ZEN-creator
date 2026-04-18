Element
=======

Overview
--------

``Element`` is the base abstraction for carriers and technologies in
ZEN-creator.

Use Cases
---------

- Define shared behavior for all model elements.
- Implement project-specific subclasses with custom attribute logic.

Examples
--------

.. code-block:: python

   from zen_creator import Element

   # Typically extended in project-specific implementations.
   class MyElement(Element):
       pass

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.Element.__init__

.. rubric:: Constructors

.. automethod:: zen_creator.Element.__init__

.. rubric:: Member Reference

.. autoclass:: zen_creator.Element
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __init__
   :no-index: