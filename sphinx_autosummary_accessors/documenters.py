from sphinx.ext.autodoc import AttributeDocumenter, Documenter, MethodDocumenter
from sphinx.ext.autodoc.importer import import_module
from sphinx.util import inspect


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

            if "." in mod_cls:
                modname, *parents = mod_cls.split(".")
            else:
                modname = mod_cls
                parents = []

            # check that we actually got a valid module
            # note: this will still result in incorrect results if mod_cls describes a
            # existing (but different) module.
            try:
                module = import_module(modname)
                cls = module
                for parent in parents:
                    cls = getattr(cls, parent)
            except (ImportError, AttributeError):
                parents.insert(0, modname)
                modname = None

            # if the module name is still missing, get it like above
            if not modname:
                modname = self.env.temp_data.get("autodoc:module")
            if not modname:
                modname = self.env.ref_context.get("py:module")
            # ... else, it stays None, which means invalid
        return modname, parents + [base]


class AccessorDocumenter(AccessorLevelDocumenter, MethodDocumenter):
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


class AccessorAttributeDocumenter(AccessorLevelDocumenter, AttributeDocumenter):
    objtype = "accessorattribute"
    directivetype = "attribute"

    # lower than AttributeDocumenter so this is not chosen for normal attributes
    priority = 0.6


class SlottedParentMethodDocumenter(MethodDocumenter):
    def import_object(self, raiseerror: bool = False) -> bool:
        """Copy pasted from MethodDocumenter to handle parent with __slots__"""
        ret = super(MethodDocumenter, self).import_object(raiseerror)
        if not ret:
            return ret

        # handle case when parent is instance with __slots__
        # otherwise autodoc errors, because it expects parents to have __dict__
        if hasattr(self.parent, "__slots__") and not isinstance(self.parent, type):
            self.parent = self.parent.__class__

        # to distinguish classmethod/staticmethod
        obj = self.parent.__dict__.get(self.object_name)

        if obj is None:
            obj = self.object

        if inspect.isclassmethod(obj) or inspect.isstaticmethod(
            obj, cls=self.parent, name=self.object_name
        ):
            # document class and static members before ordinary ones
            self.member_order = self.member_order - 1

        return ret


class AccessorMethodDocumenter(AccessorLevelDocumenter, SlottedParentMethodDocumenter):
    objtype = "accessormethod"
    directivetype = "method"

    # lower than MethodDocumenter so this is not chosen for normal methods
    priority = 0.6


class AccessorCallableDocumenter(
    AccessorLevelDocumenter, SlottedParentMethodDocumenter
):
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
