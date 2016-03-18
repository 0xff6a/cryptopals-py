class HashSet(object):
    """A hash set implementation for fast set lookups"""
    def __init__(self, data = []):
        self.__set = {}

        for el in data:
            self.__set[el] = True

    def add(self, el):
        """Add an element to the set"""
        self.__set[el] = True

    def remove(self, el):
        """Remove an element from the set"""
        self.__set.pop(el, None)

    def clear(self):
        """Clear the contents of the set"""
        self.__set = {}

    def contains(self, el):
        """Return boolean whether the element is in the set"""
        return self.__set.has_key(el)

    def to_list(self):
        """Converts the set to a list"""
        return self.__set.keys()
