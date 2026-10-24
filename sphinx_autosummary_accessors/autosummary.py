import re

import sphinx
from packaging import version as pv
from sphinx.ext.autosummary import generate

from sphinx_autosummary_accessors.templates import known_templates

directives_re = re.compile(r"^\.\. ([^:]+):: (.+)$", re.MULTILINE)


def extract_documenter(content):
    matches = directives_re.findall(content)
    (_, modname), (directive_name, name) = matches

    if directive_name.startswith("auto"):
        directive_name = directive_name[4:]

    return directive_name, "::".join([modname, name])


def patch_autosummary_old(cls):
    original_create_documenter = cls.create_documenter

    def create_documenter_from_template(autosummary, app, obj, parent, full_name):
        real_name = ".".join(full_name.split("::"))

        options = autosummary.options
        template_name = options.get("template", None)
        if template_name is None or template_name not in known_templates:
            return original_create_documenter(autosummary, app, obj, parent, full_name)

        imported_members = options.get("imported_members", False)
        recursive = options.get("recursive", False)

        context = {}
        context.update(app.config.autosummary_context)

        rendered = generate.generate_autosummary_content(
            real_name,
            obj,
            parent,
            template=generate.AutosummaryRenderer(app),
            template_name=template_name,
            app=app,
            context=context,
            imported_members=imported_members,
            recursive=recursive,
        )

        documenter_name, real_name = extract_documenter(rendered)
        doccls = app.registry.documenters.get(documenter_name)
        documenter = doccls(autosummary.bridge, real_name)

        return documenter

    cls.create_documenter = create_documenter_from_template


def patch_autosummary_8_2(cls):
    original_create_documenter = cls.create_documenter

    def create_documenter_from_template(
        autosummary, obj, parent, full_name, *, registry
    ):
        real_name = ".".join(full_name.split("::"))

        options = autosummary.options
        template_name = options.get("template", None)
        if template_name is None or template_name not in known_templates:
            return original_create_documenter(
                autosummary, obj, parent, full_name, registry=registry
            )

        imported_members = options.get("imported_members", False)
        recursive = options.get("recursive", False)

        context = {}
        context.update(autosummary.env.config.autosummary_context)

        rendered = generate.generate_autosummary_content(
            real_name,
            obj,
            parent,
            template=generate.AutosummaryRenderer(autosummary.env.app),
            template_name=template_name,
            context=context,
            imported_members=imported_members,
            recursive=recursive,
            registry=registry,
            events=autosummary.env.events,
            config=autosummary.env.config,
        )

        documenter_name, real_name = extract_documenter(rendered)
        doccls = registry.documenters.get(documenter_name)
        documenter = doccls(autosummary.bridge, real_name)

        return documenter

    cls.create_documenter = create_documenter_from_template


