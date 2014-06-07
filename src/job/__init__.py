#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import errors
from lib import const

class JobWrap(object):
    def __init__(self, job_conf,
            hosts_file=const.DEFAULT_HOST_FILE,
            setup_cache=const.DEFAULT_SETUP_CACHE):

        #保存配置相关信息，以便于序列化
        self._job_conf = job_conf

        #连接相关信息
        self._conn_config = job_conf.get('conn_config', {})

        #trigger相关
        self._trigger_config = job_conf.get('trigger_config', {})

        self.target = Target(hosts_file)
        self.job = self.load_job_from_job_conf(job_config.get('job_config', {}))
        self.setup_cache = setup_cache
        self.stats = AggreateStats()

    def load_job_from_job_conf(self, job_conf):
        if type(job_conf) != dict:
            raise errors.JobError('job conf data must be dict')

        job = None
        if 'include' in job_conf:
            if len(job_conf) != 1:
                raise errors.JobError('job conf error: include should only have'
                        'only one item')
            else:
                job = self.load_job_from_file(job_conf['include'])
        else:
            if not self._check_job_conf(job_conf):
                raise  errors.JobError('job conf error')
            job = Job(self, **job_conf)

        return job

    def load_job_from_file(self, job_file):
        yaml_data = utils.parse_yaml_from_file(job_file)
        assert type(yaml_data) is dict, "job yaml file should be dict"
        if not self._check_job_conf(yaml_data):
            raise  errors.JobError('job conf error')
        return Job(self, **yaml_data)

    def _check_job_conf(self, job_conf):
        assert type(job_conf) is dict, "job_conf must be dict"
        for i in job_conf:
            if x not in Job.VALID_KEYS:
                raise error.JobError('{0} not is not valid'.format(x))
        return True


    def run(self):
        all_hosts = self.target.list_hosts(self.job.hosts)

        for h in all_hosts:
            for task in self.job.tasks():
                self._run_task(task, h)

            for handler in self.job.handlers():
                if len(handlers.notified_by) > 0:
                    self._run_task(handler, handler.notified_by, is_handler=True)


    def _run_task(self, task, hosts):
        if not isinstance(hosts, list):
            hosts = [hosts]

        results = self._run_task_internal(task, hosts)
        if results is None:
            results = {}

        self.stats.compute(results, ignore_errors=task.ignore_errors)

        if len(self.notify)>0:
            for host, results in results.get('contacted',{}).iteritems():
                if results.get('changed', False):
                    for handler_name in task.notify:
                        self._flag_handler(play.handlers(), utils.template(handler_name, task.module_vars), host)

    def _flag_handler(self, handlers, handler_name, host):
        found = False
        for x in handlers:
            if handler_name == x.name:
                found = True
                x.notified_by.append(host)
        if not found:
            raise errors.JobError('change handler (%s) is not defined' % handler_name)

    def _run_task_internal(self, task, hosts):
        runner = Runner(
        )

        results = runner.run()

        return results

    def get_next_run_time(self):
        pass
