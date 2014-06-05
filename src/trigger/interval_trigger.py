#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from datetime import datetime, timedelta

class IntervalTrigger(object):
    def __init__(self, interval, start_date=None):
        if not isinstance(interval, timedelta):
            raise errors.TriggerError('interval must be timedelta')

        self.interval = interval
        self.interval_seconds = time_seconds(interval)
        if self.interval_seconds == 0:
            self.interval = timedelta(seconds=1)
            self.interval_seconds = 1

        if start_date:
            self.start_date = convert_to_datetime(start_date)
        else:
            self.start_date = datetime.now() + self.interval

    def get_next_fire_time(self, start_date):
        if start_date < self.start_date:
            return self.start_date

        total_seconds = time_seconds(datetime.now() - self.start_date)

        return self.start_date + ceil(total_seconds/self.interval_seconds)*self.interval_seconds

    def __str__(self):
        return 'interval[%s]' % str(self.interval)

    def __repr__(self):
        return '<%s(%s, %s)>' % (self.__class__.__name__,
                repr(self.interval), repr(self.start_date))
