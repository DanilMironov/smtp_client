import argparse
from EmailMaker import MakeEmail
from SMTP import SMTP
from MakeZip import Ziper


class Main:

    def __init__(self):
        self.parser = self.create_parser().parse_args()

    @staticmethod
    def create_parser():
        parser = argparse.ArgumentParser(description='SMTP-client.')
        parser.add_argument('-s', '--ssl', action='store_true',
                            help='If you want create the safe connection'
                                 ' you can use it')
        parser.add_argument('-t', '--test', action='store_true',
                            help='If you want to test the program')
        parser.add_argument('-srv', '--server',
                            default='smtp.yandex.ru',
                            type=str,
                            help='To send the letter '
                                 'you must enter the servername. '
                                 'Default: smtp.yandex.ru')
        parser.add_argument('-p', '--port', default=587, type=int,
                            help='To send the letter you '
                                 'must enter the port. '
                                 'Default: 587')
        parser.add_argument('-mu', '--multi', action='store_true',
                            help='If you want to add attachment')
        parser.add_argument('-html', '--html', action='store_true',
                            help='If you want to send the html-page '
                                 'you should use this key. \n'
                                 'ATTENTION!>>>>Sending html-page '
                                 'is impossible without key "-mu/--multi"')
        parser.add_argument('-z', '--zip', action='store_true',
                            help='If you want to send the zip archive. \n'
                                 'ATTENTION!>>>Sending zip is '
                                 'impossible withount key "-mu/--multi"')
        parser.add_argument('-sbj', '--subject', default='', type=str,
                            help='If the subject of mail too long to print '
                                 'you can add filename from where '
                                 'to read the subject')
        parser.add_argument('-m', '--message', default='', type=str,
                            help='If the message too long '
                                 'you can add filename '
                                 'from where to read the text')
        return parser

    def identify_serv(self):
        servername = self.parser.server
        port = self.parser.port
        serv = SMTP(servername, port)
        return serv

    @staticmethod
    def _get_recipient():
        return input('Enter the recipient. "." means the end of the input\n')

    @staticmethod
    def make_list_recip():
        recip_list = []
        while True:
            recipient = Main._get_recipient()
            if recipient == '.':
                break
            recip_list.append(recipient)
        return recip_list

    @staticmethod
    def _get_attachment():
        return Main._indicate('Please enter the path to the file '
                              'of attachment("." means the end of input)')

    @staticmethod
    def make_attachment_list(path_list):
        while True:
            path = Main._get_attachment()
            if path == '.':
                break
            path_list.append(path)
        return path_list

    @staticmethod
    def make_ssl(ssl: bool, serv, sender, passwd):
        if ssl:
            serv.auth(sender, passwd)
        else:
            return

    @staticmethod
    def _indicate(in_text: str):
        return input(in_text + '\n')

    @staticmethod
    def indicate_zip():
        return Main._indicate('Please enter the path to the file '
                              'you want to archive')

    @staticmethod
    def indicate_signature():
        return Main._indicate('Enter you signature')

    @staticmethod
    def indicate_sender():
        return Main._indicate('Enter your login')

    @staticmethod
    def indicate_pwd():
        return Main._indicate('Enter your password')

    @staticmethod
    def indicate_some(some: str, in_text: str):
        if len(some) == 0:
            thing = Main._indicate(in_text)
        else:
            op = open(some)
            thing = op.read()
            op.close()
        return thing

    @staticmethod
    def app_zip(path_list):
        zip_addr = Main.indicate_zip()
        zip_path = Ziper.get_zip_path(zip_addr)
        path_list.append(zip_path)
        return path_list

    @staticmethod
    def tadaam(serv: SMTP, multi, is_zip,
               text, signature, sender,
               recip_list, subject):
        em = MakeEmail()
        path_list = []
        if multi:
            if is_zip:
                Main.app_zip(path_list)
            Main.make_attachment_list(path_list)
            message = em.create_multiple_email(text, signature, sender,
                                               recip_list, path_list, subject)
            serv.send_email(message, True)
        else:
            message = em.create_email(text, signature, sender,
                                      recip_list, subject)
            serv.send_email(message)
        serv.close()

    @staticmethod
    def main():
        main = Main()
        server = main.identify_serv()
        server.helo()
        sender = Main.indicate_sender()
        password = Main.indicate_pwd()
        Main.make_ssl(main.parser.ssl, server, sender, password)
        server.indicate_the_sender(sender)
        recip_list = Main.make_list_recip()
        server.indicate_the_recipient(recip_list)
        subject = Main.indicate_some(main.parser.subject,
                                     'Enter the subject of mail')
        signature = Main.indicate_signature()
        text = Main.indicate_some(main.parser.message, 'Enter the text')
        Main.tadaam(server,
                    main.parser.multi,
                    main.parser.zip,
                    text, signature,
                    sender, recip_list, subject)


if __name__ == '__main__':
    Main.main()
