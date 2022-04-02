import re

from sphinx.ext.autosummary import Autosummary, generate

from .templates import known_templates

directives_re = re.compile(r"^\.\. ([^:]+):: (.+)$", re.MULTILINE)

original_create_documenter = Autosummary.create_documenter


def extract_documenter(content):
    matches = directives_re.findall(content)
    (_, modname), (directive_name, name) = matches

    if directive_name.startswith("auto"):
        directive_name = directive_name[4:]

    return directive_name, "::".join([modname, name])


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
