import re

from sphinx.ext import autosummary
from sphinx.ext.autosummary import Autosummary, __, generate


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
        print("running custom get_items")
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
