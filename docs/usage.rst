Usage
=====

To enable the extension, add it to the list of extensions in ``conf.py``:

.. code:: python

    extensions = [
       ...,
       "sphinx_autosummary_accessors",
       ...,
    ]

and set ``templates_path`` appropriately:

.. code:: python

   templates_path = ["_templates", sphinx_autosummary_accessors.templates_path]

Then, we can simply add a ``template`` option to the ``autosummary``
directive to get summary and detail pages:

.. code:: rst

   .. currentmodule:: example

   Just the attributes:
   .. autosummary::
      :toctree: generated/
      :template: autosummary/accessor_attribute.rst

      Example.test.double

   The methods:
   .. autosummary::
      :toctree: generated/
      :template: autosummary/accessor_method.rst

      Example.test.multiply


For more, see :doc:`templates` and :doc:`examples`.
