#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import const

class Target(object):

    def __init__(self, host_list=const.HOST_LIST):
        self.host_list  = host_list
        self.subset = None

    def get_groups(self):
        return self._groups

    def get_hosts(self):
        pass

    def fnmatch(self, pattern):
        pass


