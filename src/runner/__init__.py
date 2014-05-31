#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import const
from lib import errors

class Runner(object):
    def __init__(self, task, hosts):
        self.task = task

        if not hosts:
            raise errors.



