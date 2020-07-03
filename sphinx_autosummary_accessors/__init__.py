import pathlib
import re

import sphinx
from sphinx.ext import autosummary
from sphinx.ext.autodoc import AttributeDocumenter, Documenter, MethodDocumenter
from sphinx.ext.autosummary import Autosummary, __, generate
from sphinx.util import rpartition

templates_path = str(pathlib.Path(__file__).parent / "templates")


class AccessorDocumenter(MethodDocumenter):
    """
    Specialized Documenter subclass for accessors.
    """

    objtype = "accessor"
    directivetype = "method"

    # lower than MethodDocumenter so this is not chosen for normal methods
    priority = 0.6

    def format_signature(self):
        # this method gives an error/warning for the accessors, therefore
        # overriding it (accessor has no arguments)
        return ""


class AccessorLevelDocumenter(Documenter):
    """
    Specialized Documenter subclass for objects on accessor level (methods,
    attributes).
    """

    # This is the simple straightforward version
    # modname is None, base the last elements (eg 'hour')
    # and path the part before (eg 'Series.dt')
    # def resolve_name(self, modname, parents, path, base):
    #     modname = 'pandas'
    #     mod_cls = path.rstrip('.')
    #     mod_cls = mod_cls.split('.')
    #
    #     return modname, mod_cls + [base]

    def resolve_name(self, modname, parents, path, base):
        if modname is None:
            if path:
                mod_cls = path.rstrip(".")
            else:
                mod_cls = None
                # if documenting a class-level object without path,
                # there must be a current class, either from a parent
                # auto directive ...
                mod_cls = self.env.temp_data.get("autodoc:class")
                # ... or from a class directive
                if mod_cls is None:
                    mod_cls = self.env.temp_data.get("py:class")
                # ... if still None, there's no way to know
                if mod_cls is None:
                    return None, []
            # HACK: this is added in comparison to ClassLevelDocumenter
            # mod_cls still exists of class.accessor, so an extra
            # rpartition is needed
            modname, accessor = rpartition(mod_cls, ".")
            modname, cls = rpartition(modname, ".")
            parents = [cls, accessor]
            # if the module name is still missing, get it like above
            if not modname:
                modname = self.env.temp_data.get("autodoc:module")
            if not modname:
                if sphinx.__version__ > "1.3":
                    modname = self.env.ref_context.get("py:module")
                else:
                    modname = self.env.temp_data.get("py:module")
            # ... else, it stays None, which means invalid
        return modname, parents + [base]


class AccessorAttributeDocumenter(AccessorLevelDocumenter, AttributeDocumenter):

    objtype = "accessorattribute"
    directivetype = "attribute"

    # lower than AttributeDocumenter so this is not chosen for normal attributes
    priority = 0.6


class AccessorMethodDocumenter(AccessorLevelDocumenter, MethodDocumenter):

    objtype = "accessormethod"
    directivetype = "method"

    # lower than MethodDocumenter so this is not chosen for normal methods
    priority = 0.6


class AccessorCallableDocumenter(AccessorLevelDocumenter, MethodDocumenter):
    """
    This documenter lets us removes .__call__ from the method signature for
    callable accessors like Series.plot
    """

    objtype = "accessorcallable"
    directivetype = "method"

    # lower than MethodDocumenter; otherwise the doc build prints warnings
    priority = 0.5

    def format_name(self):
        return MethodDocumenter.format_name(self).rstrip(".__call__")


def extract_documenter(content):
    directives_re = re.compile(r"^\.\. ([^:]+):: (.+)$", re.MULTILINE)
    matches = directives_re.findall(content)
    (_, modname), (directive_name, name) = matches

    if directive_name.startswith("auto"):
        directive_name = directive_name[4:]

    return directive_name, "::".join([modname, name])


