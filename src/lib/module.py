#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

class ResolvingError(Exception):
    pass


def get_callable_name(func):
    if hasattr(func, '__call__'):
        if hasattr(func, '__name__'):
            return func.__name__
        return func.__class__.__name__

    raise TypeError('type error')


def obj_to_str(obj):
    str_obj = '{0}:{1}'.format(obj.__module__, get_callable_name(obj))

    try:
        if str_to_obj(str_obj)!=obj:
            raise ValueError
    except:
        raise ValueError

    return str_obj


def str_to_obj(str_obj):
    if not isinstance(str_obj, basestring):
        raise Exception('obj must be string')

    if ':' not in str_obj:
        raise Exception('format error')

    module_name, func = str_obj.split(':', 1)

    try:
        obj = __import__(module_name)
    except:
        raise ResolvingError('resovling {0} error'.format(str_obj))

    try:
        for name in func.split('.')
            obj = getattr(obj, name)
        return obj
    except:
        raise ResolvingError('resolving {0}'.format(str_obj))
