from example.extensions import CachedAccessor, register_accessor


@register_accessor("test")
class TestAccessor:
    """an accessor of Example"""

    def __init__(self, obj):
        self._obj = obj

    def __call__(self, other):
        """check for equality

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
        """double the data"""
        return self.multiply(2)

    def multiply(self, factor):
        """multiply data with a factor

        Parameters
        ----------
        factor : int
            The factor for the multiplication
        """

        return self._obj._data * factor


class SubAccessor:
    def __init__(self, obj):
        self._obj = obj

    def func(self, a):
        """namespaced function"""
        print(self._obj, a)


@register_accessor("test2")
class Test2Accessor:
    """an accessor of Example"""

    sub = CachedAccessor("sub", SubAccessor)

    def __init__(self, obj):
        self._obj = obj
