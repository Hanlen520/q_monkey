#! /usr/bin/python
# @Time    : 6/4/18 12:45 AM
# @Author  : Xiangwei Sun
# @FileName: mail.py
# @Software: PyCharm
from email.mime.text import MIMEText
import time
import smtplib
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SendMail():
    def __init__(self):
        # self.mail_host = ''
        self.user_name = 'seqatest360@gmail.com'
        self.passwrd = 'seqatest'
        self.str_date = time.strftime('%Y-%m-%d  %H:%M', time.localtime(time.time()))

    def send_mail(self, to_list, content):
        me = " Automation" + "<" + self.user_name + ">"
        msg = MIMEText(content, _subtype='plain', _charset='utf-8')
        msg['Subject'] = 'Monkey Result_%s' % self.str_date
        msg['From'] = me
        msg['To'] = to_list
        try:
            logger.info("start connnect mail server")
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            logger.info("Inputing usr_name and passwrd")
            server.login(self.user_name, self.passwrd)
            logger.info("start send mail")
            server.sendmail(self.user_name, to_list, msg.as_string())
            logger.info("close server")
            server.close()
            logging.info('mail sent successfully')
            return True
        except Exception:
            traceback.print_exc()
            logging.info('mail send failed')
            return False


if __name__ == '__main__':
    # for test
    mail = SendMail()
    mail.send_mail('sxwollo@hotmail.com', '123123213')
