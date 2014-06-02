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
        self.child_groups.append(group)
        group.depth += 1
        self.parent_group.append(self)

    def add_host(self, host):
        self.hosts.append(host)
        host.add_group(self)

    def get_hosts(self):
        hosts = []
        for child_group in self.child_groups:
            hosts.extend(child_groups.get_hosts())
        hosts.extend(self.hosts)
        return hosts

    def _get_ancestors(self):
        results = {}
        for g in self.parent_groups:
            results[g.name] = g
            results.update(g.get_ancestors())

        return results

    def get_ancesotrs(self):
        ancestors = self._get_ancestors()
        return ancestors.values()
