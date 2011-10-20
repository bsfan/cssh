#!/usr/bin/python
import argparse
import sys

def argvParser():
    try:
        parser = argparse.ArgumentParser(description = '''
        Description: this script can execute command, run script or copy files to servers in bulk'''
        , epilog = 'Bug Report: mr.hackie.chain@gmail.com''', formatter_class = argparse.RawDescriptionHelpFormatter,)

        #Run mode
        parserGroupMode = parser.add_mutually_exclusive_group(required = True)
        parserGroupMode.add_argument('-c', '--cmd', metavar = 'COMMAND',
                                     help = 'execute command on target servers')
        parserGroupMode.add_argument('-cp', '--copy', metavar = 'File',
                                     nargs = 2, help = 'copy local file to target servers')
        parserGroupMode.add_argument('-s', '--script', metavar = 'Script',
                                     help = 'execute a local script on target servers')
        #List Type
        parserGroupType = parser.add_mutually_exclusive_group(required = True)
        parserGroupType.add_argument('-f', '--File', metavar = 'FILE', type = argparse.FileType('r'),
                                      help = 'Target Server List,only ONE IP each Line')
        parserGroupType.add_argument('-l', '--List', metavar = 'SERVER', nargs = '+')
        parserGroupType.add_argument('-fp', '--FileWithParam', type = argparse.FileType('r'),
                        metavar = 'FILE', help = 'a server list file,which contains parameters \
                        that will pass into the local script by its\' sequence. \
                        Format:<IP><Space><Param1><Space><Param2>....Escape character:"\\" \
                        Eg. 10.10.192.11 testStr "test Str" test\\\'str ')
        #Params
        parser.add_argument('-u', '--user', metavar = 'USER', required = True)
        parser.add_argument('-p', '--passwd', metavar = 'PASS', required = True)

        parser.add_argument('--stdout', type = argparse.FileType('w'),
                        default = sys.stdout, metavar = 'FILE', help = 'write the remote stdout to a file,you can also use "1>"')
        parser.add_argument('--stderr', type = argparse.FileType('w'),
                        default = sys.stderr, metavar = 'FILE', help = 'write the remote stderr to a file,you can also use "2>"')
        parser.add_argument('--log', type = argparse.FileType('w', 0),
                        default = 'cssh.log', metavar = 'LOG', help = 'remote stdin,stdout,stderr and so on,default is ./cssh.log')
        parser.add_argument('--timeout', type = int,
                        default = '60', metavar = 'Sec', help = 'connection timout value,default is 60 Sec')
        parser.add_argument('--port', type = int,
                        default = '22', metavar = 'PORT', help = 'connection port')                        
        
        args = parser.parse_args()

        values = {}
        values['user'] = args.user
        values['passwd'] = args.passwd
        values['stdout'] = args.stdout
        values['stderr'] = args.stderr
        values['log'] = args.log
        values['timeout'] = args.timeout
        values['port'] = args.port
        if args.cmd != None:
            values['mode'] = ['cmd', args.cmd]
        elif args.copy != None:
            values['mode'] = ['copy', args.copy]
        elif args.script != None:
            values['mode'] = ['script', args.script]
            
        serverlist = []
        if args.File != None:
            for line in args.File:
                serverlist.append([(line.split())[0], ['']])
        elif args.List != None:
            for line in args.List:
                serverlist.append([line])
        elif args.FileWithParam != None:
            for line in args.FileWithParam:
                serverlist.append([line.split()[0], line.split()[1:]])
        values['serverlist'] = serverlist

        return values
    
    except:
        print sys.exc_info()[1]
        sys.exit(1)
if __name__ == '__main__':
    print argvParser()
else:
    pass
