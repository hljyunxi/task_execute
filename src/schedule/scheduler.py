#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from threading import Thread, Event, Lock

from lib import errors, utils
import trigger

class Scheduler(object):
    _thread = None
    _initialized = False
    _stopped = True

    def __init__(self, job_file):
        self._pending_jobs = []
        self._started = False
        self._jobstore_lock = Lock()
        self._threadpool = None
        self._job_file = job_file

    @proptery
    def running(self):
        thread_alive = self._thread and self._thread.isAlive()
        standalone = getattr(self, 'standalone', False)
        return not self.stopped and (thread_alive or standalone)


    def initialize(self):
        if self.running:
            raise errors.SchedulerError('schedulre already running')

        yaml_data = utils.parse_yaml_from_file(self.job_file)
        assert isinstance(yaml_data, dict), 'job config yaml file should be dict'

        self._initialized = True


    def start(self):
        if self.running:
            raise errors.SchedulerError('already started')

        if not self._initialized:
            raise errors.SchedulerError('scheduler not initialized')

        self._stopped = False


    def stop(self, stop_jobstore=True, stop_threadpool=True):
        if not self.running:
            raise errors.Scheduler('job not running')

        self._stopped = True

        if stop_threadpool:
            self._threapool.shutdown()

        self._thread:
            self._thread.join()

        if stop_jobstore:
            for store in self._job_stores:
                store.stop()

    def _add_interval_job(self):
        pass


    def _add_crontab_job(self):
        pass


    def add_job_store(self, jobstore, alias):
        with self._jobstore_lock:
            if alias in self._job_stores:
                raise errors.SchedulerError('jobstore %s already added' % alias)
            self._job_stores[alias] = jobstore


    def remove_job_store(self, alias, close=True):
        with self._jobstore_lock:
            if alias not in self._job_stores:
                raise errors.SchedulerError('jobstore %s not in scheduler' % alias)

            jobstore = self._job_stores.pop(alias)

        if close:
            job_store.close()


    def _main_loop(self):
        while not self._stopped:
            pass


    def _process_jobs(self):
        pass


    def get_jobs(self):
        jobs = []
        with self._jobstore_lock:
            for i in self.job_store:
                jobs.extend(i.get_jobs())

        return jobs
