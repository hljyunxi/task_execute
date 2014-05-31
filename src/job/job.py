#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import utils
from lib import errors

class Job(object):
    VALID_KEYS = [
       'hosts', 'name', 'vars', 'vars_prompt', 'vars_files',
       'tasks', 'handlers', 'user', 'port', 'include',
       'sudo', 'sudo_user', 'connection', 'tags', 'gather_facts', 'serial'
    ]

    def __init__(self, job_runner, ds):
        for x in ds.keys():
            if not x in Job.VALID_KEYS:
                raise errors.JobError('%s not valid in Job' % x)

        self._ds = ds
        self.job_runner = job_runner

        hosts = ds.get('hosts')
        if hosts is None:
            raise errors.JobError('hosts is required in Job conf')
        if isinstance(hosts, list):
            hosts = ';'.join(hosts)
        self.hosts = utils.template(hosts, job_runner.extra_vars)

        self.remote_user  = utils.template(ds.get('user', job_runner.remote_user), job_runner.extra_vars)
        self.remote_port  = ds.get('port', job_runner.remote_port)
        self.sudo         = ds.get('sudo', job_runner.sudo)
        self.sudo_user    = ds.get('sudo_user', job_runner.sudo_user)
        self.transport    = ds.get('connection', job_runner.transport)
        self._tasks_data  = ds.get('tasks', [])
        self._handlers_data = ds.get('handlers', [])

        self.vars = self._get_vars(ds, job_runner)

        if self.sudo_user != 'root':
            self.sudo = True

    def _load_tasks(self, tasks):
        results = []
        for x in tasks:
            task_vars = vars.copy()
            if 'include' in x:
                tokens = shlex.split(x['include'])
                for t in tokens[1:]:
                    (k,v) = t.split("=", 1)
                    task_vars[k] = utils.template(v, task_vars)
                include_file = utils.template(tokens[0], task_vars)
                data = utils.parse_yaml_from_file(utils.path_dwim(self.job_runner.basedir, include_file))
            elif type(x) == dict:
                data = [x]
            else:
                raise Exception("unexpected task type")

            for y in data:
                mv = task_vars.copy()
                results.append(Task(self,y,module_vars=mv))

        return results

    def tasks(self):
        if not self.hasattr('_tasks'):
            self._tasks = self._load_tasks(self._tasks_data)
        return self._task

    def handlers(self):
        if not self.hasattr('_handlers'):
            self._handlers= self._load_tasks(self._handlers_data)
        return self._handlers

    def _get_vars(self, ds, job_runner):
        vars_ds = ds.get('vars', {})

        if type(vars_ds) not in [dict, list]:
            raise errors.JobError("'vars' section must contain only key/value paris")

        vars = job_runner.global_vars

        if type(vars_ds) == list:
            for item in vars_ds:
                k,v = item.iteritems()[0]
                vars[k] = v
        else:
            vars.update(vars_ds)

        vars.update(job_runner.extra_vars)
        return vars
