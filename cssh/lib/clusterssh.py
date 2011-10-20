#!/usr/bin/python
from argv import argvParser
from core import scp_command
from core import ssh_command
from core import ssh_script
from core import checkSSH
import CThread
import time
g_successcount = 0

def threadCall(job):
    global g_successcount
    stdout = ''
    stderr = ''
    log = ''
    try:
        rt, errstr = checkSSH(job['server'][0], job['port'])
        if rt == True:
            log += 'cssh:' + str(job['server'][0]) + ' ssh checking OK:' + 'Mode ' + str(job['mode'][0]) + '\n'
        else:
            stderr += 'cssh:' + str(job['server'][0]) + ' ssh checking FAILED:' + errstr + '\n'
            log += 'cssh:' + str(job['server'][0]) + ' ssh checking FAILED: ' + errstr + '\n'
            return
        if job['mode'][0] == 'cmd':
            #log+='ssh_command:'+str(job['server'][0])+','+str(job['mode'][1])+'\n'
            fd1, fd2 = ssh_command(job['server'][0], job['user'], job['passwd'],
                                job['mode'][1], job['timeout'])
            if fd1 != None:
                stdout += fd1
                stderr += fd2
                log += 'STDOUT:\n' + fd1 + '\nSTDERR:\n' + fd2 + '\n'
            else:
                stderr += 'cssh:' + str(job['server'][0]) + ' ssh FAILED:' + fd2 + '\n'
                log += 'STDERR:\n' + fd2 + '\n'

        elif job['mode'][0] == 'copy':
            rt, errstr = scp_command(job['server'][0], job['user'], job['passwd'],
                                job['mode'][1][0], job['mode'][1][1], job['timeout'])
            if rt == True:
                stdout += 'cssh:' + str(job['server'][0]) + ' scp OK' + '\n'
                log += 'cssh:' + str(job['server'][0]) + ' scp OK' + '\n'
            else:
                stderr += 'cssh:' + str(job['server'][0]) + ' scp FAILED:' + errstr + '\n'
                log += 'cssh:' + str(job['mode'][0]) + 'scp FAILED:' + errstr + '\n'
        
        elif job['mode'][0] == 'script':
            fd1, fd2 = ssh_script(job['server'][0], job['user'], job['passwd'],
                                job['mode'][1], job['server'][1], job['timeout'])
            if fd1 != None:
                stdout += fd1
                stderr += fd2
                log += 'STDOUT:\n' + fd1 + '\nSTDERR:\n' + fd2 + '\n'
            else:
                stderr += fd2
                log += 'STDERR:\n' + fd2 + '\n'
        else:
            pass
        g_successcount += 1
    finally:
        job['stdout'].write(stdout)
        job['stdout'].flush()
        job['stderr'].write(stderr)
        job['stderr'].flush()
        job['log'].write(log)
        job['log'].flush()
        
def cssh(argv):
    CThread.initThread(50, threadCall)
    for item in argv['serverlist']:
        CThread.putjob({
        'server':item,
        'user':argv['user'],
        'passwd':argv['passwd'],
        'stdout':argv['stdout'],
        'stderr':argv['stderr'],
        'log':argv['log'],
        'timeout':argv['timeout'],
        'mode':argv['mode'],
        'port':argv['port']
        })
    CThread.waitDone()
    
def main():
    start = time.time()
    argv = argvParser()
    #print 'cssh: init thread....'
    #print 'cssh: Break with CTRL+Z kill %%'
    cssh(argv)
    finish = time.time()
    argv['log'].write('cssh:' + str(len(argv['serverlist'])) + ' Jobs ' + str(g_successcount) + ' Done. ' + '\n')
    argv['log'].write('run time: ' + '%.2f' % (finish - start) + ' Sec' + '\n')
