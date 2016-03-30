import socket
import struct
import xdrlib

from enum import Enum
from key_pair import KeyPair

# TODO extract to separate file and share with client
class Code(Enum):
    FIX_PARAMS
    KEY_EXCHG
    SEND_MSG
    RECV_MSG

class MessageServer(object):
    """Simple message server for encrypted communications
     using Diffie-Hellman key exchange"""

     TCP_IP = '127.0.0.1'
     TCP_PORT = 9090
     BUFFER_SIZE = 1024

     def __init__(self):
        self._keys = KeyPair()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((TCP_IP, TCP_PORT))
        sock.listen(1)

        conn, addr = sock.accept()

        while True:
            self._handle(conn)

    def _handle(self, conn):
        # Run through protocol...
        # 1 Fix parameters
        # 2 Exchange keys
        # 3 Send encrypted hello
        # 4 read encrypted reply

        # use pack/unpack for message transfer
        conn.close()

    def _fix_parameters(self, conn):
        """Fix the DH p, g parameters to use in key exchange"""
        msg_code = Code.FIX_PARAMS
        fixed_p = KeyPair.P_NIST.digits(16)
        fixed_g = KeyPair.G_NIST.digits(16)

        # Pack the data using xdrlib
        packer = xdrlib.Packer()
        packer.pack_int(msg_code)
        packer.pack_string(fixed_p)
        packer.pack_string(fixed_g)

        # Send the data
        conn.send(packer.get_buffer())

    def _key_exchange(self, conn):
        """Initiate a DH key exchange (send/receive public keys)"""
        msg_code = Code.KEY_EXCHG
        public_key = self._keys.get_public().to_hex()

        # Pack the data using xdrlib
        packer = xdrlib.Packer()
        packer.pack_int(msg_code)
        packer.pack_string(public_key)

        # Send the data
        conn.send(packer.get_buffer())

        # Read the client public key
        raw = xdrlib.Unpacker(conn.recv(self.BUFFER_SIZE))
        recv_code = raw.unpack_int()
        recv_pub = raw.unpack_string()

        if recv_code != Code.KEY_EXCHG
            raise AssertionError('Unexpected message code', recv_code)

        # Create the shared secret
        buf = Buffer.from_hex(recv_pub)
        self._session_secret = self._keys.session_key(buf)

    def _send_msg(self, conn):
        """Send an encrypted server hello"""


    def _read_msg(self, conn):
        """Receive the encrypted client response"""
