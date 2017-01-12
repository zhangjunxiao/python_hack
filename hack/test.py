#!/usr/bin/python
# coding=utf-8

import datetime
import time
curent_date = time.strftime("%Y%m%d")
file_create_day = (datetime.datetime.strptime("20170111", "%Y%m%d") - datetime.datetime.strptime(curent_date, "%Y%m%d")).days
print file_create_day
print datetime.datetime.today()