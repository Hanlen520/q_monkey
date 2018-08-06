#! /usr/bin/python
# @Time    : 6/3/18 6:28 PM
# @Author  : Xiangwei Sun
# @FileName: adb_cmd.py
# @Software: PyCharm
import os, logging, time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ADB_CMD(object):
    def attacted_devices(self):
        cmd = 'adb devices'
        devices_id = []
        logger.info("Run CMD: adb devices")
        result = os.popen(cmd, 'r').readlines()
        if result.__le__() == 0 and result[0].strip().endswith('attached'):
            return False
        elif result.__le__() >= 1:
            for r in result:
                if r.strip().endswith('device'):
                    logger.info("Device Name: %s" % r.strip().split('\t')[0])
                    devices_id.append(r.strip().split('\t')[0])

    def start_adb(self):
        cmd = 'adb start-server'
        logger.info("Run CMD: adb start-server")
        os.popen(cmd, 'r')

    def stop_adb(self):
        cmd = 'adb kill-server'
        logger.info("Run CMD: adb kill-server")
        os.popen(cmd, 'r')

    def start_monkey(self, cmd, f_name):
        logger.info("Monkey Start")
        monkey_cmd = '%s > "%s"' % (cmd, f_name)
        logger.info('Monkey CMD is "%s"' % monkey_cmd)
        os.popen(monkey_cmd, 'r')
        logger.info("Monkey Finish")

    def stop_monkey(self):
        cmd = 'adb shell ps | grep monkey'
        pids = []
        for r in os.popen(cmd, 'r').readlines():
            if r.strip().endswith('monkey'):
                pids.append(r.strip().split()[1])
        if pids.__len__() == 0:
            pass
        elif pids.__len__() > 0:
            for pid in pids:
                cmd = 'adb shell kill %s' % pid
                os.popen(cmd, 'r')

    def gen_bugreport(self, report_fname):
        andriod_version = int(os.popen('adb shell getprop ro.build.version.sdk').readlines()[0].strip())
        if andriod_version >= 23:
            os.popen('adb bugreport %s.zip' % report_fname)
        if andriod_version < 23 and andriod_version > 0:
            os.popen('adb bugreport > %s.txt' % report_fname)

    def set_up_jar(self):
        monkey_path = os.path.join(os.getcwd() + os.path.sep + 'Maxim', 'monkey.jar')
        logger.info("Monkey.jar path is %s" % monkey_path)
        framework_path = os.path.join(os.getcwd() + os.path.sep + 'Maxim', 'framework.jar')
        logger.info("Framework.jar Path is %s" % framework_path)
        os.popen('adb push "%s" /sdcard/' % monkey_path, 'r')
        os.popen('adb push "%s" /sdcard/' % framework_path, 'r')

    def install_adb_keyboard(self):
        cmd = 'adb shell pm list packages -3 | grep com.android.adbkeyboard'
        results = os.popen(cmd, 'r').readlines()
        if results.__len__() == 0:
            adb_keyboard_apk_path = os.path.join(os.getcwd() + os.path.sep + 'Maxim' + os.path.sep + 'test',
                                                 'ADBKeyBoard.apk')
            os.popen('adb install "%s"' % adb_keyboard_apk_path, 'r')

    def clear_logs(self):
        os.popen('adb shell logcat -c', 'r')
        os.popen('adb shell dumpsys batterystats --reset', 'r')
        os.popen('adb shell rm /sdcard/crash-dump.log', 'r')
        os.popen('adb shell rm /sdcard/oom-traces.log', 'r')

    def pull_crash_log(self, path):
        result = os.popen('adb shell ls /sdcard/ | grep crash-dump.log', 'r').readlines()
        cmd = 'adb pull /sdcard/crash-dump.log %s' % path
        if result.__len__() > 0:
            logger.info('pull_crash_log_cmd: %s' % cmd)
            os.popen(cmd, 'r')
        else:
            logger.info("No crash-dump file found")
            pass

    def pull_oom_log(self, path):
        result = os.popen('adb shell ls /sdcard/ | grep oom-tr*.log', 'r').readlines()
        cmd = 'adb pull /sdcard/oom-traces.log %s' % path
        if result.__len__() > 0:
            logger.info('pull_oom_log_cmd: %s' % cmd)
            os.popen(cmd, 'r')
        else:
            logger.info("No oom-traces.log found")
            pass

    def get_phone_info(self):
        phone_info = {}
        phone_info['Phone Model'] = os.popen('adb shell getprop ro.product.model', 'r').readline().strip()
        phone_info['Phone Brand'] = os.popen('adb shell getprop ro.product.brand', 'r').readline().strip()
        phone_info['Phone Resolution'] = os.popen('adb shell wm size', 'r').readline().strip()
        return phone_info

    def get_logs(self, log_path):
        logs = []
        crash_cmd = 'adb shell ls /sdcard/ | grep app_crasm*.txt'
        anr_cmd = 'adb shell ls /sdcard/ | grep anr_*.txt'
        crash_results = os.popen(crash_cmd, 'r').readlines()
        for crash_r in crash_results:
            logs.append(crash_r)
        anr_results = os.popen(anr_cmd, 'r').readlines()
        for anr_result in anr_results:
            logs.append(anr_result)
        for l in logs:
            cmd = "adb pull /sdcard/%s %s" % (l, log_path)
            os.popen(cmd, 'r')
        logger.info(logs)
        return logs
