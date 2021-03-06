import paramiko

class RunCommand(object):
    known_hosts="/home/chiara/.ssh/known_hosts_mass"
    user="chiara"
    manage="/srv/test.costruttoridimondi.org/costruttoridimondi/manage.py"

    def __init__(self,host):
        self.host=host

    def __call__(self,*args,**kwargs):
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy()) 
        self.client.load_host_keys(self.known_hosts)
        self.client.connect(self.host)
        ret=self.exec_command(*args,**kwargs)
        self.client.close()
        return ret

    def exec_command(self,*args,**kwargs):
        stdin, stdout, stderr = self.client.exec_command('ls -l')
        return 

class CreateSession(RunCommand):
    def exec_command(self,*args,**kwargs):
        (email,)=args
        cmd=self.manage+" create_session "+str(email)
        stdin, stdout, stderr = self.client.exec_command(cmd)
        stdin.close()
        key=stdout.read().strip().decode()
        return key

class ResetDatabase(RunCommand):
    def exec_command(self,*args,**kwargs):
        cmd=self.manage+" flush --noinput"
        stdin, stdout, stderr = self.client.exec_command(cmd)
        stdin.close()
        return 

def create_session_on_server(host, email):
    cmd=CreateSession(host)
    return cmd(email)

def reset_database(host):
    cmd=ResetDatabase(host)
    return cmd()

