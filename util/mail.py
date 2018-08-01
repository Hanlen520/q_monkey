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
    mail_info = "crash:\r\n" \
                "// CRASH: com.qihoo.browser (pid 14286) (dump time: 2018-07-11 12:42:09)\r\n" \
                "// Build Time: 1524853579000\r\n" \
                "// *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***\r\n" \
                "// Build fingerprint: '360/QK1801/QK1801:7.1.1/NMF26X/7.1.100.PX.180427.360_360_QK1801_CN:user/release-keys'\r\n" \
                "// Revision: '0'\r\n" \
                "// ABI: 'arm'\r\n" \
                "// pid: 14286, tid: 14286, name: m.qihoo.browser  >>> com.qihoo.browser <<<\r\n" \
                "// signal 6 (SIGABRT), code -6 (SI_TKILL), fault addr --------\r\n" \
                "// Abort message: '[FATAL:jni_android.cc(236)] Please include Java exception stack in crash report\r\n" \
                "// #00 0xc84a1ae3 /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so+0x0029eae3\r\n" \
                "// #01 0xc848bf03 /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so+0x00288f03\r\n" \
                "// #02 0xc84f8bb1 /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so+0x002f5bb1\r\n" \
                "// #03 0xc84642ed /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armea    r0 00000000  r1 000037ce  r2 00000006  r3 00000008\r\n" \
                "//     r4 f0b2358c  r5 00000006  r6 f0b23534  r7 0000010c\r\n" \
                "//     r8 f02e8008  r9 fff3fd24  sl 00000000  fp ca35b5ac\r\n" \
                "//     ip 0000000b  sp fff3f770  lr f02a2d53  pc f02a566c  cpsr 600f0010\r\n" \
                "// \r\n" \
                "// backtrace:\r\n" \
                "//     #00 pc 0004a66c  /system/lib/libc.so (tgkill+12)\r\n" \
                "//     #01 pc 00047d4f  /system/lib/libc.so (pthread_kill+34)\r\n" \
                "//     #02 pc 0001daa5  /system/lib/libc.so (raise+10)\r\n" \
                "//     #03 pc 00019465  /system/lib/libc.so (__libc_android_abort+34)\r\n" \
                "//     #04 pc 000174c0  /system/lib/libc.so (abort+4)\r\n" \
                "//     #05 pc 00290bc5  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so\r\n" \
                "//     #06 pc 0029eb4d  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so\r\n" \
                "//     #07 pc 00288f01  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so\r\n" \
                "//     #08 pc 002f5baf  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so\r\n" \
                "//     #09 pc 002612ed  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so\r\n" \
                "//     #10 pc 002616df  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so\r\n" \
                "//     #11 pc 00b21605  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so\r\n" \
                "//     #12 pc 00b21d0f  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so\r\n" \
                "//     #13 pc 00b2a883  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so\r\n" \
                "//     #14 pc 00aa6871  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so\r\n" \
                "//     #15 pc 00a948fd  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so\r\n" \
                "//     #16 pc 0070e9f3  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so\r\n" \
                "//     #17 pc 00291bc9  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so\r\n" \
                "//     #18 pc 002a4917  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so\r\n" \
                "//     #19 pc 002a4f99  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so\r\n" \
                "//     #20 pc 002a5213  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so\r\n" \
                "//     #21 pc 002a5a85  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/lib/armeabi-v7a/libqihoowebview.so\r\n" \
                "//     #22 pc 0007b2d5  /data/data/com.qihoo.browser/qihoo_webview/1.0.0.38/QihooWebView.dex (offset 0x1c2000)\r\n" \
                "// \r\n" \
                "crashend"
    mail.send_mail('sunxiangwei-iri@360.cn', mail_info)
