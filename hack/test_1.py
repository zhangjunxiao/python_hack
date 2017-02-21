#!/usr/bin/python
# coding=utf-8
import MySQLdb

db = MySQLdb.connect(host="localhost", user="zjx_wx", passwd="zjx123456", charset="utf8")
cursor = db.cursor()
cursor.execute("use `youwa-211`;")
cursor.execute("source /Users/junxiaozhang/mysql/youwa.sql")
cursor.commit()
cursor.close()
db.close()
