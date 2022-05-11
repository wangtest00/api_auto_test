import time
from appium import webdriver
import unittest,os
from daiqian.base_lp import *
from app.auth_tur import *
from data.var_tur_app import *
from app.grab_data import *
from app.appium_start_stop import *
from app.swipe_test import *

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
port=4727
udid='192.168.20.116:5555'

class Test_Install_Login_Tur(unittest.TestCase):
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
        desired_caps['udid'] = udid
        # 应用的包名
        desired_caps['appPackage'] = 'com.turrant'
        # 应用启动需要的Android Activity名称
        desired_caps['appActivity'] = 'com.turrant.ui.activity.LaunchActivity'
        # 跳过检查核对应用进行debug的签名的步骤
        # desired_caps['noSign'] = "True"
        # desired_caps["unicodeKeyboard"] = True
        # desired_caps["resetKeyboard"] = True
        desired_caps["automationName"] = "Uiautomator2"
        desired_caps['app'] = app_address
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
    def test_install_first_apply(self):
        '''【turrant-android-MOTO】test_install_first_apply-授权，进件5页面，检查数据抓取正案例'''
        self.shouquan()
        time.sleep(3)
        registNo=str(random.randint(7000000000,9999999999)) #10位随机数作为手机号
        print(registNo)
        self.driver.find_element_by_id('com.turrant:id/phone').send_keys(registNo)
        time.sleep(1)
        code = compute_code(registNo)
        self.driver.find_element_by_id('com.turrant:id/code').send_keys(code)
        self.driver.find_element_by_id('com.turrant:id/login_btn').click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('com.turrant:id/loan_btn').click()  # step1点击申请贷款按钮,进入实名认证页面
        self.driver.find_element_by_xpath(xp1).send_keys('wang shuang')
        self.driver.find_element_by_xpath(xp2).send_keys('test')
        self.driver.find_element_by_xpath(xp3).send_keys('android')
        self.driver.find_element_by_xpath(xp4).click()
        time.sleep(5)
        self.driver.find_element_by_id("com.turrant:id/textView2").click()#点击ok
        self.driver.find_element_by_xpath(xp5).click()                    #点击education
        time.sleep(3)
        self.driver.find_element_by_id('com.turrant:id/textView2').click()#点击ok
        time.sleep(3)
        self.driver.find_element_by_xpath(xp6).click()     #marital status婚姻状况
        time.sleep(3)
        self.driver.find_element_by_id('com.turrant:id/textView2').click()#点击ok
        swipeup(self.driver,1000)
        self.driver.implicitly_wait(10)
        curtNo=certlist()
        self.driver.find_element_by_xpath(xp7).send_keys('wang123QQ@gmail.com')  #email
        self.driver.find_element_by_xpath(xp8).send_keys(curtNo[0])  #A卡
        self.driver.find_element_by_xpath(xp9).send_keys(curtNo[1])  #pan卡
        self.driver.find_element_by_xpath(xp10).click()  # 选择语言
        time.sleep(3)
        self.driver.find_element_by_id('com.turrant:id/textView2').click()
        time.sleep(3)
        self.driver.find_element_by_xpath(xp11).click()  #step2点击下一步,进入kyc页面
        time.sleep(3)
        self.driver.find_element_by_id('com.turrant:id/card_1').click()
        self.driver.find_element_by_id('com.turrant:id/tt_select_album').click()
        self.driver.find_element_by_xpath(xp12).click()
        self.driver.find_element_by_xpath(xp13).click()
        self.driver.find_element_by_id('com.turrant:id/card_2').click()
        self.driver.find_element_by_id('com.turrant:id/tt_select_album').click()
        self.driver.find_element_by_xpath(xp12).click()
        self.driver.find_element_by_xpath(xp13).click()
        self.driver.find_element_by_id('com.turrant:id/card_3').click()
        self.driver.find_element_by_id('com.turrant:id/tt_select_album').click()
        self.driver.find_element_by_xpath(xp12).click()
        self.driver.find_element_by_xpath(xp13).click()
        self.driver.find_element_by_id('com.turrant:id/card_4').click()
        time.sleep(3)
        self.driver.find_element_by_id('com.oppo.camera:id/shutter_button').click()#点击拍照
        time.sleep(3)
        self.driver.find_element_by_id('com.oppo.camera:id/done_button').click() #点击确认
        time.sleep(3)
        self.driver.find_element_by_id('com.turrant:id/next').click() #step3点击下一步，进入家庭地址信息页面
        time.sleep(5)
        self.driver.find_element_by_xpath(xp14).send_keys('123456789')
        self.driver.find_element_by_xpath(xp15).send_keys('this is home address')
        self.driver.find_element_by_xpath(xp16).click()
        time.sleep(3)
        self.driver.find_element_by_id(id17).click()
        self.driver.find_element_by_xpath(xp18).click()
        time.sleep(3)
        self.driver.find_element_by_id(id19).click()
        self.driver.find_element_by_id('com.turrant:id/next').click()#step4点击下一步,进入工作信息证明页面
        time.sleep(5)
        self.driver.find_element_by_xpath(xp20).click()
        self.driver.find_element_by_id(id21).click()
        self.driver.find_element_by_xpath(xp22).send_keys('This Is Company Name')
        self.driver.find_element_by_xpath(xp23).click()
        self.driver.find_element_by_id(id24).click()
        self.driver.find_element_by_xpath(xp25).click()
        self.driver.find_element_by_id(id26).click()
        self.driver.find_element_by_id(id27).click()
        self.driver.find_element_by_id(id28).click()
        self.driver.find_element_by_id(id29).click()
        self.driver.find_element_by_xpath(xp30).click()
        self.driver.find_element_by_xpath(xp31).click()
        self.driver.find_element_by_id(id32).click()
        self.driver.find_element_by_id(id33).click()
        self.driver.find_element_by_xpath(xp34).click()
        self.driver.find_element_by_xpath(xp35).click()
        self.driver.find_element_by_id('com.turrant:id/next').click()  #step5点击下一步，进入联系人信息页面
        time.sleep(5)
        self.driver.find_element_by_id(id36).click()
        self.driver.find_element_by_id(id37).click()
        self.driver.find_element_by_xpath(xp38).send_keys('test android one')
        self.driver.find_element_by_xpath(xp39).send_keys('7474666222')
        self.driver.find_element_by_id(id40).click()
        time.sleep(1)
        self.driver.swipe(360, 1400, 360, 1300, 1000)
        time.sleep(1)
        self.driver.find_element_by_id('com.turrant:id/textView2').click() #点击ok
        self.driver.find_element_by_xpath(xp42).send_keys('test android two')
        self.driver.find_element_by_xpath(xp43).send_keys('7474666333')
        swipeup(self.driver,1000)
        self.driver.find_element_by_id('com.turrant:id/next').click() #点击提交申请
        time.sleep(30)
        self.driver.find_element_by_id('com.turrant:id/bind_bank').click() #提交成功后，点击ok按钮
        time.sleep(5)
        self.driver.find_element_by_id('com.turrant:id/tv_title').is_displayed()#检查是否被拒绝
        grab_data=cx_grab_data(registNo)
        for i in range(len(grab_data)):
            self.assertIsNotNone(grab_data[i])
        logout(self.driver)
    def tearDown(self):
        #self.driver.quit()
        print("testcase done")
    @classmethod
    def tearDownClass(cls):  # 在所有用例都执行完之后运行的
        appium_stop(port)
        print('我是tearDownClass，我位于多有用例运行的结束')

if __name__ == '__main__':
    unittest.main()