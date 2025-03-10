from example.object import Example


class CachedAccessor:
    def __init__(self, name, accessor):
        self._name = name
        self._accessor = accessor

    def __get__(self, obj, cls):
        if obj is None:
            return self._accessor

        accessor_obj = self._accessor(obj)
        setattr(obj, self._name, accessor_obj)

        return accessor_obj


def register_accessor(name):
    def func(accessor):
        setattr(Example, name, CachedAccessor(name, accessor))

        return accessor

    return func
