sphinx-autosummary-accessors
============================

.. image:: https://github.com/xarray-contrib/sphinx-autosummary-accessors/workflows/CI/badge.svg?branch=master
    :target: https://github.com/xarray-contrib/sphinx-autosummary-accessors/actions
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black
.. image:: https://readthedocs.org/projects/sphinx-autosummary-accessors/badge/?version=latest
   :target: https://sphinx-autosummary-accessors.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

A ``sphinx`` extension to properly document
`pandas <https://github.com/pandas-dev/pandas>`_ or
`xarray <https://github.com/pydata/xarray>`_ accessors.

``autosummary`` is able to create summary and object pages for objects
and their methods, but it doesn't work well with accessor styled
properties and methods (``obj.accessor.attribute``). ``pandas`` has
accessor documentation built using ``autosummary`` templates, which
``xarray`` recently adopted by copying the templates and all related
code.

To avoid even more duplicated code, and to make it easier for projects
to document their custom accessors, this project aims to provide this
functionality by way of a ``sphinx`` extension.

Most of the code was adapted from ``pandas``.

Usage
=====
Using it should be as simple as adding

.. code:: python

   import sphinx_autosummary_accessors

   extensions = [
       ...,
       "sphinx_autosummary_accessors",
   ]
   templates = ["_templates", ..., sphinx_autosummary_accessors.template_path]

to your ``conf.py`` and using the appropriate template:

.. code:: rst

   .. autosummary::
      :template: autosummary/accessor_method.rst

      Example.test.multiply

Documentation
=============
For more information and examples, see the `documentation`_.

.. _documentation: https://sphinx-autosummary-accessors.readthedocs.io
