try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

import pathlib

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

    add_autosummary_create_documenter(autosummary.create_documenter_from_template)

    return {"version": __version__, "parallel_read_safe": True}
