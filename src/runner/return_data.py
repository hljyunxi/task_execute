#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

class ReturnData(object):
    def __init__(self, conn=None, host=None, result=None, comm_ok=True):
        self.conn = conn
        if conn is not None:
            if hasattr(conn, 'host'):
                self.host = conn.host
            else:
                self.host = host
        else:
            self.host = host
        if self.host is None:
            raise RunnerError('returndata host is not set')

        self.result = result
        if self.result in [str, unicode]:
            self.result = utils.parse_json(self.result)

        self.comm_ok = comm_ok

    def comm_ok(self):
        return self.comm_ok

    def is_success(self):
        return self.comm_ok and ('failed' not in self.result and\
                self.result.get('rc', 0)==0)
