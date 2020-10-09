# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: send_email
@time: 2020/2/18 15:59
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr


class SendMail(object):
    def __init__(self, host, user, pwd):
        self.host = host  # 设置服务器
        self.user = user  # 用户名
        self.pwd = pwd  # 口令
        pass

    def to(self, title, msg, receivers):
        """
        第三方 SMTP 服务
        :param title:
        :param msg:
        :param receivers: str, 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        :return:
        """
        message = MIMEMultipart()
        mail_body = MIMEText(msg, _subtype='html', _charset='utf-8')
        message['From'] = formataddr(["Jarrett", self.user])  # 括号里对应收件人邮箱昵称发件人邮箱账号
        message['To'] = formataddr([receivers, receivers])
        # 邮件主题，也就是说是标题
        message['Subject'] = Header(title, 'utf-8')
        message.attach(mail_body)

        try:
            sever = smtplib.SMTP(self.host, 25)  # 发件人邮箱中的SMTP服务器
            sever.login(self.user, self.pwd)
            sever.sendmail(self.user, [receivers], message.as_string())  # sendmail的第二个参数必须是list，可以发送多个用户
            print("邮件发送成功")
            sever.quit()  # 关闭连接
            return True
        except smtplib.SMTPException:
            print("Error: 无法发送邮件至" + receivers)
            return False
