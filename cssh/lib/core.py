import sys
import paramiko
import socket


def scp_command(host, user, password, localpath, remotepath, expire):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        rt = ssh.connect(host, username = user, password = password, timeout = expire)
        sftp = ssh.open_sftp()
        sftp.put(localpath, remotepath)
        return True, None
    except:
        return False, str(sys.exc_info()[1])

def ssh_command (host, user, password, command, expire):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        rt = ssh.connect(host, username = user, password = password, timeout = expire)
        stdin, stdout, stderr = ssh.exec_command(command)
        stdin.channel.shutdown_write()
        fd1 = stdout.read()
        fd2 = stderr.read()
        return fd1, fd2
    except:
        return None, str(sys.exc_info()[1])
    
def ssh_script (host, user, password, script, paramList, expire):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        rt = ssh.connect(host, username = user, password = password, timeout = expire)
        param = " ".join(paramList)
        stdin, stdout, stderr = ssh.exec_command('bash -s ' + param)
        scriptfile = open(script, 'r')
        for line in scriptfile:
            stdin.write(line)
        stdin.flush()
        stdin.close()
        scriptfile.close()
        stdin.channel.shutdown_write()
        fd1 = stdout.read()
        fd2 = stderr.read()
        return fd1, fd2
    except:
        return None, str(sys.exc_info()[1])
        
def checkSSH(HOST, PORT):     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((HOST, PORT))
        s.send('Hello')
        data = s.recv(64)
        pos = data.find('OpenSSH')
        if pos < 0:
            return False, str('not a OpenSSH service ,please check')
        s.close()
        return True, ''
    except socket.error, msg:
        s.close()
        return False, str(sys.exc_info()[1])
