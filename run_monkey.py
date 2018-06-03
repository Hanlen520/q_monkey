import os, time, logging
from util.adb_cmd import ADB_CMD
from util.mail import SendMail

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.chdir(os.getcwd())
PACKAGE_NAME = 'com.qihoo.browser'
Monkey_CMD = 'adb shell CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec app_process /system/bin tv.panda.test.monkey.Monkey -p %s --uiautomatormix --monitor-native-crashes --bugreport -v -v -v'


class Controller(object):
    def __init__(self, count):
        self.app = ADB_CMD()
        self.count = count

    def set_up(self):
        self.app.start_adb()
        self.app.set_up_jar()
        self.app.install_adb_keyboard()

    def tear_down(self):
        self.app.stop_monkey()
        self.app.stop_adb()
        self.app.clear_logs()

    def run(self):
        log_dir = os.getcwd() + os.path.sep + 'logs' + os.path.sep + time.strftime('%Y_%m_%d', now)
        while self.count > 0:
            now = time.localtime()
            cur_date = time.strftime('%Y_%m_%d', now)
            cur_time = time.strftime('%Y%m%d%H%M', now)
            #self.set_up()
            monkey_log = os.path.join(log_dir + os.path.sep + 'logs',
                                      'MonkeyLog_' + time.strftime('%Y%m%d%H%M%S', now) + '.txt')
            report_fname = os.path.join(log_dir + os.path.sep + 'logs',
                                        'bugreport_%s' % time.strftime('%Y%m%d%H%M%S', now))
            crash_fname = os.path.join(log_dir + os.path.sep + 'logs',
                                       'crash_%s.log' % time.strftime('%Y%m%d%H%M%S', now))
            anr_fname = os.path.join(log_dir + os.path.sep + 'logs', 'anr_%s.log' % time.strftime('%Y%m%d%H%M%S', now))
            dump_fname = os.path.join(log_dir + os.path.sep + 'logs',
                                      'dump_%s.log' % time.strftime('%Y%m%d%H%M%S', now))
            if not os.path.exists(log_dir):
                os.popen('mkdir -p %s' % log_dir, 'r')
            self.app.start_monkey(Monkey_CMD % PACKAGE_NAME,monkey_log)
            self.app.gen_bugreport(report_fname)
            self.app.pull_crash_log(dump_fname)
            self.app.pull_oom_log(anr_fname)
            self.app.get_logs(log_dir)
            self.tear_down()
            self.count = self.count -1



if __name__ == '__main__':
    controller = Controller(1)
    controller.run()
