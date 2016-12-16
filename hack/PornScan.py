#!/usr/bin/python
# coding=utf-8

# 端口扫描器
import optparse
from socket import *
from threading import *

# 信号量  线程互锁
screenLock = Semaphore(value=1)


# 连接 主机 端口
def connScan(tgtHost, tgtPort):
    try:
        connetSocket = socket(AF_INET, SOCK_STREAM)
        connetSocket.connect((tgtHost, tgtPort))
        connetSocket.send('ViolentPython\r\n')
        results = connetSocket.recv(100)
        screenLock.acquire()
        print '[+] %d/tcp open' % tgtPort
        print '[+] ' + str(results)
    except:
        screenLock.acquire()
        print '[-] %d/tcp closed' % tgtPort
    finally:
        screenLock.release()
        connetSocket.close()


# 获取端口 线程进行
def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print "[-] Cannot resolve '%s': Unknown host" % tgtHost
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        print '\n[+] Scan Results for: ' + tgtName[0]
    except:
        print '\n[+] Scan Results for: ' + tgtIP

    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()


def main():
    parser = optparse.OptionParser('usage %prog ' + \
                                   '-H <target host> -p <target port>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port[s] separated by comma')

    (options, args) = parser.parse_args()

    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(',')

    if (tgtHost == None) | (tgtPorts[0] == None):
        print parser.usage
        exit(0)

    portScan(tgtHost, tgtPorts)

if __name__ == '__main__':
    main()
