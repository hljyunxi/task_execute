#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>


class Connection(object):
    def __init__(self, runner, host, port):
        self.runner = runner
        self.host = host
        self.port = port


