#!/usr/bin/python
#coding: utf8
#author: chenyunyun<hljyunxi@gmail.com>

import getpass
import smtplib
from email.mime.text import MIMEText
import socket

class EmailException(Exception): pass

class Emailer(object):
    def __init__(self, smtp_host):
        self.smtp_host = smtp_host

    @property
    def from_addr(self):
        user = getpass.getuser()
        hostname = socket.gethostname()
        return '@'.join((user, hostname))

    def send(self, to_addr, subject, context):
        msg = MIMEText(context)
        msg['Subject'] = subject
        ms['To'] = to_addr

        host_ports = self.smtp_host.split(":")
        host = host_ports.pop(0)
        port = host_ports.pop(0) if host_ports else 25

        s = smtplib.SMTP()
        s.connect(host, port)
        s.sendmail(self.from_addr, to_addr, msg.as_string())
        s.close()

if __name__ == "__main__":
    pass
