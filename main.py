#!/usr/bin/env python
# encoding: utf-8

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from utils.key_code import *
from utils.adb_utils import AdbUtils
from utils.device_utils import *
from utils.file_utils import *
from Ids import *


# -----------------手淘App--------------------------------
package_name = 'com.small.target'
activity = 'com.admin.module.view.activity.index.LoadingActivity'
# activity = '.WelcomeActivity'


# -------------------------------------------------



class SmallTarget(object):

    def __init__(self):
        self.poco = AndroidUiautomationPoco(screenshot_each_action=False)
        self.adb = AdbUtils()
        auto_setup(__file__)

    def run(self):
        self.__pre()
        sleep(5)
        # self.__search_good_by_key()
        # exec_cmd('open %s' % get_screenshot_pic())
        self.adb.sendKeyEvent(POWER)
        self.poco.stop_running()

    def __pre(self):
        """
        准备工作
        :return:
        """
        if not self.adb.isInstall(package_name):
            print('未安装{},无法执行'.format(package_name))
            return
        #解锁手机
        self.adb.unlockPhone()
        # 删除缓存文件
        remove_dir('./temp/')
        home()
        stop_app(package_name)
        start_target_app(package_name, activity)


    def __search_good_by_key(self):
        """
        通过关键字搜索商品
        :return:
        """
        self.poco(id_page_main_button_search).wait(5).click()
        # perform_view_id_click(poco, id_page_main_button_search)
        perform_view_input(self.poco, id_page_search_edittext_search, self.key)

        # 点击搜索
        self.poco(id_page_search_button_search).wait_for_appearance()
        while self.poco(id_page_search_button_search).exists():
            print('点击一次搜索')
            perform_view_id_click(self.poco, id_page_search_button_search)

        # 等待列表加载出来
        self.poco(id_page_goods_rv).wait_for_appearance()

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
    SmallTarget().run()
