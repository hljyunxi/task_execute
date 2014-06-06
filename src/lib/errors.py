#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

class NotImplementError(Exception):
    pass

class JobError(Exception):
    pass

class RunnerError(Exception):
    pass

class ConnectionError(Exception):
    pass

class TargetError(Exception):
    pass

class TemplateError(Exception):
    pass

class SchedulerError(Exception):
    pass
