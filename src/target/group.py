#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import errors

class Group(object):
    __slots__ = ['name', 'hosts', 'vars', 'child_groups', 'parent_groups', 'depth']

    def __init__(self, name=None):
        self.name = name
        self.child_groups = []
        self.parent_groups = []
        self.hosts = []
        self.depth = 0

    def add_child_group(self, group):
        if self == group:
            raise errors.TargetError('cannt add group to itself')

