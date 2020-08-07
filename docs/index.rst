sphinx-autosummary-accessors
============================
**sphinx-autosummary-accessors** is a `sphinx`_ extension to properly
document `pandas`_ or `xarray`_ style accessors using `autosummary`_
and `autodoc`_.

`autosummary`_ is able to create summary and detail pages for objects
and their methods, but it doesn't work well with accessor styled
properties and methods (``obj.accessor.attribute``). `pandas`_ uses
`autosummary`_ templates to build its accessor documentation, which
`xarray`_ recently adopted by copying the templates and all related
code.

To avoid even more duplicated code, and to make it easier for projects
to document their custom accessors, this package aims to make this
(almost) as simple as adding ``"sphinx_autosummary_accessors"`` to the
``extensions`` setting.

Most of the code is adapted from `pandas`_.

It is developed on `github
<https://github.com/keewis/sphinx-autosummary-accessors>`_.

**Documentation**:

* :doc:`installing`
* :doc:`usage`
* :doc:`templates`
* :doc:`examples`
* :doc:`whats-new`


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Contents

   installing
   usage
   templates
   examples
   whats-new

.. _sphinx: https://www.sphinx-doc.org
.. _pandas: https://pandas.pydata.org
.. _xarray: https://xarray.pydata.org
.. _autodoc: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
.. _autosummary: https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html
