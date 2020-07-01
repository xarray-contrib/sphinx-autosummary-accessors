accessors
=========
`accessors` is a `sphinx` extension to properly document `pandas`_ or
`xarray`_ style accessors using `autosummary`_ and `autodoc`_.

`autosummary`_ is able to create summary and detail pages for objects
and their methods, but its doesn't work well with accessor styled
properties and methods (``obj.accessor.attribute``). `pandas`_ has
accessor documentation build using `autosummary`_ templates, which
`xarray`_ recently adopted by copying the templates and all related
code.

To avoid even more duplicated code, and to make it easier for projects
to document their custom accessors, this package aims to make this as
simple as adding ``"accessors"`` to the ``extensions`` setting in
``conf.py``:

.. code:: python

    extensions = [
       ...,
       "accessors",
       ...,
    ]

Then, we can simply add a template option to the `autosummary`_
directives to get summary and detail pages:

.. code:: rst

   .. currentmodule:: example

   .. autosummary::
      :toctree: generated/
      :template: accessor_attribute.rst

      Example.test.double

   .. autosummary::
      :toctree: generated/
      :template: accessor_method.rst

      Example.test.multiply
   

will become:

.. currentmodule:: example

.. autosummary::
    :toctree: generated/
    :template: accessor_attribute.rst

    Example.test.double

.. autosummary::
    :toctree: generated/
    :template: accessor_method.rst

    Example.test.multiply

.. _sphinx: https://www.sphinx-doc.org
.. _pandas: https://pandas.pydata.org
.. _xarray: https://xarray.pydata.org
.. _autodoc: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
.. _autosummary: https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html
