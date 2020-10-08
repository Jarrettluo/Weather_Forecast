# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: sendemail
@time: 2020/2/18 15:59
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

HOST = 'smtp.163.com'
USER = '*************@163.com'
PWD = '#############'

def automail(title, msg, receivers):
    """

    :param title:
    :param msg:
    :param receivers: str, 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    :return:
    """
    # 第三方 SMTP 服务
    mail_host = HOST  # 设置服务器
    mail_user = USER  # 用户名
    mail_pass = PWD  # 口令

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = formataddr(["Jarrett", mail_user])  # 括号里对应收件人邮箱昵称发件人邮箱账号
    message['To'] = formataddr([receivers, receivers])

    subject = title  # 邮件主题，也就是说是标题
    message['Subject'] = Header(subject, 'utf-8')

    try:
        sever = smtplib.SMTP(mail_host, 25)  # 发件人邮箱中的SMTP服务器
        sever.login(mail_user, mail_pass)
        sever.sendmail(mail_user, [receivers], message.as_string())  # sendmail的第二个参数必须是list，可以发送多个用户
        print("邮件发送成功")
        sever.quit()  # 关闭连接
    except smtplib.SMTPException:
        print("Error: 无法发送邮件至" + receivers)
