import socket

class MessageServer(object):
    """Simple message server for encrypted communications
     using Diffie-Hellman key exchange"""

     TCP_IP = '127.0.0.1'
     TCP_PORT = 9090
     BUFFER_SIZE = 1024

     def __init__(self, port):
        self.__sock = socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind((TCP_IP, TCP_PORT))
        self.__sock.listen(1)

        conn, addr = self.__sock.accept()

        while True:
            self.handle(conn)

    def handle(self, conn):
        # Run through protocol...
        # 1 Fix parameters
        # 2 Exchange keys
        # 3 Send encrypted hello
        # 4 read encrypted reply
        conn.close()

    def __fix_parameters(self, conn):
        # Determine the p, g parameters to use in key exchange

    def __key_exchange(self, conn):
        # Initiate DH key exchange

    def __send_msg(self, conn):
        # Send encrypted message

    def __read_msg(self, conn):
        # Receive encrypted reply
