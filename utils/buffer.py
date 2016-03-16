from array import array

class Buffer(object):
    """"Generic buffer object to hold binary data for manipulation"""
    def __init__(self, data):
        self.__data = array('B', data)

    @classmethod
    def init(self, size, value = 0):
        """Initialize a buffer of the specified size initialized to value"""
        data = [value] * size
        self.__init__(data)

    @classmethod
    def from_base64(self, string):
        """Create a new buffer from a base64 encoded string"""

    @classmethod
    def from_hex(self, string):
        """Create a new buffer from a hex encoded string"""

    @classmethod
    def from_bin(self, string):
        """Create a new buffer from a binary encoded string"""

    @classmethod
    def from_file(self, filepath):
        """Create a new buffer from the contents of a file"""

    @property
    def bytes(self):
        """Returns an array of buffer bytes"""
        return self.__data.tolist()

    @property
    def size(self):
        """Returns the buffer size (bytes)"""
        return len(self.__data)

    def to_base64(self):
        """Converts the buffer to a base64 encoded string"""

    def to_hex(self):
        """Converts the buffer to a hex encoded string"""

    def to_bin(self):
        """Converts the buffer to a binary encoded string"""

    def to_file(self, encoding, filepath):
        """Dumps the buffer to a file in the specified encoding"""

    def xor(self, buffer):
        """Return XORed bytes of each buffer (up to size of current buffer)"""

    def concat(self, buffer):
        """Concatenate the buffer with another"""
