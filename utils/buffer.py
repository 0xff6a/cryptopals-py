from array import array
import base64
import binascii

SZ_BYTE = 8

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
    def from_b64(_class, string):
        """Create a new buffer from a base64 encoded string"""
        ascii_str = base64.b64decode(string)

        return _class(ascii_str)

    @classmethod
    def from_hex(_class, string):
        """Create a new buffer from a hex encoded string"""
        ascii_str = string.decode('hex')

        return _class(ascii_str)

    @classmethod
    def from_bin(_class, string):
        """Create a new buffer from a binary encoded string"""
        ascii_str = ''
        for i in xrange(0, len(string), SZ_BYTE):
            ascii_str += chr(int(string[i:i + SZ_BYTE], 2))

        return _class(ascii_str)

    @classmethod
    def from_file(_class, filepath, encoding):
        """Create a new buffer from the contents of a file"""
        fo = open(filepath, 'r')
        raw = fo.read()
        fo.close()

        if encoding == 'b64':
            return _class.from_b64(raw)
        elif encoding == 'hex':
            return _class.from_hex(raw)
        elif encoding == 'bin':
            return _class.from_bin(raw)
        else:
            return _class(raw)

    @property
    def bytes(self):
        """Returns an array of buffer bytes"""
        return self.__data.tolist()

    @property
    def size(self):
        """Returns the buffer size (bytes)"""
        return len(self.__data)

    def get(self, index):
        """Get the byte value at index"""
        return self.__data[index]

    def set(self, index, value):
        """Set the byte value at index"""
        self.__data[index] = value

    def to_string(self):
        """Converts a buffer to an ASCII string"""
        return self.__data.tostring()

    def to_b64(self):
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

    def to_file(self, filepath, encoding):
        """Dumps the buffer to a file in the specified encoding"""
        if encoding == 'b64':
            out_data = self.to_b64()
        elif encoding == 'hex':
            out_data = self.to_hex()
        elif encoding == 'bin':
            out_data = self.to_bin()
        else:
            out_data = self.to_string()

        fo = open(filepath, 'w', 1)
        fo.write(out_data)
        fo.close()

    def xor(self, buffer):
        """Return XORed bytes of each buffer (up to size of current buffer)"""
        result = self.__class__.init(self.size)

        for i in range(self.size):
            result.set(i, self.get(i) ^ buffer.get(i))

        return result

    def concat(self, buffer):
        """Concatenate the buffer with another"""
        self.__data.extend(buffer.bytes)

        return self

    def map(self, func):
        """Map the buffer to a new buffer using a lambda"""
        raw_in = self.__data
        out = self.__class__.init(self.size)

        for i in range(self.size):
            out.set(i, func(raw_in[i]))

        return out

    def copy(self):
        """Copy a buffer into a new instance and return it"""
        return self.__class__(self.__data)
