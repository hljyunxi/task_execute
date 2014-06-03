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

    def _get_host(self, host_name):
        ret_host = None
        for g in self.get_groups():
            for h in g.get_hosts():
                if h.name == host_name:
                    ret_host = h
                    break
        return ret_host

    def get_host(self, host_name):
        if host_name not in self._host_cache:
            self._host_cache[host_name] = self._get_host(host_name)

        return self._host_cache[host_name]

    def get_groups(self):
        return self._groups

    def _get_hosts(self, patterns):
        by_pattern = {}
        for pattern in patterns:
            (name, _) = self._enumerate_info(pat)
            hpat = sorted(slef._host_inunenumerate_patterns(name), key=lambda h: h.name)
            by_pattern[pattern] = hpat

        ranged = {}
        for (pat, hosts) in by_pattern:
            ranged[pat] = self._apply_ranges(pat, hosts)

        return set(reduce(lambda x,y: x[1]+y[1], ranged, []))

    def _enumerate_info(self, pattern):
        if '[' not in pattern:
            return (pattern, None)
        (first, rest) = pattern.split('[')
        rest = rest.replace("]", "")
        if '-' not in rest:
            raise errors.TargetError('enumerate pattern format error')
        left, right = rest.split('-', 1)
        return (first, (left, right))

    def _apply_ranges(self, pat, hosts):
        name, limits = self._enumerate_info(pat)
        if not limits:
            return hosts
        left, right = limits
        enumerated = enumerate(hosts)
        hosts = [h for (i, h) in enumerated if i>=int(left) and i <=int(right)]
        return hosts

    def _hosts_in_unenumerate_patterns(self, pattern):
        hosts = {}
        for g in self.get_groups():
            for h in g.get_hosts():
                if pattern=='all' or self._match(g.name, pattern) or\
                        self._match(h.name, pattern):

                    hosts[h.name] = h

        return sorted(hosts.values(), key=lambda h: h.name)

    def get_hosts(self, pattern):
        patterns = pattern.replace(';', ':').split(':')
        positive_patterns = [p for p in patterns if not p.startswith("!")]
        negative_patterns = [p for p in patterns if p.startswith("!")]

        hosts = self._get_hosts(positive_patterns)

        if len(negative_patterns):
            exclude_hosts = self._get_hosts(negative_patterns)
            hosts = [h for h in hosts if h not in exclude_host]

        return sorted(hosts, lambda x: x.name)

    def list_hosts(self, pattern="all"):
        return [h.name for h in self.get_hosts(pattern)]

    def _match(self, str_obj, pattern):
        return fnmatch.fnmatch(str_obj, pattern)

    def is_file(self):
        if not isinstance(self.host_list, basestring):
            return False
        return os.path.exist(self.host_list)
