#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import errors

def has_range(line):
    if (not line.startswith('[') and
        line.find('[') != -1 and
        line.find(':') != -1 and
        line.find(']') != -1 and
        line.index("[") < line.index(":") < line.index("]")):

        return True
    else:
        return False

def expand_range(line):
    all_hosts = []
    if line:
        head, nrange, tail = line.replace('[', '|').replace(']', '|').split('|')

        bounds = nrange.split(":")
        if len(bounds)!=2:
            raise errors.TargetError('nrange format error')
        begin, end = bounds
        if not begin:
            begin = 0
        if not end:
            raise errors.TargetError('end bound should not be none')

        for _ in range(int(begin), int(end)+1):
            all_hosts.append(''.join(head, str(_), tail))

    return all_hosts
