#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from threading import Thread, Event, Lock

from lib import errors, utils, const
import trigger

TRIGGER_MAP = {
    'simple': '_add_simple_job',
    'interval': '_add_interval_job',
}

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

        #1. 加载scheduler配置
        self._threadpool = ThreadPool(**const.DEFAULT_THREADPOOL_CONFIG)


        #2. 加载job配置文件
        yaml_data = utils.parse_yaml_from_file(self.job_file)
        assert isinstance(yaml_data, list), 'job config yaml file should be list'
        for job_config in yaml_data:
            job_wrap = JobWrap(job_config)
            trigger_type, kwargs = job_wrap.get_trigger()
            assert trigger_type in TRIGGER_MAP
            getattr(self, TRIGGER_MAP[trigger_type])(**kwargs)


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


    def _add_simple_job(self, **kwargs):
        pass


    def _add_interval_job(self, **kwargs):
        pass


    def _add_crontab_job(self, **kwargs):
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
        self._wakeup.clear()
        while not self._stopped:
            now = datetime.now()
            next_wakeup_time = self._process_jobs(now)

            if next_wakup_time:
                wait_seconds = time_difference(next_wakeup_time, now)
                self._wakeup.wait(wait_seconds)
                self._wakeup.clear()
            elif self.standalone:
                self.shutdown()
                break
            else:
                self._wakeup.wait()
                self._wakeup.clear()

    def _process_jobs(self):
        next_wakeup_time = None
        self._jobstore_lock.acquire()

        try:
            for name, store in self._job_stores:
                for job in store.get_jobs():
                    run_times = job.get_run_times(now)
                    if run_times:
                        self._threadpool.submit(self._run_job, job, run_times)

                        if job.compute_next_run_time(now+timedelta(seconds=1)):
                            jobstore.update_job(job)
                        else:
                            self._remove_job(jobstore, job)

                    if not next_wakeup_time:
                        next_wakeup_time = job.next_run_time
                    else:
                        next_wakeup_time = min(next_wakeup_time, job.next_run_time)
        finally:
            self._jobstore.release()


    def _remove_job(self, store, job):
        store.remove_job(job)


    def _run_job(self, job, run_times):
        for i in run_times:
            try:
                ret_val = job.run()
            except:
                pass


    def get_jobs(self):
        jobs = []
        with self._jobstore_lock:
            for store in self.job_store:
                jobs.extend(store.get_jobs())

        return jobs
