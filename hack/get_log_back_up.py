#!/usr/bin/python
# coding=utf-8

import os
import time
import MySQLdb
import datetime
import urllib

# 获取数据库备份文件
# 源数据主机 信息
user = "tzm529"
host = "120.55.240.252"
host_file_path = "/home/tzm529/run/backup/"


# 数据库配置
mysql_host = "localhost"
mysql_user = "root"
#mysql_passwd = "ihD45goig4ohIPAoh8gdsjsdf"
mysql_db = "nginx_log"
mysql_charset = "utf8"
mysql_socket ="/soft/mysql/mysql.sock"

# 路径配置
# 本机文件存储路径
save_file_path = os.getcwd()+"/log_back_up"

try:
    if not os.path.exists(save_file_path):
        os.makedirs(save_file_path)
    #scp_str = "scp %s@%s:%s%s.tar.bz2 -C %s" % (user, host, host_file_path, time.strftime("%Y%m%d"), save_file_path)
    log_file_name = time.strftime("%Y%m%d", time.localtime(time.time()-24*60*60))
    scp_str = "scp %s@%s:%s%s  %s" % (user, host, host_file_path, log_file_name, save_file_path)
    print log_file_name

    child = os.system(scp_str)
    # print scp_str
    # print child
    if child != 0:
        print "拷贝日志文件出错"
        exit(0)
    file_name = "%s/%s" % (save_file_path, log_file_name)
    if not os.path.exists(file_name):
        print "备份日志文件不存在"
        exit(0)

    db = MySQLdb.connect(host=mysql_host, user=mysql_user, charset=mysql_charset,unix_socket=mysql_socket)
    cursor = db.cursor()
    cursor.execute("use nginx_log;")

    cursor.execute("DROP TABLE IF EXISTS `%s`;" % log_file_name)
    create_table_str = '''CREATE TABLE `%s` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `remote_addr` varchar(50) NOT NULL DEFAULT '0.0.0.0' COMMENT '远程访问地址',
  `remote_user` varchar(50) NOT NULL DEFAULT '' COMMENT '客户端用户名称',
  `time_local` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '客户端本地时间（未+8）',
  `request_pattern` varchar(500) NOT NULL DEFAULT '' COMMENT '客户端请求方式',
  `request_url` varchar(500) NOT NULL DEFAULT '' COMMENT '客户端请求URL',
  `request_http` varchar(500) NOT NULL DEFAULT '' COMMENT '客户端请求http协议',
  `request_response_code` int(5) unsigned NOT NULL DEFAULT '0' COMMENT '客户端请求响应码',
  `request_response_size` int(5) unsigned NOT NULL DEFAULT '0' COMMENT '客户端请求响应内容大小',
  `http_referer` varchar(1000) NOT NULL DEFAULT '' COMMENT '客户端输入的完整http请求',
  `http_user_agent` varchar(300) NOT NULL DEFAULT '' COMMENT '客户端信息',
  `http_x_forwarded_for` varchar(50) NOT NULL DEFAULT '0.0.0.0' COMMENT '代理地址',
  `total_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '请求耗时',
  PRIMARY KEY (`id`),
  KEY `remote_addr` (`remote_addr`),
  KEY `total_time` (`total_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='服务器访问日志记录表';''' % log_file_name
    cursor.execute(create_table_str)
    print '建表完成'
    for line in open(file_name):
        # print line
        # 21 / Feb / 2017:23:51:40
        temp_line_ary = line.split(' ')
        # print len(temp_line_ary)
        # print line
        if len(temp_line_ary) < 11:
            continue
        remote_addr = temp_line_ary[0]
        remote_user = temp_line_ary[2]
        if remote_user == '-':
            remote_user = ''
        time_tmp = temp_line_ary[3].split('[')[1]
        time_local_tmp = datetime.datetime.strptime(time_tmp, '%d/%b/%Y:%H:%M:%S')
        time_local = time_local_tmp.strftime('%Y-%m-%d %H:%M:%S')
        request_pattern = temp_line_ary[5].split('\"')[1]
        request_url = urllib.unquote(temp_line_ary[6])
        request_http = temp_line_ary[7].split('\"')[0]
        request_response_code = temp_line_ary[8]

        if request_response_code == '-' or request_response_code == '\"-\"':
            request_response_code = 0 
        request_response_size = temp_line_ary[9]

        if request_response_size == '-' or request_response_size == '\"-\"':
            request_response_size = 0
        if temp_line_ary[10] != '-' or request_response_size != '\"-\"':
            if '\"' in temp_line_ary[10]:
                http_referer = temp_line_ary[10].split('\"')[1]
                if http_referer == '-':
                    http_referer = ''
            else:
                http_referer = temp_line_ary[10]
        else:
            http_referer = ''

        if len(temp_line_ary) >= 22 and '\"' in temp_line_ary[21] and '-' not in temp_line_ary[21] and len(temp_line_ary[21].split('\"')) >= 3:
            total_time = int(float(temp_line_ary[21].split('\"')[1]) * 1000)
        else:
            total_time = 0

        temp_line_ary2 = line.split('\"')

        if len(temp_line_ary2) < 8:
            continue

        http_user_agent = temp_line_ary2[5]
        if http_user_agent == '-':
            http_user_agent = ''
        http_x_forwarded_for = temp_line_ary2[7]
        if http_x_forwarded_for == '-':
            http_x_forwarded_for = ''

        mysql_cmd = """INSERT INTO `%s`(`remote_addr`,`remote_user`,`time_local`,`request_pattern`, `request_url`,`request_http`,`request_response_code`,`request_response_size`, `http_referer`,`http_user_agent`,`http_x_forwarded_for`, `total_time`) VALUES('%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s', '%s', '%d')""" % (log_file_name, remote_addr, remote_user, time_local, request_pattern,
                                        request_url, request_http, request_response_code, request_response_size,
                                        http_referer, http_user_agent, http_x_forwarded_for, total_time)
        print mysql_cmd
        # print request_response_size
        cursor.execute(mysql_cmd)
        db.commit()
    cursor.close()
    db.close()
    print '%s导入完成' % log_file_name
    # 删除过期备份文件 备份时间30天
    current_date = time.strftime("%Y%m%d")
    limit_day = datetime.datetime.strptime(current_date, "%Y%m%d") - datetime.timedelta(days=91)

    log_file_list = os.listdir("./log_back_up/")
    for log_file in log_file_list:
        file_create_day = datetime.datetime.strptime(log_file, "%Y%m%d")
        if file_create_day < limit_day:
            rm_str = "rm -irf ./log_back_up/" + log_file
            result = os.system(rm_str)
    exit(0)
except Exception, e:
    print e
    exit(0)
