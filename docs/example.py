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


class Example:
    def __init__(self, data):
        self._data = data


def register_accessor(name):
    def func(accessor):
        setattr(Example, name, CachedAccessor(name, accessor))

        return accessor

    return func


@register_accessor("test")
class TestAccessor:
    """ an accessor of Example """

    def __init__(self, obj):
        self._obj = obj

    def __call__(self, other):
        """ check for equality

        Parameters
        ----------
        other
            The value to compare to

        Returns
        -------
        result : bool
        """

        return self._obj._data == other

    @property
    def double(self):
        """ double the data """
        return self.multiply(2)

    def multiply(self, factor):
        """ multiply data with a factor

        Parameters
        ----------
        factor : int
            The factor for the multiplication
        """

        return self._obj._data * factor
