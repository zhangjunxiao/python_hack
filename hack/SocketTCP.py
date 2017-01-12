#!/usr/bin/python

import socket
import optparse
import sys

def main():
    optparser = optparse.OptionParser('usage %prog -H <targetHost> -P <targetPort> -D <data>')
    optparser.add_option('-H', dest='tgtHost',  type='string', help='specify target host')
    optparser.add_option('-P', dest='tgtPort',  type='string', help='specify target Port')
    optparser.add_option('-D', dest='data',  type='string', help='data')
    (options, args) = optparser.parse_args()
    host = options.tgtHost
    port = options.tgtPort
    data = options.data

    if host == None or port == None:
        print "host is empty or port is empty"
        print optparser.usage
        exit(0)

    if data == None:
        print "data is empty"
        data = '123456'

    address = (str(host), int(port))
    socketConnect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = socketConnect.connect_ex(address)
    if result == 0:
        print "connected to " + host + ":" + port
    print 'receiving....'
    recvStr = socketConnect.recv(512)
    print 'received :' + recvStr

    socketConnect.send(data)

    print 'receiving....'
    recvStr = socketConnect.recv(2048)
    print 'received :' + recvStr

    socketConnect.close()
    exit(0)

if __name__ == '__main__':
    main()
