from FormRedactor import FormRedactor as fred
from EmailMaker import MakeEmail
from MakeZip import Ziper
from unittest.mock import MagicMock, patch
from SMTP import SMTP
from Main import Main
from Client import AuthWindow, AttachmentWindow
import argparse
import unittest
import base64
import tkinter as tk
import os
import socket
import ssl


class TestEmailMaker(unittest.TestCase):
    def test_sender_field(self):
        signature = 'Steve Jobs'
        laddr = 'stevejobs1998@mail.ru'
        expectation = 'From: Steve Jobs <stevejobs1998@mail.ru>\r\n'
        reality = MakeEmail._make_sender_field(signature, laddr)
        self.assertEqual(expectation, reality)

    def test_subject_field(self):
        subject = 'Theme'
        expectation = 'Subject: Theme\r\n'
        reality = MakeEmail._make_subject_field(subject)
        self.assertEqual(expectation, reality)

    def test_recipient_field_with_one_recipient(self):
        raddr = ['mironovd1999@gmail.com']
        expectation = 'To: mironovd1999@gmail.com\r\n'
        reality = MakeEmail._make_recipient_field(raddr)
        self.assertEqual(expectation, reality)

    def test_recipient_field_with_few_recipient(self):
        raddr = ['mironovd1999@gmail.com', 'mironovd1999@yandex.ru']
        expectation = 'Cc: mironovd1999@gmail.com, mironovd1999@yandex.ru\r\n'
        reality = MakeEmail._make_recipient_field(raddr)
        self.assertEqual(expectation, reality)

    def test_mail_with_one_recip(self):
        em = MakeEmail()
        list_of_recipient = ['mironovd1999@gmail.com']
        form = em.create_email('сообщение', 'Данил', 'mironovd1999@yandex.ru', list_of_recipient, 'тема')
        expectation = 'From: Данил <mironovd1999@yandex.ru>\r\n' \
                      'To: mironovd1999@gmail.com\r\n' \
                      'Subject: тема\r\n' \
                      'MIME-Version: 1.0\r\n' \
                      'Content-Transfer-Encoding: 8bit\r\n' \
                      'Content-Type: text/plain; charset=utf-8\r\n' \
                      'Return-Path: mironovd1999@yandex.ru\r\n' \
                      '\r\n' \
                      'сообщение'
        self.assertEqual(form, expectation)

    def test_mail_with_several_recip(self):
        em = MakeEmail()
        list_of_recipient = ['mironovd1999@gmail.com', 'mironovd1999@yandex.ru']
        form = em.create_email('сообщение', 'Данил', 'mironovd1999@yandex.ru', list_of_recipient, 'тема')
        expectation = 'From: Данил <mironovd1999@yandex.ru>\r\n' \
                      'Cc: mironovd1999@gmail.com, mironovd1999@yandex.ru\r\n' \
                      'Subject: тема\r\n' \
                      'MIME-Version: 1.0\r\n' \
                      'Content-Transfer-Encoding: 8bit\r\n' \
                      'Content-Type: text/plain; charset=utf-8\r\n' \
                      'Return-Path: mironovd1999@yandex.ru\r\n' \
                      '\r\n' \
                      'сообщение'
        self.assertEqual(form, expectation)

    def test_multiple_mail(self):
        em = MakeEmail()
        list_of_recipient = ['mironovd1999@gmail.com', 'mironovd1999@yandex.ru']
        list_of_files = [r'C:\Users\я\Desktop\шукстов.jpg']
        message = 'abracadabra'
        sender = 'mironovd1999@yandex.ru'
        subject = 'Theme'
        signature = 'Danil'
        beginning_field = 'MIME-Version: 1.0\r\n' \
                          'Content-Type: multipart/mixed; boundary="kwak"\r\n'.encode()
        sender_place = 'From: Danil <mironovd1999@yandex.ru>\r\n'.encode()
        recipient_place = 'Cc: mironovd1999@gmail.com, mironovd1999@yandex.ru\r\n'.encode()
        subject_place = 'Subject: Theme\r\n'.encode()
        other_place = '\r\n--kwak\r\n' \
                     'Content-Type: text/plain; charset=utf-8\r\n' \
                     'Content-Transfer-Encoding: 8bit\r\n' \
                     '\r\n'.encode()
        text = 'abracadabra\r\n'.encode()
        bound = '--kwak\r\n'.encode()
        op = open(list_of_files[0], 'rb')
        att = op.read()
        op.close()
        att = base64.b64encode(att)
        cont_type = 'Content-Type: image/jpeg; name="шукстов.jpg"\r\n'.encode()
        enc = 'Content-Transfer-Encoding: base64\r\n'.encode()
        expectation = beginning_field + \
                      sender_place + \
                      recipient_place + \
                      subject_place + \
                      other_place +\
                      text + \
                      bound + cont_type + enc + att + b'\r\n' + '--kwak--'.encode()
        reality = em.create_multiple_email(message, signature, sender, list_of_recipient, list_of_files, subject)
        self.assertEqual(expectation, reality)


