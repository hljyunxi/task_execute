#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import const

class JobRunner(object):
    def __init__(self,
        host_list = const.DEFAULT_HOST_LIST,
        setup_cache = const.DEFAULT_SETUP_CACHE,
        trigger = None):
        this.setup_cache = setup_cache
        self.trigger = trigger

    def _do_setup_step(self, job):
        pass

    def _load_job_from_file(self, job_file):
        pass
