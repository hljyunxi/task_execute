#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import utils
from lib import errors

class Job(object):

    def __init__(self,
        host_list = const.DEFAULT_HOST_LIST,
        sudo = False,
        sudo_user = const.DEFAULT_SUDO_USER,
        extra_vars = None,
        trigger = None):

        for x in ds.keys():
            if not x in Job.VALID_KEYS:
                raise errors.JobError('%s not valid in Job' % x)

        self._ds = ds

        if 'hosts' not job_conf:
            raise errors.JobError('job conf must have hosts section')
        self.remote_user  = utils.template(ds.get('user', job_wrap.remote_user), job_wrap.extra_vars)
        self.remote_port  = ds.get('port', job_wrap.remote_port)
        self.sudo         = ds.get('sudo', job_wrap.sudo)
        self.sudo_user    = ds.get('sudo_user', job_wrap.sudo_user)
        self.transport    = ds.get('connection', job_wrap.transport)

        self.vars = self._get_vars(ds, job_wrap)

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
                data = utils.parse_yaml_from_file(utils.path_dwim(self.job_wrap.basedir, include_file))
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
            self._tasks = self._load_tasks(self._ds.get('tasks', []))
        return self._task

    def handlers(self):
        if not self.hasattr('_handlers'):
            self._handlers= self._load_tasks(self._ds.get('handlers', []))
        return self._handlers

    def _get_vars(self, ds, job_wrap):
        vars = job_wrap.global_vars.copy()

        vars_ds = ds.get('vars', {})

        if type(vars_ds) not in [dict, list]:
            raise errors.JobError("'vars' section must contain only key/value paris")
        if type(vars_ds) == list:
            for item in vars_ds:
                k,v = item.iteritems()[0]
                vars[k] = v
        else:
            vars.update(vars_ds)

        vars.update(job_wrap.extra_vars)
        return vars
