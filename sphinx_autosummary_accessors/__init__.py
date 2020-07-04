try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

import pathlib

import packaging.version
import sphinx

from .documenters import (
    AccessorAttributeDocumenter,
    AccessorCallableDocumenter,
    AccessorDocumenter,
    AccessorMethodDocumenter,
)

if packaging.version.parse(sphinx.__version__) >= packaging.version.parse("3.1"):
    from .autosummary import CustomAutosummary
else:
    CustomAutosummary = None


try:
    __version__ = version("sphinx-autosummary-accessors")
except Exception:
    __version__ = "999"

templates_path = str(pathlib.Path(__file__).parent / "templates")


def setup(app):
    app.setup_extension("sphinx.ext.autosummary")

    app.add_autodocumenter(AccessorDocumenter)
    app.add_autodocumenter(AccessorAttributeDocumenter)
    app.add_autodocumenter(AccessorMethodDocumenter)
    app.add_autodocumenter(AccessorCallableDocumenter)

    if CustomAutosummary is not None:
        app.add_directive("autosummary", CustomAutosummary, override=True)
