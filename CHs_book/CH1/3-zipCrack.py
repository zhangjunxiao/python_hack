#!/usr/bin/python
# -*- coding: utf-8 -*-
import zipfile
import optparse
import sys
from threading import Thread
# 命令行格式 python 3-zipCrack.py -f name.zip -d 词典名称.text

def extractFile(zFile, password):
    try:
        zFile.extractall(pwd=password)
        print '[+] Found password ' + password + '\n'
    except:
        pass


def main():
    parser = optparse.OptionParser("usage %prog "+\
      "-f <zipfile> -d <dictionary>")
    parser.add_option('-f', dest='zname', type='string',\
      help='specify zip file')
    parser.add_option('-d', dest='dname', type='string',\
      help='specify dictionary file')
    # args = ['-f', 'evil.zip', '-d', './evil']
    print sys.argv
    (options, args) = parser.parse_args()
    print parser.usage
    print options
    print args
    if (options.zname == None) | (options.dname == None):
        print parser.usage
        exit(0)
    else:
        zname = options.zname
        dname = options.dname

    zFile = zipfile.ZipFile(zname)
    passFile = open(dname)

    for line in passFile.readlines():
        password = line.strip('\n')
        t = Thread(target=extractFile, args=(zFile, password))
        t.start()


if __name__ == '__main__':
    main()
