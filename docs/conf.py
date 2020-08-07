# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import datetime as dt
import pathlib
import site
import subprocess
import sys

here = pathlib.Path(__file__).absolute().parent
site.addsitedir(str(here))
site.addsitedir(str(here.parent))

import sphinx_autosummary_accessors  # isort:skip # noqa: F401


# -- environment information -------------------------------------------------

print(f"sys.path: {sys.path}")
print(f"sphinx-autosummary-accessors: {sphinx_autosummary_accessors.__version__}")
print("environment:")
subprocess.run(["python", "-m", "pip", "list"])

# -- Project information -----------------------------------------------------

project = "sphinx-autosummary-accessors"
year = dt.datetime.now().year
author = "xarray developers"
copyright = f"{year}, {author}"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_autosummary_accessors",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates", sphinx_autosummary_accessors.templates_path]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# master document
master_doc = "index"
suffix = ".rst"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]


# -- Extension configuration -------------------------------------------------

# autodoc
autodoc_typehints = "none"

# autosummary
autosummary_generate = True

# extlinks
base_url = "https://github.com/xarray-contrib/sphinx-autosummary-accessors"
extlinks = {
    "issue": (f"{base_url}/issues/%s", "GH"),
    "pull": (f"{base_url}/pull/%s", "PR"),
}

# napoleon
napoleon_use_param = False
napoleon_use_rtype = True


# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}
