try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

import pathlib

import packaging
import sphinx

from . import autosummary
from .documenters import (
    AccessorAttributeDocumenter,
    AccessorCallableDocumenter,
    AccessorDocumenter,
    AccessorMethodDocumenter,
)

try:
    __version__ = version("sphinx-autosummary-accessors")
except Exception:
    __version__ = "999"

templates_path = str(pathlib.Path(__file__).parent / "templates")


def add_autosummary_create_documenter(func):
    import sphinx.ext.autosummary

    sphinx.ext.autosummary.Autosummary.create_documenter = func


def setup(app):
    app.setup_extension("sphinx.ext.autosummary")

    app.add_autodocumenter(AccessorDocumenter)
    app.add_autodocumenter(AccessorAttributeDocumenter)
    app.add_autodocumenter(AccessorMethodDocumenter)
    app.add_autodocumenter(AccessorCallableDocumenter)

    sphinx_version = packaging.version.parse(sphinx.__version__)
    if sphinx_version >= packaging.version.parse("3.2"):
        add_autosummary_create_documenter(autosummary.create_documenter_from_template)
    elif sphinx_version >= packaging.version.parse("3.1"):
        app.add_directive("autosummary", autosummary.CustomAutosummary, override=True)
