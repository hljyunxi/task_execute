#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

import os
from lib import errors
import subprocess
import tracebook
import shutil

class Connection(object):
    def __init__(self, runner, host, port):
        self.runner = runner
        self.host = host
        self.port = port

    def connect(self):
        pass

    def close(self):
        pass

    def exec_command(self, command, tmp_path, sudo_user, sudoable=False):
        if self.runner.sudo and sudoable:
            if self.runner.sudo_pass:
                raise errors.RunnerError('sudo pass only support in ssh and paramiko'
                        'connection plugin')
            command = 'sudo -u {0} -p {1}'.format(sudo_user, command)

         p = subprocess.Popen(command, shell=True, stdin=None,
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
         stdout, stderr = p.communicate()
         return ("", stdout, stderr)

    def put_file(self, in_path, out_path):
        if not os.path.exists(in_path)
            raise errors.RunnerError('')

        try:
            shutil.copyfile(in_path, out_path)
        except shutil.Error:
            traceback.print_exec()
            raise errors.RunnerError()
        except IOError:
            traceback.print_exec()
            raise errors.RunnerError()

    def fetch_file(self, in_path, out_path):
        self.put_file(in_path, out_path)
