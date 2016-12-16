#!/usr/bin/python
# coding = utf-8

import nmap
import optparse
from threading import *


def nmapScan(tgtHost, tgtPort):
    nmScan = nmap.PortScanner()
    nmScan.scan(tgtHost, tgtPort)
    state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    print "[*] " + tgtHost + " tcp/"+tgtPort +" "+state


def main():
    optparser = optparse.OptionParser("usage %prog -H <tgtHost> -p <tgtPort>")
    optparser.add_option('-H', dest='tgtHost', type="string", help='specify target host')
    optparser.add_option('-p', dest='tgtPorts', type='string', help='specify target port[s] separated by comma')
    (options, args) = optparser.parse_args()

    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPorts).split(',')

    if(tgtHost == None) |(tgtPorts[0] == None):
        print optparser.usage
        exit(0)

    for tgtPort in tgtPorts:
        t = Thread(target=nmapScan, args=(tgtHost, tgtPort))
        t.start()

if __name__ == '__main__':
    main()
