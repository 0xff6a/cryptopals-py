class HashSet(object):
    """A hash set implementation for fast set lookups"""
    def __init__(self, data=None):
        self._set = {}

        if data is not None:
            for element in data:
                self._set[element] = True

    def add(self, element):
        """Add an element to the set"""
        self._set[element] = True

    def remove(self, element):
        """Remove an element from the set"""
        self._set.pop(element, None)

    def clear(self):
        """Clear the contents of the set"""
        self._set = {}

    def contains(self, element):
        """Return boolean whether the element is in the set"""
        return self._set.has_key(element)

    def to_list(self):
        """Converts the set to a list"""
        return self._set.keys()
