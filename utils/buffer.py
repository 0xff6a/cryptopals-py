import base64
import binascii

from array import array
from gmpy2 import mpz

SZ_BYTE = 8

class Buffer(object):
    """"Generic buffer object to hold binary data for manipulation"""
    def __init__(self, data):
        self._data = array('B', data)

    @classmethod
    def init(cls, size, value=0):
        """Initialize a buffer of the specified size initialized to value"""
        data = [value] * size

        return cls(data)

    @classmethod
    def from_b64(cls, string):
        """Create a new buffer from a base64 encoded string"""
        ascii_str = base64.b64decode(string)

        return cls(ascii_str)

    @classmethod
    def from_hex(cls, string):
        """Create a new buffer from a hex encoded string"""
        ascii_str = string.decode('hex')

        return cls(ascii_str)

    @classmethod
    def from_bin(cls, string):
        """Create a new buffer from a binary encoded string"""
        ascii_str = ''
        for i in xrange(0, len(string), SZ_BYTE):
            ascii_str += chr(int(string[i:i + SZ_BYTE], 2))

        return cls(ascii_str)

    @classmethod
    def from_file(cls, filepath, encoding):
        """Create a new buffer from the contents of a file"""
        file_obj = open(filepath, 'r')
        raw = file_obj.read()
        file_obj.close()

        if encoding == 'b64':
            return cls.from_b64(raw)
        elif encoding == 'hex':
            return cls.from_hex(raw)
        elif encoding == 'bin':
            return cls.from_bin(raw)
        else:
            return cls(raw)

    @classmethod
    def from_mpz(cls, n_mpz):
        """ Create a new buffer from a gmpy2 arbitrary precision integer"""
        if n_mpz.num_digits(16) % 2 != 0:
            instr_hex = '0' + n_mpz.digits(16)
        else:
            instr_hex = n_mpz.digits(16)

        return cls.from_hex(instr_hex)

    @property
    def bytes(self):
        """Returns an array of buffer bytes"""
        return self._data.tolist()

    @property
    def size(self):
        """Returns the buffer size (bytes)"""
        return len(self._data)

    def get(self, index):
        """Get the byte value at index"""
        return self._data[index]

    def set(self, index, value):
        """Set the byte value at index"""
        self._data[index] = value

    def to_string(self):
        """Converts a buffer to an ASCII string"""
        return self._data.tostring()

    def to_b64(self):
        """Converts the buffer to a base64 encoded string"""
        return base64.b64encode(self.to_string())

    def to_hex(self):
        """Converts the buffer to a hex encoded string"""
        return binascii.hexlify(self.to_string())

    def to_bin(self):
        """Converts the buffer to a binary encoded string"""
        out_str = ''
        for byte in self._data:
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

        file_obj = open(filepath, 'w', 1)
        file_obj.write(out_data)
        file_obj.close()

    def to_mpz(self):
        """Transform the buffer to a GMP arbitrary precision integer"""
        return mpz(self.to_hex(), 16)

    def xor(self, buf):
        """Return XORed bytes of each buffer (up to size of current buffer)"""
        result = self.__class__.init(self.size)

        for i in range(self.size):
            result.set(i, self.get(i) ^ buf.get(i))

        return result

    def concat(self, buf):
        """Concatenate the buffer with another"""
        self._data.extend(buf.bytes)

        return self

    def map(self, func):
        """Map the buffer to a new buffer using a lambda"""
        raw_in = self._data
        out = self.__class__.init(self.size)

        for i in range(self.size):
            out.set(i, func(raw_in[i]))

        return out

    def copy(self):
        """Copy a buffer into a new instance and return it"""
        return self.__class__(self._data)
