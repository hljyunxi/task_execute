#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import errors

class BaseStore(object):

    def add_task(self, task):
        raise errors.NotImplementError

    def remove_task(self):
        raise errors.NotImplementError

    def update_task(self):
        raise errors.NotImplementError

    def load_tasks(self):
        raise errors.NotImplementError

    def close(self):
        pass
