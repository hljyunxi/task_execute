#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import utils
from lib import errors

class Task(object):

    def __init__(self, job, ds):
        self.job = job

        if 'action' not in ds:
            raise errors.JobError('task must have action section')

        self.action = ds.get('action')
        self.name = ds['name'] if ds.get('name', None) else self.action
        self.action = utils.template(self.action, job.module_vars)
        self.name = utils.template(self.name, job.module_vars)

        self.only_if = ds.get('only_if', 'True')
        self.notify = ds.get('notify', [])
        self.notified_by = []
        self.async_seconds = int(ds.get('async', 0))
        self.async_poll_interval = int(ds.get('poll', 0))


    def module_vars(self):
        if not self.hasattr('_module_vars'):
            self.

