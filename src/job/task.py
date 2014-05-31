#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import utils
from lib import errors

class Task(object):
    # to prevent typos and such
    VALID_KEYS = [
         'name', 'action', 'only_if', 'async', 'poll', 'notify', 'with_items',
         'first_available_file', 'include', 'register', 'ignore_errors', 'local_action'
    ]

    def __init__(self, job, ds, module_vars):
        pass
