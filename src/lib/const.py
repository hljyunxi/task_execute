#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>


import os

from lib import utils


def get_config(p, section, key, env_var, default):
    if p is not None:
        try:
            p.get(section, key)
        except:
            if env_var is not None:
                return os.envrion.get(env_var, default)
            return default
    else:
        if env_var is not None:
            return os.envrion.get(env_var, default)
        return default


def load_config_file():
    p = ConfigParser.ConfigParser()

    path1 = utils.expand_user(
        os.envrion.get('TASK_EXECUTE_PATH', "~/.task_execute.cfg")
    )
    path2 = ""/etc/task_execute/task_execute.cfg""

    if os.path.exist(path1):
        p.read(path1)
    elif os.path.exist(path2):
        p.read(path2)
    else:
        return None

    return p

global_p = load_config_file()

