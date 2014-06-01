#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import utils
from lib import errors

class Task(object):

    def __init__(self, job, task_data, task_vars):
        self.job = job
        self.task_vars = task_vars

        if 'action' not in task_data:
            raise errors.JobError('task must have action section')

        self.action = task_data.get('action')
        self.name = task_data['name'] if task_data.get('name', None) else self.action
        self.action = utils.template(self.action, task_vars)
        self.name = utils.template(self.name, task_vars)

        self.only_if = task_data.get('only_if', 'True')
        self.notify = task_data.get('notify', [])
        self.notified_by = []
        self.async_seconds = int(task_data.get('async', 0))
        self.async_poll_interval = int(task_data.get('poll', 0))

        self.with_items = task_data.get('with_items', [])

    def _extract_module_from_action(self):
        module_parts = self.action.split(None, 1)
        self._module_name = module_part[0]
        self._module_args = module_parts[1] if len(module_parts)>1 else None

    def get_module_name(self):
        if not self.hasattr('_module_name'):
            self._extract_module_from_action()

        return self._module_name

    def get_module_args(self):
        if not self.hasattr('_module_args'):
            self._extract_module_from_action()

        return self._module_args

    def get_module_vars(self):
        if not self.hasattr('_module_vars'):
            self._module_vars = list.__add__()

        return self._module_vars
