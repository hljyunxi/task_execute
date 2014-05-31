#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import const

class JobWrap(object):
    def __init__(self, job_conf, setup_cache=const.DEFAULT_SETUP_CACHE):
        self.setup_cache = setup_cache
        self.job = self.load_from_job_conf(job_conf)
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

        return False

    def _do_setup_step(self, job):
        pass

    def run(self):
        self._do_setup_step(self.job)

        all_hosts = self.target.list_hosts(job.hosts)

    def _run_task(self):
        pass
