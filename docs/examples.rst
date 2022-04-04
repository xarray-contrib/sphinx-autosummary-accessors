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
   :lines: 32-68

for a class named :py:class:`Example`:

.. autosummary::
   :toctree: generated/

   Example

Documenting attributes and methods can be done with the
``accessor_attribute.rst`` and ``accessor_method.rst`` templates:

.. literalinclude:: examples.rst
   :language: rst
   :lines: 33-43

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

.. literalinclude:: examples.rst
   :language: rst
   :lines: 53-57

becomes:

.. autosummary::
   :toctree: generated/
   :template: autosummary/accessor_callable.rst

   Example.test

Methods on nested accessors can be documented, too:

.. literalinclude:: example.py
   :language: python
   :lines: 71-86

and

.. literalinclude:: examples.rst
   :language: rst
   :lines: 73-77

become:

.. autosummary::
   :toctree: generated/
   :template: autosummary/accessor_method.rst

   Example.test2.sub.func

Different templates still work:

.. literalinclude:: examples.rst
   :language: rst
   :lines: 87-91

becomes:

.. autosummary::
   :toctree: generated/
   :template: custom-template.rst

   TestAccessor