class CustomAutosummary(Autosummary):
    def get_documenter_from_template(self, name, obj, parent, options):
        options = options.copy()
        options.pop("toctree")
        template_name = options.pop("template")
        options["imported_members"] = options.get("imported_members", False)
        options["recursive"] = options.get("recursive", False)

        app = self.env.app

        context = {}
        context.update(app.config.autosummary_context)

        rendered = generate.generate_autosummary_content(
            name,
            obj,
            parent,
            template=generate.AutosummaryRenderer(app),
            template_name=template_name,
            app=app,
            context=context,
            **options,
        )

        documenter_name, real_name = extract_documenter(rendered)
        documenter = app.registry.documenters.get(documenter_name)

        return documenter, real_name

    def get_items(self, names):
        """Try to import the given names, and return a list of
        ``[(name, signature, summary_string, real_name), ...]``.
        """
        prefixes = autosummary.get_import_prefixes_from_env(self.env)

        items = []

        max_item_chars = 50

        for name in names:
            display_name = name
            if name.startswith("~"):
                name = name[1:]
                display_name = name.split(".")[-1]

            try:
                with autosummary.mock(self.config.autosummary_mock_imports):
                    real_name, obj, parent, modname = autosummary.import_by_name(
                        name, prefixes=prefixes
                    )
            except ImportError:
                autosummary.logger.warning(
                    __("autosummary: failed to import %s"),
                    name,
                    location=self.get_source_info(),
                )
                continue

            # initialize for each documenter
            self.bridge.result = autosummary.StringList()
            full_name = real_name
            if not isinstance(obj, autosummary.ModuleType):
                # give explicitly separated module name, so that members
                # of inner classes can be documented
                full_name = modname + "::" + full_name[len(modname) + 1 :]
            # NB. using full_name here is important, since Documenters
            #     handle module prefixes slightly differently

            if "template" in self.options:
                doccls, full_name = self.get_documenter_from_template(
                    real_name, obj, parent, self.options
                )
            else:
                doccls = autosummary.get_documenter(self.env.app, obj, parent)

            documenter = doccls(self.bridge, full_name)
            if not documenter.parse_name():
                autosummary.logger.warning(
                    __("failed to parse name %s"),
                    real_name,
                    location=self.get_source_info(),
                )
                items.append((display_name, "", "", real_name))
                continue
            if not documenter.import_object():
                autosummary.logger.warning(
                    __("failed to import object %s"),
                    real_name,
                    location=self.get_source_info(),
                )
                items.append((display_name, "", "", real_name))
                continue
            if documenter.options.members and not documenter.check_module():
                continue

            # try to also get a source code analyzer for attribute docs
            try:
                documenter.analyzer = autosummary.ModuleAnalyzer.for_module(
                    documenter.get_real_modname()
                )
                # parse right now, to get PycodeErrors on parsing (results will
                # be cached anyway)
                documenter.analyzer.find_attr_docs()
            except autosummary.PycodeError as err:
                autosummary.logger.debug("[autodoc] module analyzer failed: %s", err)
                # no source file -- e.g. for builtin and C modules
                documenter.analyzer = None

            # -- Grab the signature

            try:
                sig = documenter.format_signature(show_annotation=False)
            except TypeError:
                # the documenter does not support ``show_annotation`` option
                sig = documenter.format_signature()

            if not sig:
                sig = ""
            else:
                max_chars = max(10, max_item_chars - len(display_name))
                sig = autosummary.mangle_signature(sig, max_chars=max_chars)

            # -- Grab the summary

            documenter.add_content(None)
            summary = autosummary.extract_summary(
                self.bridge.result.data[:], self.state.document
            )

            items.append((display_name, sig, summary, real_name))

        return items


def setup(app):
    app.setup_extension("sphinx.ext.autosummary")

    app.add_autodocumenter(AccessorDocumenter)
    app.add_autodocumenter(AccessorAttributeDocumenter)
    app.add_autodocumenter(AccessorMethodDocumenter)
    app.add_autodocumenter(AccessorCallableDocumenter)

    app.add_directive("autosummary", CustomAutosummary, override=True)
