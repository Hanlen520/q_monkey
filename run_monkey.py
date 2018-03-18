import os, time, logging

cur_date = time.strftime('%Y_%m_%d', time.localtime())
cur_time = time.strftime('%Y%m%d%H%M', time.localtime())
os.chdir(os.getcwd())
log_dir = os.path.join(os.getcwd(), cur_date)
Monkey_CMD = 'adb shell CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec app_process /system/bin tv.panda.test.monkey.Monkey -p  --uiautomatormix --monitor-native-crashes --bugreport -v -v -v'


class ADM_CMD(object):
    def is_device_attached(self):
        cmd = 'adb devices'
        result = os.popen(cmd, 'r').readlines()
        logging.info(result)
        if result.__len__() == 0 and result[0].strip().endswith('attached'):
            return False
        elif result.__len__() >= 1:
            for r in result:
                if r.strip().endswith('device'):
                    return True

    def start_adb(self):
        cmd = 'adb start-server'
        os.popen(cmd, 'r')

    def clear_monkey_log(self):
        os.popen('adb shell logcat -c', 'r')
        os.popen('adb shell dumpsys batterystats --reset', 'r')

    def stop_monkey(self):
        cmd = 'adb shell | grep monkey'
        pids = []
        for r in os.popen(cmd, 'r').readlines():
            if r.strip().endswith('monkey'):
                pids.append(r.strip().split()[1])
            if pids.__len__() == 0:
                logging.info('No MONKEY Found')
            else:
                logging.info('MONMEY Found')
                for pid in pids:
                    logging.info('Monkey PID is ' + pid)
                    cmd = 'adb shell kill' + pid
                    os.popen(cmd, 'r')
                    logging.info('Monkey PID: ' + pid + 'is killed')

    def start_monkey(self, cmd, f_name):
        logging.info('Monkey Starts')
        os.popen(cmd + ' > ' + f_name, 'r')
        logging.info('Monkey Ends')

    def gen_monkey_bugreport(self, report_fname):
        android_version = int(os.popen('adb shell getprop ro.build.version.sdk').readlines()[0].strip())
        if android_version >= 23:
            os.popen('adb bugreport %s.zip' % report_fname)
        else:
            os.popen('adb bugreport > %s.txt' % report_fname)

    def __push_monkey_jar(self):
        monkey_path = os.path.join(os.getcwd() + os.path.sep + 'Maxim-master', 'monkey.jar')
        cmd = 'adb push %s /sdcard/' % monkey_path
        os.popen(cmd, 'r')

    def __push_framework_jar(self):
        framework_path = os.path.join(os.getcwd() + os.path.sep + 'Maxim-master', 'framework.jar')
        cmd = 'adb push %s /sdcard/' % framework_path
        os.popen(cmd, 'r')

    def push_jar(self):
        cmd = 'adb shell ls /sdcard/ | grep .jar'
        has_monkey = False
        has_framework = False
        results = os.popen(cmd, 'r').readlines()
        if results.__len__() == 0:
            self.__push_framework_jar()
            self.__push_monkey_jar()
        else:
            for r in results:
                if r.strip().startswith('monkey'):
                    has_monkey = True
                if r.startswith('framework'):
                    has_framework = True
        if not has_monkey:
            self.__push_monkey_jar()
        if not has_framework:
            self.__push_framework_jar()


class Controller(object):
    def __init__(self, count):
        self.adb = ADM_CMD()
        self.count = count

    def setUp(self):
        self.adb.start_adb()
        self.adb.push_jar()
        self.adb.clear_monkey_log()

    def run(self):
        while self.count > 0:
            self.setUp()
            now = time.localtime()
            log_dir = os.getcwd() + os.path.sep + time.strftime('%Y_%m_%d', now)
            monkey_log = os.path.join(log_dir, 'MonkeyLog_' + time.strftime('%Y%m%d%H%M%S', now) + '.txt')
            report_fname = os.path.join(log_dir, 'bugreport_%s' % time.strftime('%Y%m%d%H%M%S', now))
            if not os.path.exists(log_dir):
                os.popen('mkdir %s' % log_dir, 'r')
            self.adb.start_monkey(Monkey_CMD, monkey_log)
            self.adb.gen_monkey_bugreport(report_fname)


if __name__ == '__main__':
    controller = Controller(1)
    controller.run()
