#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

from lib import const
from lib import errors

from connection import Connection

class Runner(object):
    def __init__(self, task, hosts, connection_config):
        self.task = task

        if not hosts:
            raise errors.RunnerError('hosts must specified in runner section')

        self.sudo = utils.default(connection_config.get('sudo'), lambda: False)
        self.sudo_user = utils.default(connection_config.get('sudo_user'), None)
        self.sudo_pass = utils.default(connection_config.get('sudo_pass'), None)
        self.remote_port = utils.default(connection_config.get('remote_port'),\
                const.DEFAULT_REMOTE_PORT)
        self.private_key_file = utils.default(connection_config.get('private_key_file'),\
                const.PRIVATE_KEY_FILE)

        self.hosts = hosts
        self.connector = Connection(self)

    def _low_level_exec_command(self, conn, cmd, tmp, sudoable=False):
        sudo_user = self.task.job.sudo_user
        stdin, stdout, stderr = conn.exec_command(cmd, tmp, sudo_user, sudoable=sudoable)
        if type(stdout) != str:
            out = '\n'.join(stdout.readlines())
        else:
            out = stdout

        if type(stderr) != str:
            err = '\n'.join(stderr.readlines())
        else:
            err = stderr

        return out + err

    def _make_tmp_path(self, conn):
        base_file = 'task-execute-%s-%s' % (time.time(), random.randint(0, 2**48))
        basetmp = os.path.join('/tmp', const.DEFAULT_REMOTE_TMP, basefile)

        cmd = 'mkdir -p %s' % basetmp
        if self.task.job.remote_user != 'root':
            cmd += ' && chmod a+rx %s' % basetmp
        cmd += ' && echo %s' % basetmp
        result = self._low_level_exec_command(conn, cmd, None, sudoable=False)
        return utils.last_non_blank_line(result).strip() + '/'

    def _copy_module(self, conn, tmp, module_name, args):
        pass

    def _execute_module_internal(self):
        pass

    def _excute_internal(self, host):
        module_vars = self.task.module_vars()

        only_if = utils.template(self.task.only_if, module_vars)
        if not eval(only_if):
            result = utils.jsonify(dict(skipped=True))
            return ReturnData(host=host, result=result)

        module_name = utils.template(self.module_name, module_vars)
        if module_name != 'raw':
            tmp_path = self._make_tmp_path()

        try:
            port = self.task.job.port
            conn = self.connector.connect(host, port)
        except errors.ConnectionError, e:
            result = dict(failed=True, msg="FAILED: %s" % str(e))
            return ReturnData(host=host, comm_ok=False, result=result)

        result = None
        handler = getattr(self, "_execute_%s" % self.module_name, None)
        if handler:
            result = handler(conn, tmp, module_vars=module_vars)
        else:
            result = self._execute_module_internal()

        if module_name != 'raw':
            self._delete_remote_file(conn, tmp)
        conn.close()

        return result

    def _excute(self, host):
        try:
            ret = self._excute_internal(host)
            if type(ret) != ReturnData:
                raise errors.Exception('return type error')
            return ret
        except errors.RunnerError, e:
            msg = str(e)
            return ReturnData(host=host, comm_ok=False, result=dict(failed=True, msg=msg))
        except Exception:
            msg = traceback.format_exc()
            return ReturnData(host=host, comm_ok=False, result=dict(failed=True, msg=msg))

    def _partition_results(self, results):
        if results is None:
            return None

        results_for_ret = {contacted={}, dark={}}
        for result in results:
            host = result.host
            if not host:
                raise errors.RunnerException('host not set for return data')
            if result.comm_ok():
                results_for_ret['contacted'][host] = result
            else:
                results_for_ret['dark'][host] = result

         for host in self.hosts:
             if not any((host in results_for_ret['contacted'],\
                     host in results_for_ret['dark'])):

                 results_for_ret['dark'][host] = {}

         return results_for_ret

    def run(self):
        if len(self.hosts)==0:
            return dict(contacted={}, dark={})

        results = None
        if self.task.job.forks > 0:
            results = self.prallel_exec(self.hosts)
        else:
            results = [self._excute(h) for h in self.hosts]

        return self._partition_results(results)
