#!/usr/bin/env python
# encoding: utf-8

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import PocoNoSuchNodeException
from utils.key_code import *
from utils.adb_utils import AdbUtils
from utils.device_utils import *
from utils.file_utils import *
from utils.airtest_utils import *
from Ids import *
import time, random

# -----------------大目标App--------------------------------
package_name = 'com.tencent.mm'
activity = '.ui.LauncherUI'


class Wechat(object):
    def __init__(self):
        try:
            self.poco = AndroidUiautomationPoco(screenshot_each_action=False)
            self.adb = AdbUtils()
            auto_setup(__file__)
            self.connected = True
        except:
            self.connected = False

    def runFunc(self, funcName, **args):
        if not self.connected:
            print('连接设备失败,无法执行')
            return
        self._pre()
        func = getattr(self, funcName, None)
        if not func is None:
            func(**args)

    def _exit(self):
        home()
        self.adb.sendKeyEvent(POWER)
        self.poco.stop_running()

    def _pre(self):
        if not self.adb.isInstall(package_name):
            print('未安装{},无法执行'.format(package_name))
            return
        #解锁手机
        self.adb.unlockPhone()
        # # 删除缓存文件
        # remove_dir('./temp/')
        home()
        # stop_app(package_name)
        start_target_app(package_name, activity)
    
    def _toHomePage(self):
        sleep(1)
        if self.poco(id_wechat_bottom_tabs).exists():
           return
        else:
           self.adb.sendKeyEvent(BACK)
           self._toHomePage()
        
    def __toUserFromSearch(self, user):
        self.poco(id_wechat_search_btn).click()
        self.poco(id_wechat_search_txt).wait_for_appearance()
        perform_view_input(self.poco, id_wechat_search_txt, user)
        self.poco(id_wechat_search_result_list).wait_for_appearance()
        items = self.poco(id_wechat_search_result_list).children()
        for item in items:
            try:
                item_info_text = item.offspring(
                    id_wechat_search_result_item_txt).get_text().strip()
                if item_info_text==user:
                    item.click()
                    return True
            except Exception as e:
                print(e)
        return False

    def __toUserFromRecent(self, user):
        self.poco(id_wechat_recent_message_list).wait_for_appearance()
        items = self.poco(id_wechat_recent_message_list).children()
        for item in items:
            try:
                item_info_text = item.child().child().offspring(
                    id_wechat_recent_message_item_txt).get_text().strip()
                if item_info_text==user:
                    item.click()
                    return True
            except Exception as e:
                print(e)
        return False

    def _goToUser(self, user):
        self._toHomePage()
        self.poco(id_wechat_tab1_btn).click()
        return self.__toUserFromRecent(user) or self.__toUserFromSearch(user)
        

    def _sendText(self, to, text):
        if to is None:
            print('未指定对象,无法发送')
            return
        if text is None:
            print('发送内容为空无法发送')
            return
        if not self._goToUser(to):
           print('未找到指定对象')
           return
        self.poco(id_wechat_message_txt).wait_for_appearance()
        perform_view_input(self.poco, id_wechat_message_txt, text)
        self.poco(id_wechat_message_send_btn).click()

    def _makeVideoCall(self, to):
        if to is None:
            print('未指定对象,无法拨打')
            return
        if not self._goToUser(to):
           print('未找到指定对象')
           return
        self.poco(id_wechat_message_txt).wait_for_appearance()
        self.poco(id_wechat_message_more_entrance_btn).click()
        self.poco(id_wechat_message_more_func_list).wait_for_appearance()
        items = self.poco(id_wechat_message_more_func_list).children()
        for item in items:
            try:
                item_info_text = item.child().child().offspring(
                    id_wechat_message_more_func_item_txt).get_text().strip()
                if item_info_text=='视频通话':
                    item.click()
                    break
            except Exception as e:
                print(e)


def sendText( text,to='老板'):
    wechat = Wechat()
    wechat.runFunc('_sendText', to=to, text=text)

def makeVideoCall(to='老板'):
    wechat = Wechat()
    wechat.runFunc('_makeVideoCall', to=to)


if __name__ == '__main__':
    sendText('hello')
