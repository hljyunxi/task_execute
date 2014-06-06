#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from threading import Thread, Event, Lock

from lib import errors, utils

class Scheduler(object):
    _thread = None
    _stopped = True

    def __init__(self, job_file, config_file):
        self._pending_jobs = []
        self._started = False
        self._jobstore_lock = Lock()
        self._threadpool = None

    @proptery
    def running(self):
        thread_alive = self._thread and self._thread.isAlive()
        standalone = getattr(self, 'standalone', False)
        return not self.stopped and (thread_alive or standalone)

    def initialize(self):
        if self.running:
            raise errors.SchedulerError('schedulre already running')

        yaml_data = utils.parse_yaml_from_file(self.config_file)

    def start(self):
        if self._started:
            raise errors.SchedulerError('already started')

    def stop(self, stop_jobstore=True, stop_threadpool=True):
        if not self.running:
            raise errors.Scheduler('job not running')

        if stop_threadpool:
            self._threapool.shutdown()

        self._thread:
            self._thread.join()

        if stop_jobstore:
            for store in self._job_stores:
                store.stop()

    def _add_job(self):
        pass

    def add_job_store(self):
        pass

    def _main_loop(self):
        pass

    def _process_job(self):
        pass
