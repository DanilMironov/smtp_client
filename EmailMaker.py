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
                'Content-Transfer-Encoding: 8bit\r\n' \
                'Content-Type: text/plain; charset=utf-8\r\n' \
                'Return-Path: {0}\r\n' \
                '\r\n'.format(laddr)
        return other

    @staticmethod
    def _make_attachment(filename):
        cont_type = mimetypes.guess_type(filename)
        beg = '--kwak\r\n'.encode()
        name = re.match(r'.+\\(.+?)$', filename).group(1)
        content = 'Content-Type: {0}; name="{1}"\r\n'.format(cont_type.__getitem__(0), name).encode()
        charset = 'Content-Transfer-Encoding: base64\r\n'.encode()
        op = open(filename, 'rb')
        att = op.read()
        op.close()
        lala = base64.b64encode(att)
        return beg + content + charset + lala + b'\r\n'

    def create_multiple_email(self, message, signature, laddr, raddr, files, subject=None):
        field = 'MIME-Version: 1.0\r\n' \
                'Content-Type: multipart/mixed; boundary="kwak"\r\n'.encode()
        sender = self._make_sender_field(signature, laddr).encode()
        recpt = self._make_recipient_field(raddr).encode()
        subj = self._make_subject_field(subject).encode()
        body1 = '\r\n--kwak\r\n' \
                'Content-Type: text/plain; charset=utf-8\r\n' \
                'Content-Transfer-Encoding: 8bit\r\n' \
                '\r\n'.encode()
        text = (message + '\r\n').encode()
        attachments = ''.encode()
        for element in files:
            attachment = self._make_attachment(element)
            attachments += attachment
        end = '--kwak--'.encode()
        email = field + sender + recpt + subj + body1 + text + attachments + end
        return email

    def create_email(self, message, signature, laddr, raddr, subject=None):
        sender = self._make_sender_field(signature, laddr)
        recpt = self._make_recipient_field(raddr)
        subj = self._make_subject_field(subject)
        other = self._make_other_field(laddr)
        form = sender + recpt + subj + other
        email = form + message
        return email

