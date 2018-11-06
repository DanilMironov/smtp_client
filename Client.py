import tkinter as tk
from SMTP import SMTP
from EmailMaker import MakeEmail
from MakeZip import Ziper
from FormRedactor import FormRedactor as fr

PASSWORD = ''
SERVERNAME = 'smtp.yandex.ru'
PORT = 587
MESSAGE = ''
SIGNATURE = ''
LADDR = ''
RADDR = []
PATH_LIST = []
SUBJECT = ''
ATTACHMENT = False


class AuthWindow:
    def __init__(self, master: tk.Tk):
        self.master = fr.make_window(master)
        self.master.title('SMTP')
        self.serv_field = fr.make_field(self.master, 'Server. Default: smtp.yandex.ru')
        self.port_field = fr.make_field(self.master, 'Port. Default: 587')
        self.log_field = fr.make_field(self.master, 'Login')
        self.pwd_field = fr.make_field(self.master, 'Password')
        self.connect_btn = fr.make_button(self.master, 'Connect', self.connect)

    def connect(self):
        global SERVERNAME, PORT, LADDR, PASSWORD
        n = fr.extract_info(self.serv_field)
        if len(n) != 0:
            SERVERNAME = n
        p = fr.extract_info(self.port_field)
        if len(p) != 0:
            PORT = int(p)
        LADDR = fr.extract_info(self.log_field)
        PASSWORD = fr.extract_info(self.pwd_field)
        new_window = tk.Toplevel(self.master)
        MainWindow(new_window)
        # print(PORT, SERVERNAME)
        # print(LADDR, PASSWORD)


class MainWindow:
    def __init__(self, master: tk.Toplevel):
        self.smtp = self.create_connection()
        self.master = fr.make_window(master, size_y=450)
        self.master.title('Writing a letter')
        self.raddr_field = fr.make_field(self.master, 'Recipient')
        self.subject_field = fr.make_field(self.master, 'Subject')
        self.signature_field = fr.make_field(self.master, 'Signature')
        self.message_field = fr.make_message_field(self.master)
        self.attachment_btn = fr.make_button(self.master, 'Make attachment', self.make_attachment)
        self.send_button = fr.make_button(self.master, 'Send', self.send)

    @staticmethod
    def create_connection():
        smtp_server = SMTP(SERVERNAME, PORT)
        smtp_server.helo()
        smtp_server.auth(LADDR, PASSWORD)
        smtp_server.indicate_the_sender(LADDR)
        return smtp_server

    def make_attachment(self):
        global ATTACHMENT
        if not ATTACHMENT:
            att_window = tk.Toplevel(self.master)
            AttachmentWindow(att_window)
            ATTACHMENT = True

    def send(self):
        email = MakeEmail()
        global MESSAGE, SIGNATURE, LADDR, RADDR, PATH_LIST, SUBJECT, ATTACHMENT
        MESSAGE = fr.extract_info(self.message_field)
        SIGNATURE = fr.extract_info(self.signature_field)
        RADDR = fr.extract_info(self.raddr_field, True)
        self.smtp.indicate_the_recipient(RADDR)
        SUBJECT = fr.extract_info(self.subject_field)
        if len(PATH_LIST) != 0:
            mail = email.create_multiple_email(MESSAGE, SIGNATURE, LADDR, RADDR, PATH_LIST, SUBJECT)
            self.smtp.send_email(mail, True)
        else:
            mail = email.create_email(MESSAGE, SIGNATURE, LADDR, RADDR, SUBJECT)
            self.smtp.send_email(mail)
        MESSAGE = ''
        SIGNATURE = ''
        LADDR = ''
        RADDR = []
        PATH_LIST = []
        SUBJECT = ''
        ATTACHMENT = False
        self.smtp.close()
        self.master.destroy()


class AttachmentWindow:
    def __init__(self, master: tk.Toplevel):
        self.master = fr.make_window(master)
        self.file_field = fr.make_field(self.master, "File's paths")
        self.zip_file_field = fr.make_field(self.master, 'Path to the file to archive')
        self.complete_btn = fr.make_button(self.master, 'Complete', self.complete)

    def complete(self):
        global PATH_LIST
        addr_to_zip = fr.extract_info(self.zip_file_field)
        if len(addr_to_zip) != 0:
            zip_path = Ziper.get_zip_path(addr_to_zip)
            PATH_LIST.append(zip_path)
        path_files = fr.extract_info(self.file_field, True)
        if len(path_files) != 0:
            for element in path_files:
                PATH_LIST.append(element)
        self.master.destroy()


def main():
    root = tk.Tk()
    AuthWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()

