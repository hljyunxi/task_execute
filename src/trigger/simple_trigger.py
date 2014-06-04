#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

class SimpleTrigger(object):
    def __init__(self, run_date):
        self.run_date = run_date

    def get_next_fire_time(self, start_date):
        if self.run_date > start_date:
            return self.run_date

    def __str__(self):
        return '[date]%s' % str(self.run_date)

    def __repr__(self):
        return '<%s(run_date=%s)>' % (self.__class__.__name__,\
                str(self.run_date))
