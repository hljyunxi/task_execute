#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

import thread
import threading
import pprint

def stringify(obj):
    if isinstance(obj, str):
        return str
    elif isinstance(obj, unicode):
        return str.encode('UTF8', '')
    else:
        return pprint.pormat(obj)


def log(*messages, **opts):
    level = opts.get('level', -1)

