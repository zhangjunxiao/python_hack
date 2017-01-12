# coding=utf8

import MySQLdb
import time
import datetime
import os

db = MySQLdb.connect(host='192.168.31.89', user='zjx', passwd='123456', db='youwa', charset="utf8")
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data
db.close()
