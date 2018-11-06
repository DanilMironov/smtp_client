from EmailMaker import MakeEmail
from SMTP import SMTP
import argparse
from MakeZip import Ziper


def main():
    parser = argparse.ArgumentParser(description='SMTP-client.')
    parser.add_argument('-s', '--ssl', action='store_true',
                        help='If you want create the safe connection you can use it')
    parser.add_argument('-t', '--test', action='store_true',
                        help='If you want to test the program')
    parser.add_argument('-srv', '--server', default='smtp.yandex.ru', type=str,
                        help='To send the letter you must enter the servername. '
                             'Default: smtp.yandex.ru')
    parser.add_argument('-p', '--port', default=587, type=int,
                        help='To send the letter you must enter the port. '
                             'Default: 587')
    parser.add_argument('-mu', '--multi', action='store_true',
                        help='If you want to add attachment')
    parser.add_argument('-html', '--html', action='store_true',
                        help='If you want to send the html-page you should use this key. \n'
                             'ATTENTION!>>>>Sending html-page is impossible without key "-mu/--multi"')
    parser.add_argument('-z', '--zip', action='store_true',
                        help='If you want to send the zip archive. \n'
                             'ATTENTION!>>>Sending zip is impossible withount key "-mu/--multi"')
    parser.add_argument('-sbj', '--subject', default='', type=str,
                        help='If the subject of mail too long to print '
                             'you can add filename from where to read the subject')
    parser.add_argument('-m', '--message', default='', type=str,
                        help='If the message too long you can add filename from where to read the text')
    pars = parser.parse_args()
    servername = pars.server
    port = pars.port
    serv = SMTP(servername, port)
    serv.helo()
    sender = input('Enter your login:\n')
    password = input('Enter your password:\n')
    if pars.ssl:
        serv.auth(sender, password)
    serv.indicate_the_sender(sender)
    recip_list = []
    while True:
        recipient = input('Enter the recipient. "." means the end of the input')
        if recipient == '.':
            break
        recip_list.append(recipient)
    serv.indicate_the_recipient(recip_list)
    if len(pars.subject) == 0:
        subject = input('Enter the subject of mail:\n')
    else:
        op = open(pars.subject)
        subject = op.read()
        op.close()
    signature = input('Enter you signature:\n')
    if len(pars.message) == 0:
        text = input('Enter the text:\n')
    else:
        op = open(pars.message)
        text = op.read()
        op.close()
    em = MakeEmail()
    path_list = []
    if pars.multi:
        if pars.zip:
            zip_addr = input('Please enter the path to the file you want to archive\n')
            zip_path = Ziper.get_zip_path(zip_addr)
            path_list.append(zip_path)
        while True:
            path = input('Please enter the path to the file of attachment("." means the end of input)\n')
            if path == '.':
                break
            path_list.append(path)
        message = em.create_multiple_email(text, signature, sender, serv.list_of_recip, path_list, subject)
        serv.send_email(message, True)
    else:
        message = em.create_email(text, signature, sender, serv.list_of_recip, subject)
        serv.send_email(message)
    serv.close()


if __name__ == '__main__':
    main()

