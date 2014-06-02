#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

import os

from lib import const
from lib import errors

class Target(object):

    def __init__(self, host_list=const.HOST_LIST):
        self.host_list  = host_list
        self._host_cache = {}

        if type(host_list) in [str, unicode]:
            if host_list.find(',') != -1:
                host_list = host_list.split(',')
                host_list = [h.strip() for h in host_list]

        if type(host_list) == list:
            all = Group('all')
            self._groups = [all]
            for x in host_list:
                if x.find(':') != -1:
                    tokens = x.split(':')
                    all.add_host(Host(tokens[0], tokens[1]))
                else:
                    all.add(Host(x))
        else:
            self.parser = TargetParser(self.host_list)
            self._groups = self.parser.get_groups()

    def get_groups(self):
        return self._groups

    def _get_hosts(self, pattern):
        pass

    def get_hosts(self, pattern):
        patterns = pattern.replace(';', ':').split(':')

    def list_hosts(self, pattern="all"):
        return [h.name for h in self.get_hosts(pattern)]

    def fnmatch(self, pattern):
        pass

    def is_file(self):
        if not isinstance(self.host_list, basestring):
            return False
        return os.path.exist(self.host_list)
