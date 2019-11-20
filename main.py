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
import time,random

# -----------------大目标App--------------------------------
package_name = 'com.small.target'
activity = 'com.admin.module.view.activity.index.LoadingActivity'

FOLLOW_MONEY = 5.0#值得围观的钱数

class SmallTarget(object):

    def __init__(self):
        try:
            self.poco = AndroidUiautomationPoco(screenshot_each_action=False)
            self.adb = AdbUtils()
            auto_setup(__file__)
            self.connected=True
        except:
            self.connected=False
        self.readCount=0
        self.money=0

    def run(self):
        if not self.connected:
            print('连接设备失败,无法执行')
            return
        self._pre()
        self._go_to_message_list()
        self._exit()
    
    def _exit(self):
        home()
        self.adb.sendKeyEvent(POWER)
        self.poco.stop_running()

    def _pre(self):
        """
        准备工作
        :return:
        """
        if not self.adb.isInstall(package_name):
            print('未安装{},无法执行'.format(package_name))
            return
        #解锁手机
        self.adb.unlockPhone()
        # # 删除缓存文件
        # remove_dir('./temp/')
        home()
        stop_app(package_name)
        start_target_app(package_name, activity)


    def _go_to_message_list(self):
        """
        将新的围观设置为已读
        """
        self.poco(id_page_message_tab).wait(1).click()
        get_screenshot_pic('temp/{}.png'.format(int(time.time())))
        if self.poco(id_page_unread_message_num).exists():#有未读新消息
            perform_view_id_click(self.poco, id_page_my_message_btn)
             # 等待列表加载出来
            self.poco(id_page_my_follow_message_list).wait_for_appearance()
            self._loop_read_message()
            follow_info = self.poco(id_page_my_follow_info).get_text().strip()
            print('围观信息:',follow_info)
            follows = follow_info.split('/')
            need_new_follow = int(follows[1])-int(follows[0])
            if need_new_follow>0:
                self._find_people_to_follow(need_new_follow)
            else:
                print('围观已满')
            follow_money_info = self.poco(id_page_my_follow_money_info).get_text().strip()
            self.money = follow_money_info.split('￥')[1]
            print('围观收入:',follow_money_info)
            self.adb.sendKeyEvent(BACK)
        else:
            print('没有未读消息')

    def _loop_read_message(self):
        """
        将所有消息设置为已读
        :return:
        """
        now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        items = self.poco(id_page_my_follow_message_list).children()
        finished = False
        for item in items:
            try:
                item_time_info = item.offspring(id_page_my_follow_message_item_time).get_text().strip()
                item_time = item_time_info.split(' ')[0]
                if self.poco(id_page_my_follow_message_item_new).exists() or (item_time==now):
                   item.click()
                   self.poco(id_page_my_follow_message_detail).wait_for_appearance()
                   self._read_message_detail()
                else:
                    finished = True
                    break; 
            except Exception as e:
                print(e)
        if not finished:
           time.sleep(1)
           self.adb.swipeByRatio(0.5, 0.8, 0.5, 0.42)
           time.sleep(1)
           self._loop_read_message()

    def _read_message_detail(self):
        time.sleep(random.randint(2,5))
        self.adb.swipeToUp()
        if random.choice([1, 2,3])==3:
            print('点赞')
            self.poco(id_page_my_follow_message_detail_money_btn).sibling(id_page_my_follow_message_detail_zan_btn).click()
        self.readCount+=1
        self.adb.sendKeyEvent(BACK)


    def _find_people_to_follow(self,count):
        print('尝试新围观{}人'.format(count))
        self.poco(id_page_home_tab).wait(1).click()
        self.poco(id_page_my_follow_message_list).wait_for_appearance()
        for index in range(count):
            self._find_one_to_follow()

    def _follow_new(self):
        print('判断是否值得围观')
        result = False
        try:
            # self.adb.swipeToDown()
            money_node = self.poco(id_page_follow_detail_money_info)
            money_node.wait_for_appearance(5)
            money_des = money_node.get_text().strip()
            money=0
            if '￥' in money_des:
                money = money_des.split('￥')[1]
            else:
                money = money_des.split(' · ')[2].split('元')[0]
            result=float(money)>=FOLLOW_MONEY
            if result:
                print('找到值得围观的人了')
        except Exception as e:
                print('_follow_new',e)
        finally:
            self.adb.sendKeyEvent(BACK)
            return result



    def _find_one_to_follow(self):
        #添加新的围观
        message_node = self.poco(id_page_my_follow_message_list)
        message_node.wait_for_appearance()
        items = message_node.children()
        success = False
        for item in items:
            try:
                btn_info = item.offspring(id_page_home_tab_item_follow_btn)
                if len(btn_info.children())>0:
                   item.click()
                   if self._follow_new():
                       success = True
                       btn_info.click()
                       self.poco(id_modal_follow_result_content).wait_for_appearance()
                       self.adb.sendKeyEvent(BACK)
                       break
            except Exception as e:
                print('_find_one_to_follow',e)
        if not success:
            time.sleep(1)
            self.adb.swipeByRatio(0.5, 0.8, 0.5, 0.421)
            time.sleep(1)
            self._find_one_to_follow()
        

def autoFollow():
    target = SmallTarget()
    target.run()
    print('已读消息:',target.readCount)
    print('已赚金额:',target.money)

if __name__ == '__main__':
    autoFollow()
