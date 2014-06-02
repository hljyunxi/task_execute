#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import const
from lib import errors

class TargetParser(object):
    def __init__(self, file_name=const.DEFAULT_HOST_LIST):
        self.file_name = file_name

    def _parse(self):
        lines = open(self.file_name).readlines()
        self._parse_groups(lines)
        self._parse_group_children(lines)

    def _parse_groups(self, lines):
        all = Group(name="all")
        self._groups = all
        self._hosts = {}

        active_group_name = None
        for line in lines:
            if line.startswith("["):
                active_group_name = line.replace('[', "").replace(']', "").strip()
            elif line.startswith("#") or line.strip()=='':
                pass
            elif active_group_name:

            else:
                raise errors.TargetError('host file format error')


    def _parse_group_children(self, lines):
        pass

    def get_groups(self):
        if not hasattr(self, '_groups'):
            self._parse()

        return self._groups

    def get_hosts(self):
        if not hasattr(self, '_hosts'):
            self._parse()

        return self._hosts
