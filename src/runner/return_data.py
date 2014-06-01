#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

class ReturnData(object):
    def __init__(self, conn=None, host=None, result=None, comm_ok=True):
        self.conn = conn
        self.host = host
        self.result = result
        self.comm_ok = comm_ok


