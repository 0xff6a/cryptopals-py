import socket

from Crypto.Cipher import AES
from Crypto import Random
from gmpy2 import mpz

from key_pair import KeyPair
from message import Message
from utils.buffer import Buffer

class MessageClient(object):
    """Simple message client for encrypted communications
     using Diffie-Hellman key exchange"""

     SERVER_IP = '127.0.0.1'
     SERVER_PORT = 9090
     BUFFER_SIZE = 1024
     AES_IV_SIZE = 16

     def __init__(self, message):
        """Connect to the message server and perform a secure echo exchange"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TCP_IP, TCP_PORT))

        self._message = message
        self._check_echo(sock)

    def _check_echo(self, sock):
        # Run through protocol...
        # 1) Fix parameters
        self._fix_parameters(sock)

        # 2) Exchange keys
        self._key_exchange(sock)

        # 3) Send an encrypted message
        self._send_msg(sock)

        # 4) Read the encrypted echo reply
        self._read_echo(sock)

        sock.close()

    def _fix_parameters(self, sock):
        """Receive the DH p, g parameters to generate a key pair"""
        raw = sock.recv(BUFFER_SIZE)
        recv_msg = Message.from_buffer(raw)

        assert recv_msg['code'] == Message.FIX_PARAMS,
            'Unexpected message code during key exchange: %d' % recv_msg['code']

        dh_p = mpz(recv_msg['dh_p'])
        dh_g = mpz(recv_msg['dh_g'])

        self._keys = KeyPair(dh_p, dh_g)

    def _key_exchange(self, sock):
        """Initiate a DH key exchange (receive/send public keys)"""
        # Read the server public key
        raw = sock.recv(self.BUFFER_SIZE)
        recv_msg = Message.from_buffer(raw)

        assert recv_msg['code'] == Message.KEY_EXCHG,
            'Unexpected message code during key exchange: %d' % recv_msg['code']

        # Create the shared secret
        buf = Buffer.from_hex(recv_msg['public_key'])
        self._session_secret = self._keys.session_key(buf)

        # Send back client public key
        public_key = self._keys.get_public().to_hex()

        # Create the message object with client public key
        msg = Message(Message.KEY_EXCHG, public_key=public_key)

        # Send the message buffer
        conn.send(msg.buffer)

    def _send_msg(self, sock):
        """Send an encrypted message to the server"""
        # Encrypt the message with AES
        iv = Random.new().read(self.AES_IV_SIZE)
        cipher = AES.new(self._session_secret, AES.MODE_CBC, iv)
        ciphertext = iv
        ciphertext += cipher.encrypt(self._message)

        # Create the message object with encoded message
        msg = Message(Message.RECV_ENC, client_msg=ciphertext)

        # Send the message buffer
        sock.send(msg.buffer)

    def _read_echo(self, sock):
        """Receive the encrypted server echo response"""
        raw = sock.recv(self.BUFFER_SIZE)
        recv_msg = Message.from_buffer(raw)

        assert recv_msg['code'] == Message.SEND_ENC,
            'Unexpected message code during receive: %d' % recv_msg['code']

        ciphertext = recv_msg['server_msg']

        assert len(ciphertext) > self.AES_IV_SIZE , 'Invalid server message size'

        # Decrypt the received ciphertext using AES-CBC (16-bit IV prepended)
        iv = ciphertext[0:self.AES_IV_SIZE]
        ciphertext = ciphertext[self.AES_IV_SIZE:]
        cipher = AES.new(self._session_secret, AES.MODE_CBC, iv)

        # Check the decrypted message matches
        echo_msg = cipher.decrypt(ciphertext)
        assert echo_msg == self._message, "Decrypted echo response did not match"
        print "[*] Successful echo..."
