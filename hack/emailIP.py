#!/usr/bin/python
# coding=utf-8
# coding:utf-8  #强制使用utf-8编码格式
import smtplib  # 加载smtplib模块
from email.mime.text import MIMEText
from email.utils import formataddr
import os

my_sender = 'zjxpeople@sina.com'  # 发件人邮箱账号，为了后面易于维护，所以写成了变量
my_user = '291722629@qq.com'  # 收件人邮箱账号，为了后面易于维护，所以写成了变量




def mail():
    ret = True
    try:
        #公网IP查询接口
        ipStr = os.popen("curl members.3322.org/dyndns/getip")
        msg = MIMEText(ipStr.read(), 'plain', 'utf-8')
        msg['From'] = formataddr(["zjxpeople", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["张俊啸", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "IP地址实时更换"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP("smtp.sina.com", 25)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, "zjx277285590")  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 这句是关闭连接的意思
    except Exception:  # 如果try中的语句没有执行，则会执行下面的ret=False
        ret = False
    return ret


ret = mail()
if ret:
    print("ok")  # 如果发送成功则会返回ok，稍等20秒左右就可以收到邮件
else:
    print("filed")  # 如果发送失败则会返回filed