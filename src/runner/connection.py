#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import utils
from lib import errors

import os.path
dirname = os.path.dirname(__file__)
modules = utils.import_plugins(os.path.join(dirname, 'connection_plugins'))


class Connection(object):
    def __init__(self, runner):
        self.runner = runner

    def connect(self, host, port=None):
        pass
