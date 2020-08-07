.. ATTENTION: to work around a bug in autosummary (it executes
   autosummary directives in code blocks), this uses literalinclude on
   itself. That means that each time the number of lines change, we
   have to check that this is still up-to-date.
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

.. literalinclude:: examples.rst
   :language: rst
   :lines: 26-36

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

.. warning::

    This feature is only fully supported from sphinx version 3.1 onwards. On
    earlier versions, the summary will claim this is a alias of the
    accessor class.

.. literalinclude:: examples.rst
   :language: rst
   :lines: 52-56

becomes:

.. autosummary::
   :toctree: generated/
   :template: autosummary/accessor_callable.rst

   Example.test
