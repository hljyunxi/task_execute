#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>

HAVE_PARAMIKO = False

try:
    import paramiko
    HAVE_PARAMIKO = True
except ImportError:
    pass

class Connection(object):
    def __init__(self, runner, host, port):
        self.runner = runner
        self.host = host
        self.port = port

    def connect(self):
        if not HAVE_PARAMIKO:
            raise errors.ConnectionError('paramiko not install')

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        user = self.runner.remote_user
        try:
            ssh.connect(self.host, username=user, allow_agent=True, look_for_keys=True,
                    key_filename=self.runner.private_key_file, password=self.runner.remote_pass,
                    timeout=self.runner.timeout, port=self.port)
        except Exception, e:
            msg = str(e)
            raise errors.ConnectionError(msg)

        self.ssh = ssh
        return self

    def close(self):
        self.ssh.close()

    def exec_command(self, cmd, tmp_path, sudo_user, sudoable=False):
        buf_size = 4096

        try:
            chan = self.ssh.get_transport().open_session()
        except Exception, e:
            msg = str(e)
            raise errors.ConnectionError(msg)

        if not self.runner.sudo or not sudoable:
            quoted_command = '"$SHELL" -c ' + pipes.quote(cmd)
            chan.exec_command(quoted_command)
        else:
            randbits = ''.join(chr(random.randint(ord('a'), ord('z'))) for x in xrange(32))
            prompt = '[sudo via ansible, key=%s] password: ' % randbits
            sudocmd = 'sudo -k && sudo -p "%s" -u %s "$SHELL" -c %s' % (
                     prompt, sudo_user, pipes.quote(cmd))

            sudo_output = ''
            try:
                chan.exec_command(sudocmd)
                if self.runner.sudo_pass:
                    while not sudo_output.endswith(prompt):
                        chunk = chan.recv(bufsize)
                        if not chunk:
                            if 'unknown user' in sudo_output:
                                raise errors.ConnectionError('unkonown sudo user %s' % sudo_user)
                            else:
                                raise errorsConnectionError('closed waiting for password prompt')
                        sudo_output += chunk
                    chan.sendall(self.runner.sudo_pass + '\n')
            except socket.timeout:
                raise errors.ConnectionError('ssh timed out waiting for sudo.\n' + sudo_output)

         return (chan.makefile('wb', bufsize), chan.makefile('rb', bufsize), chan.makefile_stderr('rb', bufsize))

    def put_file(self):
        if not os.path.exists(in_path):
            raise errors.AnsibleFileNotFound("file or module does not exist: %s" % in_path)
        try:
            sftp = self.ssh.open_sftp()
        except:
            raise errors.AnsibleError("failed to open a SFTP connection")
        try:
            sftp.put(in_path, out_path)
        except IOError:
            raise errors.AnsibleError("failed to transfer file to %s" % out_path)
        sftp.close()

    def fetch_file(self):
        try:
            sftp = self.ssh.open_sftp()
        except:
            raise errors.AnsibleError("failed to open a SFTP connection")
        try:
            sftp.get(in_path, out_path)
        except IOError:
            raise errors.AnsibleError("failed to transfer file from %s" % in_path)
        sftp.close()
