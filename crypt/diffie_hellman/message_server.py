import socket
import struct
import xdrlib

from enum import Enum
from Crypto.Cipher import AES
from key_pair import KeyPair
from message import Message

class MessageServer(object):
    """Simple message server for encrypted communications
     using Diffie-Hellman key exchange"""

     TCP_IP = '127.0.0.1'
     TCP_PORT = 9090
     BUFFER_SIZE = 1024
     AES_IV_SIZE = 16

     def __init__(self):
        """Initialize a DH key pair and start listening for client connections"""
        self._keys = KeyPair()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((TCP_IP, TCP_PORT))
        sock.listen(1)

        conn, addr = sock.accept()

        while True:
            self._handle(conn)

    def _handle(self, conn):
        # Run through protocol...
        # 1) Fix parameters
        self._fix_parameters(conn)

        # 2) Exchange keys
        self._key_exchange(conn)

        # 3) Read encrypted msg
        self._read_msg(conn)

        # 4) Echo encrypted reply
        self._echo_msg(conn)

        conn.close()

    def _fix_parameters(self, conn):
        """Fix the DH p, g parameters to use in key exchange"""
        fixed_p = KeyPair.P_NIST.digits(16)
        fixed_g = KeyPair.G_NIST.digits(16)

        # Create the message object with our DH parameters
        msg = Message(Message.FIX_PARAMS, dh_p=fixed_p, dh_g=fixed_g)

        # Send the message buffer
        conn.send(msg.buffer)

    def _key_exchange(self, conn):
        """Initiate a DH key exchange (send/receive public keys)"""
        public_key = self._keys.get_public().to_hex()

        # Create the message object with server public key
        msg = Message(Message.KEY_EXCHG, public_key=public_key)

        # Send the message buffer
        conn.send(msg.buffer)

        # Read the client public key
        raw = conn.recv(self.BUFFER_SIZE)
        recv_msg = Message.from_buffer(raw)

        assert recv_msg['code'] != Message.KEY_EXCHG,
            'Unexpected message code during key exchange: %d' % recv_msg['code']

        # Create the shared secret
        buf = Buffer.from_hex(recv_msg['public_key'])
        self._session_secret = self._keys.session_key(buf)

    def _read_msg(self, conn):
        """Receive the encrypted client response"""
        raw = conn.recv(self.BUFFER_SIZE)
        recv_msg = Message.from_buffer(raw)

        assert recv_msg['code'] == Message.RECV_ENC,
            'Unexpected message code during receive: %d' % recv_msg['code']

        ciphertext = recv_msg['client_msg']

        assert len(ciphertext) <= AES_IV_SIZE , 'Invalid client message size'

        # Decrypt the received ciphertext using AES-CBC (16-bit IV prepended)
        iv = ciphertext[0:AES_IV_SIZE]
        ciphertext = ciphertext[AES_IV_SIZE:]
        cipher = AES.new(self._session_secret, AES.MODE_CBC, iv)

        # Store the decrypted message and IV
        self._iv = iv
        self._echo_msg = cipher.decrypt(ciphertext)

    def _echo_msg(self, conn):
        """Send an encrypted server echo response"""
        # Re-encrypt the echo message
        cipher = AES.new(self._session_secret, AES.MODE_CBC, self._iv)
        ciphertext = self._iv
        ciphertext += cipher.encrypt(self._echo_msg)

        # Create the message object with encoded echo message
        echo_msg = Message(Message.SEND_ENC, server_msg=ciphertext)

        # Send the message buffer
        conn.send(echo_msg.buffer)
