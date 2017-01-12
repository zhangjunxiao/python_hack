#!/usr/bin/python
# coding=utf-8

import  socket
import os
import time
import MySQLdb
import re
import datetime

# 获取数据库备份文件

global i
i = 0
def is_exist_host():
    global i
    address = ("192.168.31.211", 22)
    socketConnect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = socketConnect.connect_ex(address)
    # temp = os.system("tcping  192.168.31.211 22 -c 2")
    while result != 0:
        i += 1
        if i == 100:
            print "目标主机不在局域网内"
            socketConnect.close()
            exit(0)
        time.sleep(10)
        is_exist_host()
    # 结束之后关闭端口
    socketConnect.close()

is_exist_host()

try:
    # path_str = sys.path[0]
    path_str = os.path.dirname(os.getcwd())
    # print path_str
    user = "root"
    host = "192.168.31.211"
    host_file_path = "/home/tzm529/run/backup/"
    save_file_path = "./mysql_back_up"

    today = time.strftime("%Y%m%d")
    if not os.path.exists(save_file_path):
        os.makedirs(save_file_path)
    # scp_str = "scp %s@%s:%s%s.tar.bz2 -C %s" % (user, host, host_file_path, time.strftime("%Y%m%d"), save_file_path)
    scp_str = "scp %s@%s:%s%s.tar.bz2 %s" % (user, host, host_file_path, "20170111", save_file_path)

    # (status, output) = commands.getstatusoutput(scp_str)
    child = os.system(scp_str)
    print scp_str
    if child != 0:
        print "拷贝数据库出错"
        exit(0)

    # file_name = "%s/%s.tar.bz2" % (path_str, time.strftime("%Y%m%d"))
    file_name = "%s/%s.tar.bz2" % (save_file_path,  "20170111")
    if not os.path.exists(file_name):
        print "备份文件不存在"
        exit(0)

    tar_path_name = path_str
    tar_str = "tar -jxvf "+file_name+" -C "+os.getcwd()+"/mysql_back_up"

    status = os.system(tar_str)
    print "\n"
    print tar_str

    if status != 0:
        print "解压文件失败"
        exit(0)

    youwa_mysql_file = os.getcwd()+"/mysql_back_up/mysql/youwa.sql"
    print youwa_mysql_file
    if not os.path.exists(youwa_mysql_file):
        print "备份文件不存在"
        exit(0)

    db = MySQLdb.connect(host='localhost', user='zjx_wx', passwd='zjx123456', db='youwa-211', charset="utf8")
    cursor = db.cursor()
    statement = ""
    # 过滤注释
    for line in open(youwa_mysql_file):
        if re.match(r'--', line):  # ignore sql comment lines
            continue
        if not re.search(r'[^-;]+;$', line):  # keep appending lines that don't end in ';'
            statement = statement + line
        else:  # when you get a line ending in ';' then exec statement and reset for next statement
            statement = statement + line
            # print "\n\n[DEBUG] Executing SQL statement:\n%s" % (statement)
            try:
                # print statement
                if statement:
                    cursor.execute(statement)
            except (MySQLdb.OperationalError, MySQLdb.ProgrammingError) as e:
                print "\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))
            statement = ""
    # db.commit()
    db.close()
    print "数据同步完成"

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



