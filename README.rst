sphinx-autosummary-accessors
============================

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
functionality by way of a ``sphinx`` extension. Once it is finished,
using it should be (almost) as simple as adding ``"accessors"`` to
``extensions`` in the project's ``conf.py``.
