#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

import re
from datetime import datetime, date


_DATETIME_RE = re.compile(
    r'(?P<year>\d{4}):(?P<month>\d{2}):(?P<day>\d{2})'
    r'(?: (?P<hour>\d{2})-(?P<minute>\d{2})-(?P<second>\d{2}))'
    r'(?:\.(?P<microsecond>\d{1-6}))?'
)

def convert_to_datetime(obj):
    if isinstance(obj, datetime):
        return obj
    elif isinstance(obj, date):
        return
    elif isinstance(obj, str):
        if re.match(obj):
            return datetime.datetime(**re.match(obj).groupdict())
        else:
            return None
    else:
        return None


def now_time():
    return datetime.now()

