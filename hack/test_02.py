#!/usr/bin/python
# coding=utf-8

import os
import time
import MySQLdb
import datetime
import urllib
import types

# 数据库配置
mysql_host = "localhost"
mysql_user = "root"
#mysql_passwd = "ihD45goig4ohIPAoh8gdsjsdf"
mysql_db = "nginx_log"
mysql_charset = "utf8"
mysql_socket ="/soft/mysql/mysql.sock"
log_file_name = '20170226'

try:
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
  `request_url` varchar(1000) NOT NULL DEFAULT '' COMMENT '客户端请求URL',
  `request_http` varchar(1000) NOT NULL DEFAULT '' COMMENT '客户端请求http协议',
  `request_response_code` int(5) unsigned NOT NULL DEFAULT '0' COMMENT '客户端请求响应码',
  `request_response_size` int(5) unsigned NOT NULL DEFAULT '0' COMMENT '客户端请求响应内容大小',
  `http_referer` varchar(1000) NOT NULL DEFAULT '' COMMENT '客户端输入的完整http请求',
  `http_user_agent` varchar(1000) NOT NULL DEFAULT '' COMMENT '客户端信息',
  `http_x_forwarded_for` varchar(50) NOT NULL DEFAULT '0.0.0.0' COMMENT '代理地址',
  `total_time` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '请求耗时',
  PRIMARY KEY (`id`),
  KEY `remote_addr` (`remote_addr`),
  KEY `total_time` (`total_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='服务器访问日志记录表';''' % log_file_name
    cursor.execute(create_table_str)

    print '建表完成'
    for line in open('./log_back_up/20170226'):
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

        temp_line_ary2 = line.split('\"')
        # print temp_line_ary2
        if len(temp_line_ary2) < 8:
            continue

        http_user_agent = temp_line_ary2[5]
        if http_user_agent == '-':
            http_user_agent = ''
        http_x_forwarded_for = temp_line_ary2[7]
        if http_x_forwarded_for == '-':
            http_x_forwarded_for = ''
        total_time_tmp = temp_line_ary2[len(temp_line_ary2)-2]
        print total_time_tmp
        if '-' not in total_time_tmp and total_time_tmp.count('.') == 1:
            total_time = int(float(total_time_tmp) * 1000)
        else:
            total_time = 0
        print total_time
        if type(request_response_code) is types.StringType and request_response_code.isdigit() == False:
            request_response_code = 0
        if type(request_response_size) is types.StringType and request_response_size.isdigit() == False:
            request_response_size = 0
        # 判断请求方式以及请求链接中是否包含转义字符
        if '\\' in request_pattern or '\\' in request_url:
            request_pattern = ''
            request_url = ''
            request_http = ''
        if '\'' in request_url:
            request_url = request_url.replace('\'', ' ')
            print request_url

        mysql_cmd = """INSERT INTO `%s`(`remote_addr`,`remote_user`,`time_local`,`request_pattern`, `request_url`,`request_http`,`request_response_code`,`request_response_size`, `http_referer`,`http_user_agent`,`http_x_forwarded_for`, `total_time`) VALUES('%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s', '%s', '%d')""" % (
        log_file_name, remote_addr, remote_user, time_local, request_pattern,
        request_url, request_http, request_response_code, request_response_size,
        http_referer, http_user_agent, http_x_forwarded_for, total_time)
        print mysql_cmd
        # print request_response_size
        cursor.execute(mysql_cmd)
        db.commit()
    cursor.close()
    db.close()
    print '%s导入完成' % log_file_name
except Exception, e:
    print e
    exit(0)