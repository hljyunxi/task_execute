#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from threading import Thread, Event, Lock

from lib import errors

class Scheduler(object):
    def __init__(self, job_file, config_file):
        self._pending_jobs = []
        self._started = False

    def initialize(self):
        pass

    def start(self):
        if self._started:
            raise errors.SchedulerError('already started')

    def stop(self):
        pass

    def _add_job(self):
        pass

    def add_job_store(self):
        pass

    def _main_loop(self):
        pass

    def _process_job(self):
        pass
