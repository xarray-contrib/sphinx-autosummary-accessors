try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

import pathlib

from .autosummary import CustomAutosummary
from .documenters import (
    AccessorAttributeDocumenter,
    AccessorCallableDocumenter,
    AccessorDocumenter,
    AccessorMethodDocumenter,
)

try:
    __version__ = version("sphinx-autosummary-version")
except Exception:
    __version__ = "999"

templates_path = str(pathlib.Path(__file__).parent / "templates")


def setup(app):
    app.setup_extension("sphinx.ext.autosummary")

    app.add_autodocumenter(AccessorDocumenter)
    app.add_autodocumenter(AccessorAttributeDocumenter)
    app.add_autodocumenter(AccessorMethodDocumenter)
    app.add_autodocumenter(AccessorCallableDocumenter)

    app.add_directive("autosummary", CustomAutosummary, override=True)
