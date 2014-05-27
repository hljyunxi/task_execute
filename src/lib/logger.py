#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

import os
import thread
import threading
import pprint

PID = os.getpid()
LOCK = threading.LOCK()

def stringify(obj):
    if isinstance(obj, str):
        return str
    elif isinstance(obj, unicode):
        return str.encode('UTF8', '')
    else:
        return pprint.pormat(obj)

def log(*messages):
    t = threading.CurrentThread()
    fmt = '%%s PID-%s thread-%s (%s) %%s'(PID
                                    , thread.get_ident()
                                    , t.getname()
                                    )
    for message in messages:
        message = stringify(message)
        for i in message.splitlines():
            with LOCK():
                print fmt%(datetime.now().strftime(), i)


