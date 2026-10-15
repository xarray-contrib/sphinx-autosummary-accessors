try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

from sphinx_autosummary_accessors.autosummary import patch_autosummary
from sphinx_autosummary_accessors.documenters import (
    AccessorAttributeDocumenter,
    AccessorCallableDocumenter,
    AccessorDocumenter,
    AccessorMethodDocumenter,
)
from sphinx_autosummary_accessors.templates import templates_path  # noqa: F401

try:
    __version__ = version("sphinx-autosummary-accessors")
except Exception:
    __version__ = "9999"


def add_autosummary_create_documenter(func):
    import sphinx.ext.autosummary

    sphinx.ext.autosummary.Autosummary.create_documenter = func


def setup(app):
    from sphinx.ext.autosummary import Autosummary

    app.setup_extension("sphinx.ext.autodoc")
    app.setup_extension("sphinx.ext.autosummary")

    app.add_autodocumenter(AccessorDocumenter)
    app.add_autodocumenter(AccessorAttributeDocumenter)
    app.add_autodocumenter(AccessorMethodDocumenter)
    app.add_autodocumenter(AccessorCallableDocumenter)

    patch_autosummary(app, Autosummary)

    return {"version": __version__, "parallel_read_safe": True}
