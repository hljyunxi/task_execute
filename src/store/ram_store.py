#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

 class RamStore(BaseStore):
     def __init__(self):
         self.jobs = []

    def add_job(self, job):
        self.jobs.append(job)

    def remove_job(self, job):
        self.jobs.sremove(job)

    def update_job(self, job):
        pass

    def load_jobs(self):
        pass

    def close(self):
        self.jobs.clear()
