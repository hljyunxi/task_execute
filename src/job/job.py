#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import utils

class Job(object):
    VALID_KEYS = [

    ]

    def __init__(self, job_runner, ds):
        for x in ds.keys():
            if not x in Job.VALID_KEYS:
                raise errors.JobError('%s not valid in Job' % x)

        hosts = ds.get('hosts')
        if hosts is None:
            raise errors.JobError('hosts is required in Job')
        if isinstance(hosts, list):
            hosts = ';'.join(hosts)

        hosts = utils.template(hosts, runner.extra_vars)

        self._ds = ds
        self.job_runner = job_runner
        self._tasks = ds.get('tasks', [])
        self._handlers = ds.get('handlers', [])

        self._tasks = self._load_tasks(self._ds, 'tasks')
        self._handlers = self._load_tasks(self._ds, 'handlers')

    def _load_tasks(self, ds, keyname):

    def tasks(self):
        return self._tasks

    def handlers(self):
        return self._hanlders
