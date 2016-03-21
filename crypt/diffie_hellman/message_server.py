import socket
import struct

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
        self.__keys = KeyPair()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((TCP_IP, TCP_PORT))
        sock.listen(1)

        conn, addr = sock.accept()

        while True:
            self.__handle(conn)

    def __handle(self, conn):
        # Run through protocol...
        # 1 Fix parameters
        # 2 Exchange keys
        # 3 Send encrypted hello
        # 4 read encrypted reply

        # use pack/unpack for message transfer
        conn.close()

    def __fix_parameters(self, conn):
        """Fix the DH p, g parameters to use in key exchange"""
        msg_code = Code.FIX_PARAMS
        fixed_p = KeyPair.P_NIST.digits(16)
        fixed_g = KeyPair.G_NIST.digits(16)
        format_str = 'i' + len(fixed_p) + 's' + len(fixed_g) + 's'

        data = struct.pack(format_str, msg_code, fixed_p, fixed_g)
        conn.send(data)

    def __key_exchange(self, conn):
        """Initiate a DH key exchange (send/receive public keys)"""
        msg_code = Code.KEY_EXCHG
        public_key = self.__keys.get_public().to_hex()
        format_str = 'i' + len(public_key) + 's'
        data = struct.pack(format_str, msg_code, public_key)

        conn.send(data)

        raw = conn.recv(self.BUFFER_SIZE)
        recv_code, recv_pub = struct.unpack(format_str, raw)

        if recv_code != Code.KEY_EXCHG
            raise AssertionError('Unexpected message code', recv_code)

        buf = Buffer.from_hex(recv_pub)
        self.__session_secret = self.__keys.session_key(buf)

    def __send_msg(self, conn):
        """Send an encrypted server hello"""


    def __read_msg(self, conn):
        """Receive the encrypted client response"""
