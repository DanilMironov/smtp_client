from FormRedactor import FormRedactor as fred
from EmailMaker import MakeEmail
from MakeZip import Ziper
from unittest.mock import MagicMock, patch
from SMTP import SMTP
from TestServer import TestServer
import unittest
import base64
import tkinter as tk
import zipfile
import os
import socket


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

    # def test_make_zip_folder(self):
    #     lil_zip = Ziper()
    #     folder_addr = os.getcwd() + '\\test_folder'
    #     exp_zip_path = '{}.zip'.format(folder_addr)
    #     os.mkdir(folder_addr)
    #     file_addr = folder_addr + '\\filename.txt'
    #     with open(file_addr, 'w') as file_in_folder:
    #         file_in_folder.write('Открывают чемодан, а там бобики')
    #     lil_zip.make_zip(folder_addr, exp_zip_path, True)
    #     with open(exp_zip_path, 'r') as zip_file:
    #         data = zip_file.read()
    #     self.assertIsNotNone(data)

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
        SMTP._init_socket = MagicMock(return_value='socket')
        smtp = SMTP('servername', 123)
        self.assertEqual(smtp._server, ('servername', 123))
        self.assertEqual(smtp.sock, 'socket')
        self.assertIsInstance(smtp.list_of_recip, list)


if __name__ == '__main__':
    unittest.main()

