# -*- coding: utf-8 -*-
import time
from appium import webdriver
import os
import unittest
from app.appium_start_stop import *

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
port=4727

class Test_Install_Login(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  # 在所有用例执行之前运行的
        print('我是setUpclass，我位于所有用例的开始')
        appium_start('127.0.0.1', port)  # 启动appium服务
    def setUp(self):
        desired_caps = {}
        # 设备系统
        desired_caps['platformName'] = 'Android'
        # 设备系统版本号
        desired_caps['platformVersion'] = '11'
        # 设备名称
        desired_caps['deviceName'] = 'MOTO'
        desired_caps['udid'] = '192.168.20.116:5555'
        # 应用的包名
        desired_caps['appPackage'] = 'com.turrant'
        # 应用启动需要的Android Activity名称
        desired_caps['appActivity'] = 'com.turrant.ui.activity.LaunchActivity'
        # 跳过检查核对应用进行debug的签名的步骤
        # desired_caps['noSign'] = "True"
        # desired_caps["unicodeKeyboard"] = True
        # desired_caps["resetKeyboard"] = True
        desired_caps["automationName"] = "Uiautomator2"
        desired_caps['app'] = 'D:\\app_list\\turrant\\Test-Turrant_V1.0.2_2022-05-07-14-45-03_google.apk'
        # 配置远程server（通过本地代码调用远程server）
        remote = "http://127.0.0.1:" +str(port)+ "/wd/hub"
        print(remote)
        self.driver = webdriver.Remote(remote, desired_caps)
        # 设置隐式等待为 10s
        self.driver.implicitly_wait(10)
    def shouquan(self):
        self.driver.find_element_by_id('com.turrant:id/agree').click()
        time.sleep(3)
        self.driver.find_element_by_id('com.android.permissioncontroller:id/permission_allow_foreground_only_button').click()
        time.sleep(3)
        self.driver.find_element_by_id('com.android.permissioncontroller:id/permission_allow_foreground_only_button').click()
        time.sleep(3)
        self.driver.find_element_by_id('com.android.permissioncontroller:id/permission_allow_button').click()
        time.sleep(3)
        self.driver.find_element_by_id('com.android.permissioncontroller:id/permission_allow_button').click()
        time.sleep(3)
        self.driver.find_element_by_id('com.android.permissioncontroller:id/permission_allow_button').click()
        time.sleep(3)
        self.driver.find_element_by_id('com.android.permissioncontroller:id/permission_allow_button').click()
    def test_install_login(self):
        self.shouquan()
        time.sleep(3)
        input = self.driver.find_element_by_id('com.turrant:id/phone')
        input.send_keys('8686860000')
        input2 = self.driver.find_element_by_id('com.turrant:id/code')
        input2.send_keys('5555')
        self.driver.find_element_by_id('com.turrant:id/login_btn').click()
    def tearDown(self):
        #self.driver.quit()
        print("testcase done")
    @classmethod
    def tearDownClass(cls):  # 在所有用例都执行完之后运行的
        appium_stop(port)
        print('我是tearDownClass，我位于多有用例运行的结束')
if __name__ == '__main__':
    unittest.main()