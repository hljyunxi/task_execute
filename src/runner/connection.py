#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import utils
from lib import errors

import os.path
dirname = os.path.dirname(__file__)
modules = utils.import_plugins(os.path.join(dirname, 'connection_plugins'))

modules['paramiko'] = modules['paramiko_ssh']
del modules['paramiko_ssh']

class Connection(object):
    def __init__(self, runner):
        self.runner = runner

    def connect(self, host, port=None):
        conn = None
        module = modules.get(self.runner.transport, None)
        if module is None:
            raise errors.RunnerException('transport invalid')

        conn = module.Connection(self.runner, host, port)
        return conn.connect()
