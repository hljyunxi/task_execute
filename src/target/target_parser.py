#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import const
from lib import errors

class TargetParser(object):
    def __init__(self, file_name=const.DEFAULT_HOST_LIST):
        self.file_name = file_name

    def _parse(self):
        all = Group(name="all")
        self._groups = all
        self._hosts = {}

        lines = open(self.file_name).readlines()

        self._parse_groups(lines)
        self._parse_group_children(lines)

    def _parse_groups(self, lines):
        active_group_name = None
        for line in lines:
            line = line.strip()
            if line.startswith("["):
                active_group_name = line.replace('[', "").replace(']', "").strip()
            elif line.startswith("#") or line.strip()=='':
                pass
            elif active_group_name:

            else:
                raise errors.TargetError('host file format error')

    def _parse_group_children(self, lines):
        group = None
        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith('[') and line.find(":children]") != -1:
                line = line.replace("[", "").replace(":children]", "")
                group = self.groups.get(line, None)
                if group is None:
                    raise errors.TargetError('group is not specified')
            elif line.starswith('#'):
                continue
            elif line.startswith('['):
                group = None
            elif group:
                kid_group = self.groups.get(line, None)
                if kid_group is None:
                    raise errors.TargetError('child group is not specified')
                else:
                    group.add_child_group(kid_group)

    def get_groups(self):
        if not hasattr(self, '_groups'):
            self._parse()

        return self._groups

    def get_hosts(self):
        if not hasattr(self, '_hosts'):
            self._parse()

        return self._hosts
