from api_auto_test.public.base_fr import *
from api_auto_test.public.dataBase import *
from api_auto_test.public.var_fr import *
import random
import unittest,requests,json
from HTMLTestRunner_Chart import HTMLTestRunner

class App_Api_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  #在所有用例执行之前运行的
        print('我是setUpclass，我位于所有用例的开始')
    def setUp(self):  #每个用例运行之前运行的
        print('setup_test')
    def tearDown(self): #每个用例运行之后运行的
        print('teardown_test')
    def test_login_code(self):    #函数名要以test开头，否则不会被执行
        '''【FeriaRapida】/api/cust/login注册登录接口-正案例'''      #用例描述，在函数下，用三个单引号里面写用例描述
        registNo=str(random.randint(8000000000,9999999999)) #10位随机数作为手机号
        code=compute_code(registNo)
        data={"registNo":registNo,"code":code,"gaid":"Exception:null"}
        r=requests.post(host_api+"/api/cust/login",data=json.dumps(data),headers=head_api,verify=False)
        self.assertEqual(r.status_code,200)
        t=r.json()
        token=t['data']['token']
        self.assertIsNotNone(token)
        self.assertEqual(t['errorCode'],0)
    def test_login_pwd(self):
        '''【FeriaRapida】/api/cust/pwd/login使用密码登录接口-正案例'''
        registNo=cx_old_registNo()
        data={"registNo":registNo,"password":"123456","gaid":"Exception:null"}
        r=requests.post(host_api+"/api/cust/pwd/login",data=json.dumps(data),headers=head_api,verify=False)
        t=r.json()
        self.assertEqual(t['errorCode'],0)
        token=t['data']['token']
        self.assertIsNotNone(token)
    def test_update_pwd(self):
        '''【FeriaRapida】/api/cust/pwd/update更新用户密码接口-正案例'''
        test_data=login_code()
        registNo=test_data[0]
        head=test_data[1]
        data2={"registNo":registNo,"newPwd":"123456"}
        r=requests.post(host_api+"/api/cust/pwd/update",data=json.dumps(data2),headers=head,verify=False)
        s=r.json()
        self.assertEqual(s['errorCode'],0)
    def test_auth_cert(self):
        '''【FeriaRapida】/api/cust/auth/cert身份认证接口-正案例'''
        st=random_four_zm()
        test_data=login_code()
        registNo=test_data[0]
        head=test_data[1]
        data2={"birthdate":"1999-5-18","civilStatus":"10050001","curp":st+"990518MM"+st+"V8","delegationOrMunicipality":"zxcvbbbccxxx","education":"10190005","fatherLastName":"WANG","gender":"10030001",
              "motherLastName":"LIU","name":"SHUANG","outdoorNumber":"qweetyyu","phoneNo":registNo,"postalCode":"55555","state":"11130001","street":"444444","suburb":"asdfhhj","email":""}
        r=requests.post(host_api+'/api/cust/auth/cert',data=json.dumps(data2),headers=head)
        s=r.json()
        custNo=s['data']['custNo']
        self.assertEqual(s['errorCode'],0)
        self.assertIsNotNone(custNo)
        sql="select CERT_AUTH from cu_cust_auth_dtl  where CUST_NO='"+custNo+"';"  #cu_客户认证信息明细表
        cert_auth=DataBase(which_db).get_one(sql)
        self.assertEqual(cert_auth[0],1)
    def test_auth_review(self):
        '''【FeriaRapida】/api/cust/auth/review接口-正案例'''
        test_data=for_test_auth_other()
        custNo=test_data[1]
        registNo=test_data[0]
        head=test_data[2]
        data1={"certType":"WORK","custNo":custNo}
        r1=requests.post(host_api+'/api/cust/auth/review',data=json.dumps(data1),headers=head)
        s1=r1.json()
        self.assertEqual(s1['errorCode'],0)
    def test_auth_work(self):
        '''【FeriaRapida】/api/cust/auth/work接口（客户工作情况）-正案例'''
        test_data=for_test_auth_other()
        custNo=test_data[1]
        head=test_data[2]
        data2={"companyAddress":"","companyName":"","companyPhone":"","custNo":custNo,"income":"10870004","industry":"","jobType":"10130006"}#工作收入来源
        r2=requests.post(host_api+'/api/cust/auth/work',data=json.dumps(data2),headers=head)
        s2=r2.json()
        self.assertEqual(s2['errorCode'],0)
    def test_app_grab_data(self):
        '''【FeriaRapida】/api/common/grab/app_grab_data接口-正案例-app第三个页面接口（抓取用户手机短信，通讯录，设备信息，已安装app等信息）'''
        test_data=for_test_auth_other()
        custNo=test_data[1]
        registNo=test_data[0]
        head=test_data[2]
        #设备信息
        data4={"appNo":"201","phoneNo":registNo,"dataType":"11090003","pageGet":"10000001","recordTime":"1621332187810","grabData":{"ipAddress":"2409:8162:a46:5405:1:0:107f:acec%20","ipResolveCit":"2409:8162:a46:5405:1:0:107f:acec%20",
        "ipResolveCom":"2409:8162:a46:5405:1:0:107f:acec%20","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc","mac":"A2:B4:74:63:FB:40","phoneNo":registNo,"recordBehavior":"抓取设备数据","recordTime":"1621332187810","userId":custNo,"mobileBrand":"HUAWEI","mobileModel":"LIO-AL00","systemVersion":"10","otherInfo":"274b98eb5c8aed06"},"custNo":custNo}
        #联系人
        data5={"appNo":"201","phoneNo":registNo,"dataType":"11090002","pageGet":"10000001","recordTime":"1621332187811","grabData":{"data":
        [{"contactName":"test","contactNo":"888 845 5666","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc",
          "mac":"A2:B4:74:63:FB:40","phoneNo":registNo,"recordBehavior":"联系人列表抓取","recordTime":"1621332187811","userId":custNo},{"contactName":"test2","contactNo":"888 335 5777",
        "deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc","mac":"A2:B4:74:63:FB:40","phoneNo":registNo,"recordBehavior":"联系人列表抓取",
        "recordTime":"1621332187811","userId":custNo}]},"custNo":custNo}
        #短信内容
        data6={"appNo":"201","phoneNo":registNo,"dataType":"11090005","pageGet":"10000001","recordTime":"1621332187836","grabData":{"data":[{"body":"【中国农业银行】您尾号8579账户05月18日17:02完成支付宝交易人民币-5000.00，余额9999999999.19。","address":"95599","date":"2021-05-18 17:02:48.863","dateSent":"2021-05-18 17:02:46.000","sender":"95599","kind":"SmsMessageKind.Received"}]},"custNo":custNo}
        #设备信息
        data7={"appNo":"201","phoneNo":registNo,"dataType":"11090004","pageGet":"10000001","recordTime":"1621332187838","grabData":{"latitude":"30.550366","longitude":"104.062236","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc","mac":"A2:B4:74:63:FB:40","phoneNo":registNo,"recordBehavior":"11000003","recordTime":"1621332187838","userId":custNo},"custNo":custNo}
        #已安装应用
        data8={"appNo":"201","phoneNo":registNo,"dataType":"11090001","pageGet":"10000001","recordTime":"1621332187731","grabData":{"data":[{"appName":"安全教育平台","appPackage":"com.jzzs.ParentsHelper","appVersionNo":"1.7.0","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc","installTime":1599480832637,"lastUpdateTime":1618934047038,"mac":"A2:B4:74:63:FB:40","phoneNo":registNo,"recordBehavior":"App列表抓取","recordTime":"1621332187731","userId":custNo}]},"custNo":custNo}
        data0=[data4,data5,data6,data7,data8]
        for data0 in data0:
            r0=requests.post(host_api+'/api/common/grab/app_grab_data',data=json.dumps(data0),headers=head)  #抓取用户手机短信，通讯录，已安装app等信息
            t0=r0.json()
            self.assertEqual(t0['errorCode'],0)
            time.sleep(1)
    def test_auth_contact(self):
        '''【FeriaRapida】/api/cust/auth/other/contact接口(填写联系人联系方式)app第四个页面-正案例'''
        test_data=for_test_auth_other()
        custNo=test_data[1]
        head=test_data[2]
        data9={"contacts":[{"name":"test","phone":"8888455666","relationship":"10110004"},{"name":"test2","phone":"8883355777","relationship":"10110003"}],"custNo":custNo}
        r9=requests.post(host_api+'/api/cust/auth/other/contact',data=json.dumps(data9),headers=head)#最后一步，填写2个联系人的联系方式
        t9=r9.json()
        self.assertEqual(t9['errorCode'],0)
    def test_apply_loan(self):
        '''【FeriaRapida】/api/loan/apply申请贷款接口-正案例'''
        test_data=for_apply_loan()
        custNo=test_data[0]
        head=test_data[1]
        data10={"custNo":custNo}
        r=requests.post(host_api+'/api/loan/apply',data=json.dumps(data10),headers=head)
        self.assertEqual(r.status_code,200)
        t=r.json()
        self.assertIsNotNone(t['data']['loanNo'])
    def test_bank_auth(self):
        '''【FeriaRapida】/api/cust/auth/bank绑定银行卡接口-正案例'''
        bank_acct_no=str(random.randint(1000,9999))
        test_data=for_bank_auth()
        custNo=test_data[0]
        head=test_data[1]
        data={"bankCode":"10020037","clabe":"138455214411441118","custNo":custNo}
        r=requests.post(host_api+'/api/cust/auth/bank',data=json.dumps(data),headers=head)
        self.assertEqual(r.status_code,200)
        t=r.json()
        self.assertEqual(t['errorCode'],0)                                    #改为4位随机数
        sql="update cu_cust_bank_card_dtl set BANK_ACCT_NO='"+bank_acct_no+"' where CUST_NO='"+custNo+"';"
        DataBase(which_db).executeUpdateSql(sql)  #防止被真实放款给该银行卡
    @classmethod
    def tearDownClass(cls): #在所有用例都执行完之后运行的
        DataBase(which_db).closeDB()
        print('我是tearDownClass，我位于多有用例运行的结束')
#
# if __name__ == '__main__':
#     suite = unittest.TestLoader().loadTestsFromTestCase(App_Api_Test)
#     runner = HTMLTestRunner(
#         title="lanaPlus接口测试-带截图，饼图，折线图，历史结果查看的测试报告",
#         description="这是描述",
#         stream=open("./App_Api_Test_Report.html", "wb"),
#         verbosity=1000,
#         retry=3,      #失败重试次数
#         save_last_try=True)
#     runner.run(suite)
