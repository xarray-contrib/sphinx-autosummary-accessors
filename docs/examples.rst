.. currentmodule:: example

.. _examples:

Examples
========
Consider the accessor class:

.. literalinclude:: example.py
   :language: python
   :lines: 30-

Documenting attributes and methods can be done with the
``accessor_attribute.rst`` and ``accessor_method.rst`` templates:

.. code:: rst

   .. autosummary::
      :toctree: generated/
      :template: autosummary/accessor_attribute.rst

      Example.test.double

   .. autosummary::
      :toctree: generated/
      :template: autosummary/accessor_method.rst

      Example.test.multiply

becomes:

.. autosummary::
   :toctree: generated/
   :template: autosummary/accessor_attribute.rst

   Example.test.double

.. autosummary::
   :toctree: generated/
   :template: autosummary/accessor_method.rst

   Example.test.multiply

Callable accessors can be documented, too:

.. code:: rst

   .. autosummary::
      :toctree: generated/
      :template: autosummary/accessor_callable.rst

      Example.test

becomes:

.. autosummary::
   :toctree: generated/
   :template: autosummary/accessor_callable.rst

   Example.test