class TestFormRedactor(unittest.TestCase):

    def test_make_button(self):
        def command():
            pass
        root = tk.Tk()
        text = 'blalala'
        btn = fred.make_button(root, text, command)
        self.assertIsInstance(btn, tk.Button)

    def test_make_field(self):
        root = tk.Tk()
        text_label = 'abracadabra'
        field = fred.make_field(root, text_label)
        self.assertIsInstance(field, tk.Text)

    def test_make_message_field(self):
        root = tk.Tk()
        message_field = fred.make_message_field(root)
        self.assertIsInstance(message_field, tk.Text)

    def test_make_window(self):
        root = tk.Tk()
        window = fred.make_window(root)
        self.assertIsInstance(window, tk.Tk)

    def test_extract_info(self):
        expectation = 'abracadabra'
        text = tk.Text()
        text.insert(1.0, 'abracadabra')
        result = fred.extract_info(text)
        self.assertEqual(expectation, result)

    def test_extract_list_info(self):
        expectation = ['abr', 'aca', 'dab', 'ra']
        text = tk.Text()
        text.insert(1.0, 'abr\naca\ndab\nra')
        result = fred.extract_info(text, True)
        self.assertEqual(expectation, result)


class TestMakeZip(unittest.TestCase):

    def test_make_zip(self):
        file = open('filename.txt', 'w')
        file.write('abracadabra')
        file.close()
        lil_zip = Ziper()
        lil_zip.make_zip('filename.txt', 'filename.zip')
        os.remove('filename.txt')
        with open('filename.zip', 'r') as zip_file:
            data = zip_file.read()
        os.remove('filename.zip')
        self.assertIsNotNone(data)

    def test_make_zip_folder(self):
        lil_zip = Ziper()
        folder_addr = os.getcwd() + '\\test_folder'
        exp_zip_path = '{}.zip'.format(folder_addr)
        os.mkdir(folder_addr)
        file_addr = folder_addr + '\\filename.txt'
        with open(file_addr, 'w') as file_in_folder:
            file_in_folder.write('Открывают чемодан, а там бобики')
        lil_zip.make_zip(folder_addr, exp_zip_path, True)
        with open(exp_zip_path, 'r') as zip_file:
            data = zip_file.read()
        self.assertIsNotNone(data)

    def test_get_zip_path(self):
        lil_zip = Ziper()
        with open('filename.txt', 'w') as file:
            file.write('abracadabra')
        address = 'filename.txt'
        expectation = 'filename.zip'
        result = lil_zip.get_zip_path(address)
        os.remove(address)
        os.remove(expectation)
        self.assertEqual(expectation, result)


class TestSMTP(unittest.TestCase):
    def test_init(self):
        SMTP._init_socket = MagicMock(return_value=socket.socket())
        smtp = SMTP('servername', 123)
        self.assertEqual(smtp._server, ('servername', 123))
        self.assertIsInstance(smtp.sock, socket.socket)
        self.assertIsInstance(smtp.list_of_recip, list)

    def test_socket(self):
        socket.socket.connect = MagicMock()
        socket.socket.recv = MagicMock(return_value='220'.encode())
        socket.socket.sendall = MagicMock()
        ssl.wrap_socket = MagicMock(return_value=socket.socket())
        result = SMTP._init_socket('address')
        self.assertIsInstance(result, socket.socket)

    def test_rec_data(self):
        socket.socket.recv = MagicMock(return_value=''.encode())
        expectation = ''
        smtp = SMTP('address', 9090)
        result = smtp._rec_data()
        self.assertEqual(expectation, result)

    def test_indicate_sender(self):
        SMTP._init_socket = MagicMock(return_value=socket.socket())
        socket.socket.recv = MagicMock(return_value='250 '.encode())
        SMTP._send_data = MagicMock()
        smtp = SMTP('servername', 9090)
        self.assertIsNone(smtp.indicate_the_sender('sender'))

    def test_indicate_sender_exception(self):
        SMTP._init_socket = MagicMock(return_value=socket.socket())
        SMTP._send_data = MagicMock()
        smtp = SMTP('servername', 9090)
        socket.socket.recv = MagicMock(return_value='350 '.encode())
        try:
            self.assertIsNone(smtp.indicate_the_sender('sender'))
        except Exception as ex:
            self.assertRaises(Exception, ex)

    def test_indicate_recipient(self):
        SMTP._init_socket = MagicMock(return_value=socket.socket())
        SMTP._send_data = MagicMock()
        socket.socket.recv = MagicMock(return_value='250 '.encode())
        smtp = SMTP('servername', 9090)
        list_of_recipients = ['recipient']
        self.assertIsNone(smtp.indicate_the_recipient(list_of_recipients))

    def test_indicate_recipient_except(self):
        socket.socket.recv = MagicMock(return_value='350 '.encode())
        smtp = SMTP('servername', 9090)
        list_of_recipients = ['recipient']
        try:
            self.assertIsNone(smtp.indicate_the_recipient(list_of_recipients))
        except Exception as ex:
            self.assertRaises(Exception, ex)

    def test_send_email(self):
        socket.socket.recv = MagicMock(return_value='354 '.encode())
        smtp = SMTP('servername', 9090)
        try:
            self.assertIsNone(smtp.send_email('abracadabra'))
        except Exception as exep:
            self.assertRaises(Exception, exep)

    def test_send_email_except(self):
        socket.socket.recv = MagicMock(return_value='350 '.encode())
        smtp = SMTP('servername', 9090)
        try:
            self.assertIsNone(smtp.send_email('abracadabra'))
        except Exception as exep:
            self.assertRaises(Exception, exep)

    def test_helo(self):
        SMTP._send_data = MagicMock()
        SMTP._init_socket = MagicMock(return_value=socket.socket())
        socket.socket.recv = MagicMock(return_value='251-12'.encode())
        smtp = SMTP('servername', 9090)
        try:
            self.assertIsNone(smtp.helo())
        except Exception as excep:
            self.assertRaises(Exception, excep)

    def test_close(self):
        SMTP._init_socket = MagicMock(return_value=socket.socket())
        socket.socket.sendall = MagicMock()
        socket.socket.close = MagicMock()
        smtp = SMTP('servername', 9090)
        self.assertIsNone(smtp.close())

    def test_auth(self):
        SMTP._init_socket = MagicMock(return_value=socket.socket())
        socket.socket.sendall = MagicMock()
        socket.socket.recv = MagicMock(return_value='230 ')
        base64.b64encode = MagicMock(return_value='data')
        smtp = SMTP('servername', 9090)
        try:
            self.assertIsNone(smtp.auth('login', 'password'))
        except Exception as excep:
            self.assertRaises(Exception, excep)


