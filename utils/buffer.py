from array import array
import base64
import binascii

class Buffer(object):
    """"Generic buffer object to hold binary data for manipulation"""
    def __init__(self, data):
        self.__data = array('B', data)

    @classmethod
    def init(_class, size, value = 0):
        """Initialize a buffer of the specified size initialized to value"""
        data = [value] * size
        return _class(data)

    @classmethod
    def from_base64(_class, string):
        """Create a new buffer from a base64 encoded string"""

    @classmethod
    def from_hex(_class, string):
        """Create a new buffer from a hex encoded string"""

    @classmethod
    def from_bin(_class, string):
        """Create a new buffer from a binary encoded string"""

    @classmethod
    def from_file(_class, filepath):
        """Create a new buffer from the contents of a file"""

    @property
    def bytes(self):
        """Returns an array of buffer bytes"""
        return self.__data.tolist()

    @property
    def size(self):
        """Returns the buffer size (bytes)"""
        return len(self.__data)

    def to_string(self):
        """Converts a buffer to an ASCII string"""
        return self.__data.tostring()

    def to_base64(self):
        """Converts the buffer to a base64 encoded string"""
        return base64.b64encode(self.to_string())

    def to_hex(self):
        """Converts the buffer to a hex encoded string"""
        return binascii.hexlify(self.to_string())

    def to_bin(self):
        """Converts the buffer to a binary encoded string"""
        out_str = ''
        for byte in self.__data:
            out_str += format(byte, '08b')

        return out_str

    def to_file(self, encoding, filepath):
        """Dumps the buffer to a file in the specified encoding"""


    def xor(self, buffer):
        """Return XORed bytes of each buffer (up to size of current buffer)"""

    def concat(self, buffer):
        """Concatenate the buffer with another"""
