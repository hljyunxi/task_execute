#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import const
from lib import errors

class Host(object):
    def __init__(self, name=None, port=None):
        if self.name is None:
            raise errors.TargetError('host name must be specified')
        self.name = name
        self.groups = []

    def add_group(self, group):
        self.groups.append(group)

    def get_groups(self):
        results = {}
        for g in self.groups:
            results[g.name] = g
            for a in g.get_ancestors():
                results[a.name] = a

        return results.values()
