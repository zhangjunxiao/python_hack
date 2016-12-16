#!/usr/bin/python
# coding = utf-8

import pexpect
import optparse
PROMPT = ['# ', '>>> ', '>', '\$ ']
def set_command(child, cmd) :
    child.sendline(cmd)
    child.expect(PROMPT)
    print child.before


def connet(user, host, password):
    ssh_newKey = 'Are you sure you want to continue connecting'
    connStr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(connStr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newKey, '[P|p]assword:'])
    if ret == 0:
        print '[-] Error Connecting'
        return

    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT,\
                            '[P|p]assword:'])
        if ret == 0:
            print '[-] Error Connecting'
            return
    child.sendline(password)
    child.expect(PROMPT)
    return child
def main():
    optparser = optparse.OptionParser("usage %prog -U <user> -H <tgtHost> -P <password>")
    optparser.add_option('-U', dest='user', type="string", help='user name')
    optparser.add_option('-H', dest='tgtHost', type="string", help='specify target host')
    optparser.add_option('-P', dest='password', type="string", help='specify target host password')
    (options, args) = optparser.parse_args()

    user = options.user
    tgtHost = options.tgtHost
    password = options.password

    if (tgtHost == None) | (password == None):
        print optparser.usage
        exit(0)

    child = connet(user, tgtHost, password)
    set_command(child, 'ls -al')

if __name__ == '__main__':
    main()
