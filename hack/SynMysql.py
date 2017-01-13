#!/usr/bin/python
# coding=utf-8

import os
import optparse

def main():
    optparser = optparse.OptionParser('usage %prog -H <host> -T <targetHost> -U <user> -P <passwd> -D <database> ')
    optparser.add_option('-H', dest='host', type='string', help='specify source host')
    optparser.add_option('-T', dest='targetHost', type='string', help='specify target host')
    optparser.add_option('-U', dest='user', type='string', help='user')
    optparser.add_option('-P', dest='passwd', type='string', help='passwd')
    optparser.add_option('-D', dest='database', type='string', help='database')
    (options, args) = optparser.parse_args()
    host = options.host
    tgtHost = options.targetHost
    user = options.user
    passwd = options.passwd
    database = options.database

    if not host:
        host = "192.168.31.211"
    if not tgtHost:
        tgtHost = "127.0.0.1"
    if not user:
        user = "root"
    if not passwd:
        passwd = "123456"
    if not database:
        database = "youwa"

    mysqldump_str = "mysqldump --host=%s -uroot -p123456 --opt youwa | mysql --host=%s -u%s -p%s -C %s" % (host, tgtHost, user, passwd, database)
    print mysqldump_str
    os.system(mysqldump_str)
    print "同步结束"
    exit(0)

if __name__ == '__main__':
    main()
