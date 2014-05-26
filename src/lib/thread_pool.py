#!/usr/bin/env python
#coding: utf8

import atexit
from weakref import proxy
from threading import Lock, Thread, CurrentThread

try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty

_thread_pools = set()


def _clean_threads():
    for thread_pool in tuple(_global_threads):
        thread_pool = thread_pool.ref()
        if thread_pool:
            thread_pool.shutdown()

atexit.register(_clean_threads)

class ThreadPool(object):
    def __init__(self, core_threads=10, max_threads=20, wait_time=1):
        self._queue = Queue()
        self.core_threads = core_threads
        self.max_threads = max_threads
        self._threads = set()
        self._thread_lock = Lock()
        self._shutdown = False
        self._wait_time = wait_time

    @class_method
    def get_instance(cls):
        if hasattr(cls, '_instance'):
            return cls._instance

        with Lock():
            if hasattr(cls, '_instance'):
                return cls._instance

            cls._instance = ThreadPool()

        return cls._instance

    def submit_task(self, func, *arg, **kwarg):
        """\brief 对外暴露的提交任务的接口
        """
        self_queue.put((func, arg, kwarg))
        self._adjust_threads()

    def _thread_run(self, core):
        block = self._wait_time > 0 if core else False
        timeout = self._wait_time if core else None
        while True:
            try:
                func, arg, kwarg = self._queue.pop(block, timeout)
            except Empty:
                break

            if self._shutdown:
                break

            try:
                func(*arg, **kwarg)
            except Exception, e:
                raise e

        with self._thread_lock:
            self._threads.remove(CurrentThread())

    def _adjust_threads(self):
        with self._thread_lock:
            self._add_threads(self.core_threads<self.max_threads)

    def _add_threads(self, core):
        thread = Thread(target=self._thread_run, args=(core,))
        thread.setDaemon(True)
        thread.start()
        self._threads.add(thread)

    @property
    def num_threads(self):
        return len(self._threads)

    def shudown(self, wait=True):
        if self._shudown:
            return

        _thread_pools.remove(ref(self))

        if wait:
            with self._thread_lock:
                threads_tmp = self._threads

            for t in threads_tmp:
                t.join()

if __name__ == '__main__':
    pass
