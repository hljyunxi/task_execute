#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>


class AggregateStates(object):
    def __init__(self):
        self.processed = {}
        self.failures = {}
        self.ok = {}
        self.dark = {}


    def _increment(self, host):
        pass


    def compute_results(self, results):
        pass


    def summarize(self):
        pass

