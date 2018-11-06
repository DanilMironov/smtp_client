import socket
import ssl
import base64


class SMTP:

    def __init__(self, servername, port):
        self._server = (servername, port)
        self.sock = self._init_socket(self._server)
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.connect(self._server)
        self.list_of_recip = list()

    @staticmethod
    def _init_socket(address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        data = (sock.recv(1024)).decode()
        if data.split(' ')[0] != '220':
            raise Exception('Can not connect to the server')
        sock.sendall('STARTTLS\r\n'.encode())
        data = (sock.recv(1024)).decode()
        if data.split(' ')[0] != '220':
            raise Exception('Can not start tls or server does not support the secure connection')
        sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_SSLv23)
        return sock

    def _send_data(self, message, is_byte=False):
        if is_byte:
            self.sock.sendall(message + b'\r\n')
        else:
            self.sock.sendall((message + '\r\n').encode())

    def _rec_data(self):
        d = []
        while True:
            data = self.sock.recv(1024)
            d.append(data.decode())
            if len(data) < 1024:
                break
        data = ''.join(d)
        return data

    def auth(self, login, password):
        self._send_data('AUTH LOGIN')
        self.sock.recv(1024)
        login = base64.b64encode(login.encode())
        password = base64.b64encode(password.encode())
        self.sock.sendall(login + b'\r\n')
        self.sock.recv(1024)
        self.sock.sendall(password + b'\r\n')
        data = self._rec_data()
        if data.split(' ')[0] != '235':
            raise Exception('Authentification failed!(INCORRECT LOGIN OR PASSWORD)')

    def helo(self):
        self._send_data('EHLO user')
        data = self._rec_data()
        if data.split('-')[0] != '250':
            raise Exception("Server is not responding.")

    def indicate_the_sender(self, sender):
        self._send_data('MAIL FROM:<{}>'.format(sender))
        data = self._rec_data()
        if data.split(' ')[0] != '250':
            raise Exception('Incorrect name of sender or need a secure connection(ssl)! Try again.')

    def indicate_the_recipient(self, list_of_recipients):
        for recipient in list_of_recipients:
            self._send_data('RCPT TO:<{}>'.format(recipient))
            data = self._rec_data()
            if data.split(' ')[0] != '250':
                raise Exception('Incorrect name of recipient! Try again.')

    def send_email(self, email, is_bytes=False):
        self._send_data('DATA')
        data = self._rec_data()
        if data.split(' ')[0] != '354':
            raise Exception('Error. ')
        self._send_data(email, is_bytes)
        self._send_data('.')
        data = self._rec_data()
        if data.split(' ')[0] != '250':
            raise Exception("The letter didn't go")

    def close(self):
        self._send_data('QUIT')
        self.sock.close()

