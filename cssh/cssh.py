#!/usr/bin/python
import sys
import os
def readlinkabs(l):
    """
    Return an absolute path for the destination 
    of a symlink
    """
    if os.path.islink(l) != True:
        return os.path.realpath(__file__)
    p = os.readlink(l)
    if os.path.isabs(p):
        return p
    return os.path.join(os.path.dirname(l), p)

sys.path.append(os.path.dirname(readlinkabs(__file__)) + "/lib.zip")
sys.path.append(os.path.dirname(readlinkabs(__file__)) + "/lib")
from clusterssh import main
from clusterssh import cssh



def call(argv):
    """
    argv is a python dict type:
     argv= {
        'server':[server1,server2,server3,......],
        'user': "username",
        'passwd': "password",
        'stdout': sys.stdout,
        'stderr': sys.stderr,
        'log': "cssh.log",
        'timeout': 60,
        'mode':["cmd","who"] #command mode 
                ["copy",[srcFilePath,dstFilePath]] #copy mode
                ["script","/root/sh.sh"], #script mode
        'port': 22
        }
    """
    cssh(argv)

if __name__ == '__main__':
        main()
