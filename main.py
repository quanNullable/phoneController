#!/usr/bin/env python
# encoding: utf-8

from airtest.core.api import *
from poco.exceptions import PocoNoSuchNodeException
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from utils.file_utils import *
from utils.string_utils import *
from utils.device_utils import *
from utils.airtest_utils import *
from utils.image_utils import *
from utils.adb_utils import AdbUtils
from queue import Queue
import datetime
from Ids import *
import time


# -----------------手淘App--------------------------------
package_name = 'com.taobao.taobao'
activity = 'com.taobao.tao.welcome.Welcome'


# -------------------------------------------------

# -----------------知乎App--------------------------------
# package_name = 'com.zhihu.android'
# activity = '.app.ui.activity.LauncherActivity'
# -------------------------------------------------


class TaoBao(object):

    def __init__(self, key, *args):
        self.poco = AndroidUiautomationPoco(screenshot_each_action=False)
        self.adb = AdbUtils()
        auto_setup(__file__)

    def run(self):

        # 1、准备工作,打开淘宝客户端
        self.__pre()
        sleep(5)
        # exec_cmd('open %s' % get_screenshot_pic())
        # adb.startWebpage("http://www.baidu.com")
        # adb.callPhone(18671717521)

    def __pre(self):
        """
        准备工作
        :return:
        """
        #解锁手机
        self.adb.unlockPhone()
        # 删除缓存文件
        remove_cache('./part.jpg', './screenshot.png', './uidump.xml')
        home()
        stop_app(package_name)
        start_target_app(package_name, activity)


    def __swipe(self, up_or_down):
        """
        滑动单条新闻
        :param up_or_down: true：往上滑动；false：往下滑动【慢慢滑动】
        :return:
        """
        if up_or_down:
            self.poco.swipe([0.5, 0.8], [0.5, 0.4], duration=0.2)
        else:
            self.poco.swipe([0.5, 0.4], [0.5, 0.8], duration=0.2)

if __name__ == '__main__':
    taobao = TaoBao('小米')
    taobao.run()
