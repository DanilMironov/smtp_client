import base64
import mimetypes
import re


class MakeEmail:

    @staticmethod
    def _make_sender_field(signature, laddr):
        sender = 'From: {0} <{1}>\r\n'.format(signature, laddr)
        return sender

    @staticmethod
    def _make_recipient_field(raddr):
        recipient = ''
        if len(raddr) == 1:
            recipient += 'To: ' + raddr[0]
        else:
            recipient += 'Cc: {0}'.format(raddr[0])
            raddr.remove(raddr[0])
            for addr in raddr:
                recipient += ', ' + addr
        recipient += '\r\n'
        return recipient

    @staticmethod
    def _make_subject_field(subject):
        subj = 'Subject: ' + subject + '\r\n'
        return subj

    @staticmethod
    def _make_other_field(laddr):
        other = 'MIME-Version: 1.0\r\n' \
                'Content-Transfer-Encoding: base64\r\n' \
                'Content-Type: text/plain; charset=utf-8\r\n' \
                'Return-Path: {0}\r\n' \
                '\r\n'.format(laddr)
        return other

    @staticmethod
    def _make_attachment(filename):
        cont_type = mimetypes.guess_type(filename)
        beg = '--kwak\r\n'.encode()
        # name = re.match(r'.+\\(.+?)$', filename).group(1)
        name = re.search(r'\\?([ _0-9а-яА-Я\w]+[^\\]\w+)?$',
                         filename).group(1)
        content = 'Content-Type: {0}; name="{1}"\r\n'\
            .format(cont_type.__getitem__(0), name).encode()
        charset = 'Content-Transfer-Encoding: base64\r\n'.encode()
        op = open(filename, 'rb')
        att = op.read()
        op.close()
        lala = base64.b64encode(att)
        return beg + content + charset + lala + b'\r\n'

    def create_multiple_email(self, message, signature,
                              laddr, raddr, files, subject=None):
        field = 'MIME-Version: 1.0\r\n' \
                'Content-Type: multipart/mixed; boundary="kwak"\r\n'.encode()
        sender = self._make_sender_field(signature, laddr).encode()
        recpt = self._make_recipient_field(raddr).encode()
        subj = self._make_subject_field(subject).encode()
        body1 = '\r\n--kwak\r\n' \
                'Content-Type: text/plain; charset=utf-8\r\n' \
                'Content-Transfer-Encoding: base64\r\n' \
                '\r\n'.encode()
        # message_words = message.split('\n')
        # new_words = []
        # for word in message_words:
        #     if word[0] == '.':
        #         word = word + '.'
        #     new_words.append(word)
        # print(new_words)
        # message = '\n'.join(new_words)
        # if message[0] == '.' and len(message) == 1:
        #     message += '.'
        # text = (base64.b64encode(message) + '\r\n').encode()
        text = base64.b64encode(message.encode())
        attachments = ''.encode()
        for element in files:
            attachment = self._make_attachment(element)
            attachments += attachment
        end = '--kwak--'.encode()
        email = field + sender + recpt + subj + \
            body1 + text + attachments + end
        return email

    def create_email(self, message: str, signature,
                     l_address, r_address, subject=None):
        sender = self._make_sender_field(signature, l_address)
        recipient = self._make_recipient_field(r_address)
        subj = self._make_subject_field(subject)
        other = self._make_other_field(l_address)
        form = sender + recipient + subj + other
        # print(type(form))
        # print(type(message))
        # message_words = message.split('\n')
        # new_words = []
        # for word in message_words:
        #     if word[0] == '.':
        #         word = word + '.'
        #     new_words.append(word)
        # print(new_words)
        # message = '\n'.join(new_words)
        print(message)
        email = form + base64.b64encode(message.encode()).decode()
        # email = form + message
        print(email)
        # print(base64.b64encode(message))
        return email
