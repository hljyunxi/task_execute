#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import const

class JobRunner(object):
    def __init__(self,
        host_list = const.DEFAULT_HOST_LIST,
        setup_cache = const.DEFAULT_SETUP_CACHE,
        sudo = False,
        sudo_user = const.DEFAULT_SUDO_USER,
        extra_vars = None,
        trigger = None):

        this.setup_cache = setup_cache
        self.trigger = trigger

    def _do_setup_step(self, job):
        pass

    def load_job_from_job_conf(self, job_conf):
        if type(job_conf) != dict:
            raise errors.JobError('job conf data must be dict')

        job = None
        if 'include' in job_conf:
            if len(job_conf) != 1:
                raise errors.JobError('job conf error: include should only have\
                        only one item')
            else:
                job = self.load_job_from_file(job_conf['include'])
        else:
            job = Job(self, job_conf)

        return job

    def load_job_from_file(self, job_file):
        yaml_data = utils.parse_yaml_from_file(job_file)
        assert type(yaml_data) is dict, "job yaml file should be dict"
        return Job(self, yaml_data)

    def run(self):
        self._do_setup_step(self.job)

        all_hosts = self.target.list_hosts(job.hosts)

    def _run_task(self):
        pass
