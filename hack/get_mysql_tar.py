#!/usr/bin/python
# coding=utf-8

import os
import time
import MySQLdb
import re
import datetime

# 获取数据库备份文件
# 源数据主机 信息
user = "tzm529"
host = "114.55.85.120"
host_file_path = "/home/tzm529/run/backup/"

# 数据库配置
mysql_host = "localhost"
mysql_user = "root"
#mysql_passwd = "ihD45goig4ohIPAoh8gdsjsdf"
mysql_db = "youwa-sever"
mysql_charset = "utf8"
mysql_socket ="/soft/mysql/mysql.sock"

# 路径配置
# 本机文件存储路径
save_file_path =os.getcwd()+"/mysql_back_up"
#
mysql_file_save_path = save_file_path+"/mysql"

try:
    if not os.path.exists(save_file_path):
        os.makedirs(save_file_path)
    #scp_str = "scp %s@%s:%s%s.tar.bz2 -C %s" % (user, host, host_file_path, time.strftime("%Y%m%d"), save_file_path)
    scp_str = "scp %s@%s:%s%s.tar.bz2  %s" % (user, host, host_file_path, time.strftime("%Y%m%d"), save_file_path)

    child = os.system(scp_str)
    print scp_str
    print child
    if child != 0:
        print "拷贝数据库出错"
        exit(0)

    file_name = "%s/%s.tar.bz2" % (save_file_path, time.strftime("%Y%m%d"))
    if not os.path.exists(file_name):
        print "备份文件不存在"
        exit(0)

    tar_str = "tar -jxvf "+file_name+" -C "+save_file_path

    status = os.system(tar_str)
    print "\n"
    print tar_str

    if status != 0:
        print "解压文件失败"
        exit(0)

    msyql_file_list = os.listdir(mysql_file_save_path)

    db = MySQLdb.connect(host=mysql_host, user=mysql_user, charset=mysql_charset,unix_socket=mysql_socket)
    cursor = db.cursor()
    # 获取 所有 database
    db_list = []
    cursor.execute("show databases;")
    for db_name in cursor.fetchall():
        db_list.append(db_name[0])

    for mysql_file_name in msyql_file_list:
        database_name = mysql_file_name.split('.sql')[0]
        if database_name not in db_list:
            cursor.execute("create database `%s`" % database_name)
        cursor.execute("use `%s`;" % database_name)
        statement = ""
        # 过滤注释
        mysql_file = mysql_file_save_path+"/"+mysql_file_name
        print "同步 %s 数据库数据中" % database_name
        cmd = "mysql -f -u%s %s < %s" % (mysql_user, database_name, mysql_file)
        status = os.system(cmd)
        if status == 0:
            print "同步 %s 数据库完成" % database_name
        else:
            print "同步 %s 数据库失败" % database_name
    # db.commit()
    db.close()

    # 删除解压文件
    rm_str = "rm -irf ./mysql_back_up/mysql"
    result = os.system(rm_str)
    sql_file_list = os.listdir("./mysql_back_up/")

    # 删除过期备份文件 备份时间30天
    current_date = time.strftime("%Y%m%d")
    limit_day = datetime.datetime.strptime(current_date, "%Y%m%d") - datetime.timedelta(days=30)
    for sql_file in sql_file_list:
        file_create_day = datetime.datetime.strptime(sql_file.split('.')[0], "%Y%m%d")
        if file_create_day < limit_day:
            rm_str = "rm -irf ./mysql_back_up/"+sql_file
            result = os.system(rm_str)
    exit(0)
except Exception, e:
    print e
    exit(0)