class TestMain(unittest.TestCase):
    def test_make_parser(self):
        result = Main.create_parser()
        self.assertIsInstance(result, argparse.ArgumentParser)

    def test_make_list_recip(self):
        Main._get_recipient = MagicMock(return_value='.')
        result = Main.make_list_recip()
        expectation = []
        self.assertEqual(result, expectation)

    def test_make_attachment_list(self):
        Main._get_attachment = MagicMock(return_value='.')
        path_list = []
        result = Main.make_attachment_list(path_list)
        expectation = []
        self.assertEqual(result, expectation)

    def test_make_ssl(self):
        result = Main.make_ssl(False, 'serv', 'so', 's')
        self.assertIsNone(result)

    def test_make_ssl_true(self):
        SMTP.auth = MagicMock()
        serv = SMTP._init_socket = MagicMock()
        result = Main.make_ssl(True, serv, 'sender', 'pasw')
        self.assertIsNone(result)

    def test_indicate_some_none(self):
        Main._indicate = MagicMock(return_value=None)
        result = Main.indicate_some('', 'text')
        self.assertIsNone(result)

    def test_indicate_some_not_none(self):
        with open('fff.txt', 'w') as file:
            file.write('abracadabra')
        result = Main.indicate_some('fff.txt', 'blabla')
        os.remove('fff.txt')
        self.assertEqual(result, 'abracadabra')

    def test_tadaam(self):
        SMTP._send_data = MagicMock(return_value=None)
        Main._indicate = MagicMock(return_value='.')
        SMTP.send_email = MagicMock(return_value=None)
        SMTP._init_socket = MagicMock(return_value=socket.socket())
        serv = SMTP('a', 555)
        socket.socket.close = MagicMock(return_value=None)
        result = Main.tadaam(serv, False, False, 'text', 'signature',
                             'sender', ['recipient'], 'subject')
        self.assertIsNone(result)

    def test_tadaam_with_multi(self):
        Main.app_zip = MagicMock(return_value=None)
        Main._get_attachment = MagicMock(return_value='.')
        SMTP.send_email = MagicMock(return_value=None)
        SMTP._init_socket = MagicMock(return_value=socket.socket())
        serv = SMTP('a', 555)
        socket.socket.close = MagicMock(return_value=None)
        MakeEmail._make_attachment = MagicMock(return_value='abcd'.encode())
        result = Main.tadaam(serv, True, True, 'text', 'signature',
                             'sender', ['recipient'], 'subject')
        self.assertIsNone(result)

    def test_indicate_signature(self):
        Main._indicate = MagicMock(return_value=42)
        result = Main.indicate_signature()
        self.assertEqual(result, 42)

    def test_indicate_zip(self):
        Main._indicate = MagicMock(return_value=42)
        result = Main.indicate_zip()
        self.assertEqual(result, 42)

    def test_indicate_pwd(self):
        Main._indicate = MagicMock(return_value=42)
        result = Main.indicate_pwd()
        self.assertEqual(result, 42)

    def test_indicate_sender(self):
        Main._indicate = MagicMock(return_value=42)
        result = Main.indicate_sender()
        self.assertEqual(result, 42)


class TestClient(unittest.TestCase):
    def test_init_auth_win(self):
        win = tk.Tk()
        result = AuthWindow(win)
        self.assertIsInstance(result.pwd_field, tk.Text)

    def test_init_att_win(self):
        level = tk.Toplevel()
        result = AttachmentWindow(level)
        self.assertIsInstance(result.complete_btn, tk.Button)


if __name__ == '__main__':
    unittest.main()

