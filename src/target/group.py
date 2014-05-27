#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

class Group(object):
    __slots__ = ['name', 'hosts', 'vars', 'child_groups', 'parent_groups', 'depth']

    def __init__(self, name=None):
        self.name = name
        self.depth = 0