def patch_autosummary_9(app, cls):
    app.config.autodoc_use_legacy_class_based = True

    def get_items(self, names: list[str]) -> list[tuple[str, str | None, str, str]]:
        """Try to import the given names, and return a list of
        ``[(name, signature, summary_string, real_name), ...]``.

        signature is already formatted and is None if :nosignatures: option was given.
        """
        from types import ModuleType

        from sphinx.ext.autodoc._legacy_class_based._directive_options import Options
        from sphinx.ext.autodoc.directive import DocumenterBridge
        from sphinx.ext.autosummary import (
            ImportExceptionGroup,
            __,
            _AutodocAttrGetter,
            _AutodocConfig,
            _AutoDocumenterOptions,
            _get_documenter,
            _load_object_by_name,
            extract_summary,
            get_import_prefixes_from_env,
            logger,
            mangle_signature,
        )

        prefixes = get_import_prefixes_from_env(self.env)

        items: list[tuple[str, str | None, str, str]] = []

        signatures_option = self.options.get("signatures")
        if signatures_option is None:
            signatures_option = "none" if "nosignatures" in self.options else "long"
        if signatures_option not in {"none", "short", "long"}:
            msg = (
                "Invalid value for autosummary :signatures: option: "
                f"{signatures_option!r}. Valid values are 'none', 'short', 'long'"
            )
            raise ValueError(msg)

        document_settings = self.state.document.settings
        env = self.env
        config = _AutodocConfig.from_config(env.config)
        current_document = env.current_document
        events = env.events
        get_attr = _AutodocAttrGetter(env._registry.autodoc_attrgetters)
        opts = _AutoDocumenterOptions()
        ref_context = env.ref_context
        reread_always = env.reread_always

        max_item_chars = 50

        for name in names:
            display_name = name
            if name.startswith("~"):
                name = name[1:]
                display_name = name.split(".")[-1]

            try:
                real_name, obj, parent, modname = self.import_by_name(
                    name, prefixes=prefixes
                )
            except ImportExceptionGroup as exc:
                errors = list({f"* {type(e).__name__}: {e}" for e in exc.exceptions})
                logger.warning(
                    __("autosummary: failed to import %s.\nPossible hints:\n%s"),
                    name,
                    "\n".join(errors),
                    location=self.get_location(),
                )
                continue

            template_name = self.options.get("template")
            is_accessor_template = (
                template_name is not None and template_name in known_templates
            )
            if is_accessor_template:
                imported_members = self.options.get("imported_members", False)
                recursive = self.options.get("recursive", False)

                context = {}
                context.update(app.config.autosummary_context)

                rendered = generate.generate_autosummary_content(
                    real_name,
                    obj,
                    parent,
                    template=generate.AutosummaryRenderer(app),
                    template_name=template_name,
                    context=context,
                    imported_members=imported_members,
                    recursive=recursive,
                    config=config,
                    events=events,
                )

                documenter_name, full_name = extract_documenter(rendered)
                doccls = app.registry.documenters.get(documenter_name)
                bridge = DocumenterBridge(
                    env,
                    self.state.document.reporter,
                    Options(),
                    self.lineno,
                    self.state,
                )

                documenter = doccls(bridge, full_name)
                result = documenter.parse_name()
                if not result:
                    raise RuntimeError(f"failed to parse {full_name}")

                path, base = full_name.rsplit(".", maxsplit=1)
                modname, [*parents, new_base] = documenter.resolve_name(
                    None, [parent], path, base
                )
                if new_base == "__call__":
                    old_base = parents[-1]
                    parent = getattr(parent, old_base)
                # manually set the parent and object
                documenter.parent = parent
                documenter.object = getattr(parent, base)

                if signatures_option == "none":
                    sig = None
                else:
                    try:
                        sig = documenter.format_signature(show_annotation=False)
                    except TypeError:
                        # the documenter does not support ``show_annotation`` option
                        sig = documenter.format_signature()

                    if not sig:
                        sig = ""
                    elif signatures_option == "short":
                        sig = "()"
                    else:  # signatures_option == 'long'
                        max_chars = max(10, max_item_chars - len(display_name))
                        sig = mangle_signature(sig, max_chars=max_chars)

                [docstring_lines] = documenter.get_doc()
                summary = extract_summary(docstring_lines, document_settings)

                items.append((display_name, sig, summary, real_name))
                continue
            elif isinstance(obj, ModuleType):
                full_name = real_name
            else:
                # give explicitly separated module name, so that members
                # of inner classes can be documented
                full_name = f"{modname}::{real_name[len(modname) + 1 :]}"

            obj_type = _get_documenter(obj, parent)

            # NB. using full_name here is important, since Documenters
            #     handle module prefixes slightly differently
            props = _load_object_by_name(
                name=full_name,
                objtype=obj_type,
                current_document=current_document,
                config=config,
                events=events,
                get_attr=get_attr,
                options=opts,
                ref_context=ref_context,
                reread_always=reread_always,
            )
            if props is None:
                logger.warning(
                    __("failed to import object %s"),
                    real_name,
                    location=self.get_location(),
                )
                items.append((display_name, "", "", real_name))
                continue

            # -- Grab the signature

            if signatures_option == "none":
                sig = None
            elif not props.signatures:
                sig = ""
            elif signatures_option == "short":
                sig = "()" if props.signatures == ("()",) else "(…)"
            else:  # signatures_option == 'long'
                max_chars = max(10, max_item_chars - len(display_name))
                sig = mangle_signature("\n".join(props.signatures), max_chars=max_chars)

            # -- Grab the summary

            # get content from docstrings or attribute documentation
            summary = extract_summary(props.docstring_lines, document_settings)

            items.append((display_name, sig, summary, real_name))

        return items

    cls.get_items = get_items


def patch_autosummary(app, cls):
    sphinx_version = pv.parse(sphinx.__version__)
    if sphinx_version < pv.Version("8.2.0"):
        patch_autosummary_old(cls)
    elif pv.Version("8.2.0") <= sphinx_version < pv.Version("9.0.0"):
        patch_autosummary_8_2(cls)
    else:
        # assume no further changes, to be extended later if necessary
        patch_autosummary_9(app, cls)
