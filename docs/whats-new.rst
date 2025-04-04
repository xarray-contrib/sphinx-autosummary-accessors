What's new
==========

2025.02.0 (*unreleased*)
------------------------
- drop support for python 3.8 (:pull:`135`)
- drop support for ``sphinx<5.3`` (:pull:`138`)
- officially support python 3.12 and 3.13 (:pull:`136`)

2023.04.0 (2022-04-12)
----------------------
- add official support for python 3.11 and `sphinx>=5.0` (:pull:`87`)
- change the policy to only actively support the last minor release of older major
  versions of `sphinx`.  Currently supported versions are now: `3.5`, `4.5`, and all minor
  versions of `5`, and `6` (:pull:`87`, :pull:`100`).
- switch to a `pyproject.toml`-based build (:pull:`99`)
- drop support for `python=3.7` (:pull:`93`)

2022.04.0 (2022-04-04)
----------------------
- skip unknown templates (:issue:`66`, :pull:`67`)

v0.2.1 (2021-06-06)
-------------------
- don't fail on options which are not parameters to the render function (:pull:`38`)
- drop support for python 3.6 (:pull:`39`)
- drop support for ``sphinx=3.2`` and start testing ``sphinx=4.0`` (:pull:`40`)

v0.2 (2021-03-06)
-----------------
- document the proper release methods (:pull:`20`)
- support nested accessors (:pull:`22`)
- drop support for ``sphinx<3.2`` (:pull:`25`)

v0.1.2 (2020-08-08)
-------------------
- declare the extension as parallel read safe (:pull:`19`)

v0.1.1 (2020-08-08)
-------------------
- fix autosummary blocks without a template option (:pull:`16`)
- fix create_documenter on sphinx<3.2 (:pull:`17`)
- add a documention url to the package description on PyPI (:pull:`18`)


v0.1 (2020-08-07)
-----------------
- import the templates and autodoc documenters from ``pandas`` (:pull:`1`)
- fix the broken callable accessor (:issue:`7`, :pull:`6`, :pull:`8`, :pull:`10`)
