import xdrlib

class Message(object):
    """Message class for our Diffie-Hellman key exchange protocol"""
    FIX_PARAMS = 1
    KEY_EXCHG = 2
    SEND_ENC = 3
    RECV_ENC = 4

    def __init__(self, code, **data_items):
        """Initialize the message with a code and data items (variable length)"""
        self.code = code
        self._packed = None
        self._unpacked = data_items

        if code == self.FIX_PARAMS:
            self._fix_params(data_items)
        elif code == self.KEY_EXCHG:
            self._key_exchg(data_items)
        elif code == self.SEND_ENC:
            self._send_enc(data_items)
        elif code == self.RECV_ENC:
            self._recv_enc(data_items)
        else:
            raise AssertionError('Unknown message code', code)

    @classmethod
    def from_buffer(cls, data):
        """Build a message construct from a string buffer"""


    @property
    def buffer(self):
        """Returns a buffer from the packed message data"""
        if self._packed is None:
            raise LookupError('No packed data')

        return self._packed.get_buffer()

    @property
    def data(self):
        """Returns a dictionary of all the message data items"""
        data_dict = dict(self._unpacked)
        data_dict['code'] = self.code

        return data_dict

    def _fix_params(self, data_items):
        """Pack the data for a FIX_PARAMS message"""
        if len(data_items) != 2:
            raise AssertionError('Invalid arguments for FIX_PARAMS message')

        # Pack the data using xdrlib
        packer = xdrlib.Packer()
        packer.pack_int(self.FIX_PARAMS)
        packer.pack_string(data_items['dh_p'])
        packer.pack_string(data_items['dh_g'])

        self._packed = packer

    def _key_exchg(self, data_items):
        """Pack the data for a KEY_EXCHG message"""
        if len(data_items) != 1:
            raise AssertionError('Invalid arguments for KEY_EXCHG message')

        # Pack the data using xdrlib
        packer = xdrlib.Packer()
        packer.pack_int(self.KEY_EXCHG)
        packer.pack_string(data_items['public_key'])

        self._packed = packer
