from api_auto_test.public.base_lp import *
from api_auto_test.public.dataBase import *
from api_auto_test.public.var_lp import *
import random,io
import unittest,requests,json
from HTMLTestRunner_Chart import HTMLTestRunner

class DaiQian_Api_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  #在所有用例执行之前运行的
        print('我是setUpclass，我位于所有用例的开始')
    def setUp(self):  #每个用例运行之前运行的
        print('setup_test')
    def tearDown(self): #每个用例运行之后运行的
        print('teardown_test')
    def test_check_user_stat(self):
        '''【lanaPlus】/api/cust/check/user/state检查用户状态接口-（验证是否已设置密码）正案例'''
        registNo=str(random.randint(8000000000,9999999999)) #10位随机数作为手机号，未设置密码
        data={"registNo": registNo}
        r=requests.post(host_api+'/api/cust/check/user/state',data=json.dumps(data),headers=head_api,verify=False)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertFalse(t['data']['hasPwd'])
        phone='8129467919'                    #已设置密码
        data={"registNo": phone}
        r=requests.post(host_api+'/api/cust/check/user/state',data=json.dumps(data),headers=head_api,verify=False)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertTrue(t['data']['hasPwd'])

    def test_login_code(self):    #函数名要以test开头，否则不会被执行
        '''【lanaPlus】/api/cust/login注册登录接口-正案例'''      #用例描述，在函数下，用三个单引号里面写用例描述
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
        '''【lanaPlus】/api/cust/pwd/login使用密码登录接口-正案例'''
        registNo=cx_old_registNo()
        data={"registNo":registNo,"password":"123456","gaid":"Exception:null"}
        r=requests.post(host_api+"/api/cust/pwd/login",data=json.dumps(data),headers=head_api,verify=False)
        t=r.json()
        self.assertEqual(t['errorCode'],0)
        token=t['data']['token']
        self.assertIsNotNone(token)
    def test_update_pwd(self):
        '''【lanaPlus】/api/cust/pwd/update更新用户密码接口-正案例'''
        registNo=str(random.randint(8000000000,9999999999)) #10位随机数作为手机号
        head=login_code(registNo)
        data2={"registNo":registNo,"newPwd":"123456"}
        r=requests.post(host_api+"/api/cust/pwd/update",data=json.dumps(data2),headers=head,verify=False)
        s=r.json()
        self.assertEqual(s['errorCode'],0)
    def test_auth_cert(self):
        '''【lanaPlus】/api/cust/auth/cert身份认证接口-正案例'''
        st=random_four_zm()
        registNo=str(random.randint(8000000000,9999999999)) #10位随机数作为手机号
        head=login_code(registNo)
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
        '''【lanaPlus】/api/cust/auth/review接口-正案例'''
        test_data=for_test_auth_other()
        custNo=test_data[1]
        registNo=test_data[0]
        head=test_data[2]
        data1={"certType":"WORK","custNo":custNo}
        r1=requests.post(host_api+'/api/cust/auth/review',data=json.dumps(data1),headers=head)
        s1=r1.json()
        self.assertEqual(s1['errorCode'],0)
    def test_auth_work(self):
        '''【lanaPlus】/api/cust/auth/work接口（客户工作情况）-正案例'''
        test_data=for_test_auth_other()
        custNo=test_data[1]
        head=test_data[2]
        data2={"companyAddress":"","companyName":"","companyPhone":"","custNo":custNo,"income":"10870004","industry":"","jobType":"10130006"}#工作收入来源
        r2=requests.post(host_api+'/api/cust/auth/work',data=json.dumps(data2),headers=head)
        s2=r2.json()
        self.assertEqual(s2['errorCode'],0)
    def test_app_grab_data(self):
        '''【lanaPlus】/api/common/grab/app_grab_data接口-正案例-app第三个页面接口（抓取用户手机短信，通讯录，设备信息，已安装app等信息）'''
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
        '''【lanaPlus】/api/cust/auth/other/contact接口(填写联系人联系方式)app第四个页面-正案例'''
        test_data=for_test_auth_other()
        custNo=test_data[1]
        head=test_data[2]
        data9={"contacts":[{"name":"test","phone":"8888455666","relationship":"10110004"},{"name":"test2","phone":"8883355777","relationship":"10110003"}],"custNo":custNo}
        r9=requests.post(host_api+'/api/cust/auth/other/contact',data=json.dumps(data9),headers=head)#最后一步，填写2个联系人的联系方式
        t9=r9.json()
        self.assertEqual(t9['errorCode'],0)
    def test_apply_loan(self):
        '''【lanaPlus】/api/loan/apply申请贷款接口-正案例'''
        test_data=for_apply_loan()
        custNo=test_data[0]
        head=test_data[1]
        data10={"custNo":custNo}
        r=requests.post(host_api+'/api/loan/apply',data=json.dumps(data10),headers=head)
        self.assertEqual(r.status_code,200)
        t=r.json()
        self.assertIsNotNone(t['data']['loanNo'])
    def test_bank_auth_01(self):
        '''【lanaPlus】/api/cust/auth/bank绑定银行卡接口-正案例'''
        bank_acct_no=str(random.randint(1000,9999))
        test_data=for_bank_auth()
        custNo=test_data[0]
        head=test_data[1]
        data={"bankCode":"10020037","clabe":"138455214411441118","custNo":custNo}
        r=requests.post(host_api+'/api/cust/auth/bank',data=json.dumps(data),headers=head)
        t=r.json()
        self.assertEqual(t['errorCode'],0)                                    #改为4位随机数
        sql="update cu_cust_bank_card_dtl set BANK_ACCT_NO='"+bank_acct_no+"' where CUST_NO='"+custNo+"';"
        DataBase(which_db).executeUpdateSql(sql)  #防止被真实放款给该银行卡
    def test_bank_auth_02(self):
        '''【lanaPlus】/api/cust/auth/bank绑定银行卡接口(有在贷不能更换银行卡)-正案例'''
        list=cx_registNo_04()
        registNo=list[0]
        custNo=list[1]
        headt_api=login_code(registNo)
        data={"bankCode":"10020037","clabe":"138455214411441118","custNo":custNo}
        r=requests.post(host_api+'/api/cust/auth/bank',data=json.dumps(data),headers=headt_api)
        t=r.json()
        self.assertEqual(t['errorCode'],30001)
        self.assertEqual(t['message'],'Su préstamo no ha sido liquidado y CLABE no se puede modificar temporalmente. Modifíquelo después de que se complete el pago.')
    def test_bank_auth_03(self):
        '''【lanaPlus】/api/cust/auth/bank绑定银行卡接口(银行卡黑名单能正常绑卡，但是会被拒)-正案例'''
        test_data=for_bank_auth()
        custNo=test_data[0]
        head=test_data[1]
        loanNo=test_data[2]
        data={"bankCode":"10020008","clabe":"012050027670348650","custNo":custNo}
        r=requests.post(host_api+'/api/cust/auth/bank',data=json.dumps(data),headers=head)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        beforeStat=cx_beforeStat_afterStat(loanNo)
        self.assertEqual('10260006',beforeStat[0])  #验证贷前状态是否更新为【拒绝】
    def test_bank_auth_04(self):
        '''【lanaPlus】/api/cust/auth/bank绑定银行卡接口(客户未认证，不能绑卡)-正案例'''
        registNo=cx_registNo_07()
        headt_api=login_code(registNo)
        data={"bankCode":"10020037","clabe":"138455214411441118","custNo":''}
        r=requests.post(host_api+'/api/cust/auth/bank',data=json.dumps(data),headers=headt_api)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],30001)
        self.assertEqual(t['message'],'custNoParámetro anormal ')
    def test_loan_apply(self):
        '''【lanaPlus】/api/loan/apply  申请贷款接口(复客进件)-正案例'''
        custNo=get_yijieqing_custNo()
        sql="select REGIST_NO from cu_cust_reg_dtl where CUST_NO='"+custNo+"';"
        registNo=DataBase(which_db).get_one(sql)
        phone=registNo[0]
        headt_api=login_code(phone)
        data={"custNo":custNo}
        r=requests.post(host_api+'/api/loan/apply',data=json.dumps(data),headers=headt_api)#申请贷款
        t=r.json()
        #print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertEqual('10260001',t['data']['beforeStat'])  #验证贷前状态是否更新为【审批中】
        self.assertFalse(t['data']['firstApply'])
        self.assertIsNone(t['data']['matchId'])
        self.assertEqual(t['data']['recentLoanDetail']['loanStat'],'UNDER_RISK')
        self.assertIsNone(t['data']['recentLoanDetail']['certStatus'])
        self.assertIsNone(t['data']['recentLoanDetail']['paymentDetail'])
        self.assertIsNone(t['data']['recentLoanDetail']['trailPaymentDetail'])
        self.assertIsNone(t['data']['recentLoanDetail']['repaymentDetail'])
        self.assertIsNone(t['data']['recentLoanDetail']['applyButtonDetail'])
        self.assertIsNone(t['data']['recentLoanDetail']['reapplyDate'])
    def test_bank_codes(self):
        '''【lanaPlus】/api/common/bank/codes?types=1002获取银行卡码值及前缀接口-正案例'''
        registNo=cx_registNo_10()
        headt_api=login_code(registNo)
        r=requests.get(host_api+"/api/common/bank/codes?types=1002",headers=headt_api)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(t,{'data': [{'valName': 'ABC CAPITAL', 'valCode': '10020037', 'preNums': '138'}, {'valName': 'ACCENDO BANCO', 'valCode': '10020020', 'preNums': '102'}, {'valName': 'ACTINVER', 'valCode': '10020034', 'preNums': '133'}, {'valName': 'AFIRME', 'valCode': '10020018', 'preNums': '062'}, {'valName': 'AKALA', 'valCode': '10020067', 'preNums': '638'}, {'valName': 'AMERICAN EXPRES', 'valCode': '10020021', 'preNums': '103'}, {'valName': 'AUTOFIN', 'valCode': '10020030', 'preNums': '128'}, {'valName': 'AZTECA', 'valCode': '10020029', 'preNums': '127'}, {'valName': 'BAJIO', 'valCode': '10020011', 'preNums': '030'}, {'valName': 'BANAMEX', 'valCode': '10020007', 'preNums': '002'}, {'valName': 'BANCO FINTERRA', 'valCode': '10020047', 'preNums': '154'}, {'valName': 'BANCO S3', 'valCode': '10020052', 'preNums': '160'}, {'valName': 'BANCOMEXT', 'valCode': '10020001', 'preNums': '006'}, {'valName': 'BANCOPPEL', 'valCode': '10020036', 'preNums': '137'}, {'valName': 'BANCREA', 'valCode': '10020046', 'preNums': '152'}, {'valName': 'BANJERCITO', 'valCode': '10020003', 'preNums': '019'}, {'valName': 'BANK OF AMERICA', 'valCode': '10020022', 'preNums': '106'}, {'valName': 'BANKAOOL', 'valCode': '10020042', 'preNums': '147'}, {'valName': 'BANOBRAS', 'valCode': '10020002', 'preNums': '009'}, {'valName': 'BANORTE', 'valCode': '10020019', 'preNums': '072'}, {'valName': 'BANREGIO', 'valCode': '10020015', 'preNums': '058'}, {'valName': 'BANSEFI', 'valCode': '10020005', 'preNums': '166'}, {'valName': 'BANSI', 'valCode': '10020017', 'preNums': '060'}, {'valName': 'BARCLAYS', 'valCode': '10020031', 'preNums': '129'}, {'valName': 'BBASE', 'valCode': '10020041', 'preNums': '145'}, {'valName': 'BBVA BANCOMER', 'valCode': '10020008', 'preNums': '012'}, {'valName': 'BMONEX', 'valCode': '10020025', 'preNums': '112'}, {'valName': 'CAJA POP MEXICA', 'valCode': '10020075', 'preNums': '677'}, {'valName': 'CAJA TELEFONIST', 'valCode': '10020077', 'preNums': '683'}, {'valName': 'CB INTERCAM', 'valCode': '10020063', 'preNums': '630'}, {'valName': 'CI BOLSA', 'valCode': '10020064', 'preNums': '631'}, {'valName': 'CIBANCO', 'valCode': '10020040', 'preNums': '143'}, {'valName': 'COMPARTAMOS', 'valCode': '10020032', 'preNums': '130'}, {'valName': 'CONSUBANCO', 'valCode': '10020038', 'preNums': '140'}, {'valName': 'CREDICAPITAL', 'valCode': '10020071', 'preNums': '652'}, {'valName': 'CREDIT SUISSE', 'valCode': '10020028', 'preNums': '126'}, {'valName': 'CRISTOBAL COLON', 'valCode': '10020076', 'preNums': '680'}, {'valName': 'CoDi Valida', 'valCode': '10020083', 'preNums': '903'}, {'valName': 'DEUTSCHE', 'valCode': '10020027', 'preNums': '124'}, {'valName': 'DONDE', 'valCode': '10020045', 'preNums': '151'}, {'valName': 'ESTRUCTURADORES', 'valCode': '10020057', 'preNums': '606'}, {'valName': 'EVERCORE', 'valCode': '10020070', 'preNums': '648'}, {'valName': 'FINAMEX', 'valCode': '10020060', 'preNums': '616'}, {'valName': 'FINCOMUN', 'valCode': '10020065', 'preNums': '634'}, {'valName': 'FOMPED', 'valCode': '10020081', 'preNums': '689'}, {'valName': 'FONDO (FIRA)', 'valCode': '10020079', 'preNums': '685'}, {'valName': 'GBM', 'valCode': '10020054', 'preNums': '601'}, {'valName': 'HDI SEGUROS', 'valCode': '10020066', 'preNums': '636'}, {'valName': 'HIPOTECARIA FED', 'valCode': '10020006', 'preNums': '168'}, {'valName': 'HSBC', 'valCode': '10020010', 'preNums': '021'}, {'valName': 'ICBC', 'valCode': '10020048', 'preNums': '155'}, {'valName': 'INBURSA', 'valCode': '10020012', 'preNums': '036'}, {'valName': 'INDEVAL', 'valCode': '10020082', 'preNums': '902'}, {'valName': 'INMOBILIARIO', 'valCode': '10020044', 'preNums': '150'}, {'valName': 'INTERCAM BANCO', 'valCode': '10020035', 'preNums': '136'}, {'valName': 'INVERCAP', 'valCode': '10020080', 'preNums': '686'}, {'valName': 'INVEX', 'valCode': '10020016', 'preNums': '059'}, {'valName': 'JP MORGAN', 'valCode': '10020024', 'preNums': '110'}, {'valName': 'LIBERTAD', 'valCode': '10020074', 'preNums': '670'}, {'valName': 'MASARI', 'valCode': '10020055', 'preNums': '602'}, {'valName': 'MIFEL', 'valCode': '10020013', 'preNums': '042'}, {'valName': 'MIZUHO BANK', 'valCode': '10020051', 'preNums': '158'}, {'valName': 'MONEXCB', 'valCode': '10020053', 'preNums': '600'}, {'valName': 'MUFG', 'valCode': '10020023', 'preNums': '108'}, {'valName': 'MULTIVA BANCO', 'valCode': '10020033', 'preNums': '132'}, {'valName': 'MULTIVA CBOLSA', 'valCode': '10020059', 'preNums': '613'}, {'valName': 'NAFIN', 'valCode': '10020004', 'preNums': '135'}, {'valName': 'PAGATODO', 'valCode': '10020043', 'preNums': '148'}, {'valName': 'PROFUTURO', 'valCode': '10020062', 'preNums': '620'}, {'valName': 'SABADELL', 'valCode': '10020049', 'preNums': '156'}, {'valName': 'SANTANDER', 'valCode': '10020009', 'preNums': '014'}, {'valName': 'SANTANDER2', 'valCode': '10020084', 'preNums': '814'}, {'valName': 'SCOTIABANK', 'valCode': '10020014', 'preNums': '044'}, {'valName': 'SHINHAN', 'valCode': '10020050', 'preNums': '157'}, {'valName': 'STP', 'valCode': '10020069', 'preNums': '646'}, {'valName': 'TRANSFER', 'valCode': '10020078', 'preNums': '684'}, {'valName': 'UNAGRA', 'valCode': '10020072', 'preNums': '656'}, {'valName': 'VALMEX', 'valCode': '10020061', 'preNums': '617'}, {'valName': 'VALUE', 'valCode': '10020056', 'preNums': '605'}, {'valName': 'VE POR MAS', 'valCode': '10020026', 'preNums': '113'}, {'valName': 'VECTOR', 'valCode': '10020058', 'preNums': '608'}, {'valName': 'VOLKSWAGEN', 'valCode': '10020039', 'preNums': '141'}], 'errorCode': 0, 'message': 'ÉXITO'}
)
    def test_feedback_codes(self):
        '''【lanaPlus】/api/common/feedback/codes?types=1111获取feedback码值接口-正案例'''
        registNo=cx_registNo_10()
        headt_api=login_code(registNo)
        r=requests.get(host_api+"/api/common/feedback/codes?types=1111",headers=headt_api)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(str(t['data']),"[{'valName': 'Acosado', 'valCode': '11110001', 'options': ['Me acosaron por mensajes de WhatsApp.', 'Me acosaron por mensajes de texto.', 'Me acosaron por una llamada telefónica.']}, {'valName': 'Aprobación es demasiado largo', 'valCode': '11110002', 'options': ['El tiempo de aprobación es demasiado largo.']}, {'valName': 'CLABE', 'valCode': '11110003', 'options': ['No sé cuál es mi cuenta CLABE.', 'Quiero cambiar mi cuenta CLABE.']}, {'valName': 'CURP', 'valCode': '11110004', 'options': ['La CURP marca error.', 'Necesito ayuda para completar la CURP.']}, {'valName': 'Depósito', 'valCode': '11110005', 'options': ['Apareció un error de limitación en la parte superior de la página.', 'He pagado pero el estatus no se ha actualizado.', 'La cuenta que ha pagado marca error.', 'No recibí el depósito.', 'Pagos múltiples.']}, {'valName': 'El tiempo de carga es demasiado largo', 'valCode': '11110007', 'options': ['Carga lenta en la página de inicio.', 'Carga prolongada de la página de pago']}, {'valName': 'Error de red', 'valCode': '11110006', 'options': ['Apareció un error de [01] en la parte superior de la página.', 'Apareció un error de [02] en la parte superior de la página.', 'Apareció un error de [03] en la parte superior de la página.', 'Apareció un error de [04] en la parte superior de la página.']}, {'valName': 'Foto', 'valCode': '11110008', 'options': ['Informar un error después de cargar la foto.', 'La cámara funciona mal y deseo cargar fotos.', 'No se pudo cargar la foto.']}, {'valName': 'INE', 'valCode': '11110009', 'options': ['Informe del error después de cargar el INE.', 'No se pudo cargar el INE.', 'Reemplace la credencial INE.', 'Sin credencial de INE / perdida', 'Sin credencial física INE, quiero subir fotos.']}, {'valName': 'LanaCoin', 'valCode': '11110010', 'options': ['Quiero saber cómo usar mi LanaCoin.']}, {'valName': 'Monto del préstamo', 'valCode': '11110011', 'options': ['Quiero elegir el monto del préstamo que más me convenga por mí mismo.', 'Quiero un monto de préstamo mayor.', 'Quiero una cantidad de préstamo menor.']}, {'valName': 'Otros', 'valCode': '11110012', 'options': ['Otros.']}, {'valName': 'Sorteo', 'valCode': '11110013', 'options': ['Gané el sorteo, pero no obtuve el premio.']}, {'valName': 'Teléfono', 'valCode': '11110014', 'options': ['Cambiar el número de teléfono móvil.', 'Error al registrar el número de teléfono móvil.', 'Número de teléfono incompatible.']}]")
    def test_get_states(self):
        '''【lanaPlus】/api/common/codes?types=1019%2C1005%2C1113获取州列表接口-正案例'''
        registNo=cx_registNo_07()
        headt_api=login_code(registNo)
        r=requests.get(host_api+'/api/common/codes?types=1019%2C1005%2C1113',headers=headt_api)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(str(t),"{'data': {'1019': [{'valName': 'Licenciatura', 'valCode': '10190005', 'typeCode': '1019'}, {'valName': 'No Escolaridad', 'valCode': '10190001', 'typeCode': '1019'}, {'valName': 'Posgrado / Maestria', 'valCode': '10190006', 'typeCode': '1019'}, {'valName': 'Preparatoria/ Bachillerato', 'valCode': '10190004', 'typeCode': '1019'}, {'valName': 'Primaria', 'valCode': '10190002', 'typeCode': '1019'}, {'valName': 'Secundaria', 'valCode': '10190003', 'typeCode': '1019'}], '1113': [{'valName': 'Aguascalientes', 'valCode': '11130001', 'typeCode': '1113'}, {'valName': 'Baja California', 'valCode': '11130002', 'typeCode': '1113'}, {'valName': 'Baja California Sur', 'valCode': '11130003', 'typeCode': '1113'}, {'valName': 'Campeche', 'valCode': '11130004', 'typeCode': '1113'}, {'valName': 'Chiapas', 'valCode': '11130005', 'typeCode': '1113'}, {'valName': 'Chihuahua', 'valCode': '11130007', 'typeCode': '1113'}, {'valName': 'Ciudad de México', 'valCode': '11130006', 'typeCode': '1113'}, {'valName': 'Coahuila', 'valCode': '11130008', 'typeCode': '1113'}, {'valName': 'Colima', 'valCode': '11130009', 'typeCode': '1113'}, {'valName': 'Durango', 'valCode': '11130010', 'typeCode': '1113'}, {'valName': 'Guanajuato', 'valCode': '11130011', 'typeCode': '1113'}, {'valName': 'Guerrero', 'valCode': '11130012', 'typeCode': '1113'}, {'valName': 'Hidalgo', 'valCode': '11130013', 'typeCode': '1113'}, {'valName': 'Jalisco', 'valCode': '11130014', 'typeCode': '1113'}, {'valName': 'Michoacán', 'valCode': '11130016', 'typeCode': '1113'}, {'valName': 'Morelos', 'valCode': '11130017', 'typeCode': '1113'}, {'valName': 'México', 'valCode': '11130015', 'typeCode': '1113'}, {'valName': 'Nayarit', 'valCode': '11130018', 'typeCode': '1113'}, {'valName': 'Nuevo León', 'valCode': '11130019', 'typeCode': '1113'}, {'valName': 'Oaxaca', 'valCode': '11130020', 'typeCode': '1113'}, {'valName': 'Puebla', 'valCode': '11130021', 'typeCode': '1113'}, {'valName': 'Querétaro', 'valCode': '11130022', 'typeCode': '1113'}, {'valName': 'Quintana Roo', 'valCode': '11130023', 'typeCode': '1113'}, {'valName': 'San Luis Potosí', 'valCode': '11130024', 'typeCode': '1113'}, {'valName': 'Sinaloa', 'valCode': '11130025', 'typeCode': '1113'}, {'valName': 'Sonora', 'valCode': '11130026', 'typeCode': '1113'}, {'valName': 'Tabasco', 'valCode': '11130027', 'typeCode': '1113'}, {'valName': 'Tamaulipas', 'valCode': '11130028', 'typeCode': '1113'}, {'valName': 'Tlaxcala', 'valCode': '11130029', 'typeCode': '1113'}, {'valName': 'Veracruz', 'valCode': '11130030', 'typeCode': '1113'}, {'valName': 'Yucatán', 'valCode': '11130031', 'typeCode': '1113'}, {'valName': 'Zacatecas', 'valCode': '11130032', 'typeCode': '1113'}], '1005': [{'valName': 'Casado', 'valCode': '10050001', 'typeCode': '1005'}, {'valName': 'Divorced', 'valCode': '10050004', 'typeCode': '1005'}, {'valName': 'Soltero', 'valCode': '10050002', 'typeCode': '1005'}, {'valName': 'Unión libre', 'valCode': '10050005', 'typeCode': '1005'}, {'valName': 'Viudo', 'valCode': '10050003', 'typeCode': '1005'}]}, 'errorCode': 0, 'message': 'ÉXITO'}")
    def test_get_cust_coin_amount(self):
        '''【lanaPlus】/api/cust/coin/amount/个人中心获取用户lanacoin积分总数接口-正案例'''
        registNo='2222225555'
        headt_api=login_code(registNo)
        r=requests.get(host_api+'/api/cust/coin/amount/2222225555',headers=headt_api)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(t['data'],5311)
    def test_get_promote_total_bonus(self):
        '''【lanaPlus】/api/cust/coin/amount/分销-获取用户可提现总金额接口-正案例'''
        registNo='2222225555'
        headt_api=login_code(registNo)
        data={"phoneNo":registNo}
        r=requests.post(host_api+'/api/cust/promote/total/bonus/'+registNo,data=json.dumps(data),headers=headt_api)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(t['data'],'6014.00')
    def test_get_cust_promote_detail(self):
        '''【lanaPlus】/api/cust/promote/detail/分销-获取用户可提现详情接口-正案例'''
        registNo='2222225555'
        headt_api=login_code(registNo)
        data={"phoneNo":registNo}
        r=requests.post(host_api+'/api/cust/promote/detail/'+registNo,data=json.dumps(data),headers=headt_api)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(str(t['data']),"{'firstLevFanNum': 1017, 'firstLevFanWithdrawNum': 4, 'firstLevWithdrawBonus': '4200.00', 'secondLevFanNum': 15, 'secondLevFanWithdrawNum': 12, 'secondLevWithdrawBonus': '1310.00', 'thirdLevFanNum': 4, 'thirdLevFanWithdrawNum': 3, 'thirdLevWithdrawBonus': '504.00', 'totalFanNum': 1036, 'totalBonus': '6014.00', 'withdrawDetail': {'custName': 'AUTO ZIXUAN PRO TEST', 'custAcctBank': 'ABC CAPITAL', 'custAcctBankCode': '10020037', 'clabe': '46206', 'alreadyWithdrawAmt': '6000.00', 'availableAmt': '14.00', 'availableWithdraw': True, 'disableWithdrawDesc': None}}")
    def test_get_cust_promote_withdraw_his(self):
        '''【lanaPlus】/api/cust/promote/withdraw/history/分销-获取用户提现历史详情接口-正案例'''
        registNo='2222225555'
        headt_api=login_code(registNo)
        data={"phoneNo":registNo}
        r=requests.post(host_api+'/api/cust/promote/withdraw/history/'+registNo,data=json.dumps(data),headers=headt_api)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(str(t['data']),"[{'withdrawTime': '1634793586000', 'withdrawAmt': '100', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1632381569000', 'withdrawAmt': '1000', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630924125000', 'withdrawAmt': '200', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630909596000', 'withdrawAmt': '200', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630647131000', 'withdrawAmt': '100', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630646098000', 'withdrawAmt': '100', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630577499000', 'withdrawAmt': '200', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630563133000', 'withdrawAmt': '100', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630500417000', 'withdrawAmt': '100', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630499054000', 'withdrawAmt': '100', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630494153000', 'withdrawAmt': '100', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630489446000', 'withdrawAmt': '100', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630489440000', 'withdrawAmt': '100', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630489432000', 'withdrawAmt': '100', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630488375000', 'withdrawAmt': '100', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630488297000', 'withdrawAmt': '100', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630466695000', 'withdrawAmt': '100', 'withdrawStat': 'WITHDRAW'}, {'withdrawTime': '1630407942000', 'withdrawAmt': '100', 'withdrawStat': 'WITHDRAW'}, {'withdrawTime': '1630407086000', 'withdrawAmt': '400', 'withdrawStat': 'WITHDRAW'}, {'withdrawTime': '1630406055000', 'withdrawAmt': '100', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630406053000', 'withdrawAmt': '100', 'withdrawStat': 'WITHDRAW'}, {'withdrawTime': '1630406050000', 'withdrawAmt': '100', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630405976000', 'withdrawAmt': '100', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630405959000', 'withdrawAmt': '1500', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630403793000', 'withdrawAmt': '500', 'withdrawStat': 'WITHDRAW'}, {'withdrawTime': '1630400816000', 'withdrawAmt': '100', 'withdrawStat': 'UNDER_WITHDRAW'}, {'withdrawTime': '1630400809000', 'withdrawAmt': '100', 'withdrawStat': 'WITHDRAW'}]")
    def test_get_cust_invitation_code(self):
        '''【lanaPlus】/api/cust/invitation/code/分销-获取用户邀请码接口-正案例'''
        registNo='2222225555'
        headt_api=login_code(registNo)
        data={"phoneNo":registNo}
        r=requests.post(host_api+'/api/cust/invitation/code/'+registNo,data=json.dumps(data),headers=headt_api)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
    def test_feedback_record(self):
        '''【lanaPlus】/api/cust/feedback/record-提交feedback记录接口-正案例'''
        registNo='2222225555'
        headt_api_f=login_code_f(registNo)
        custNo='C2012108318120925314188222464'
        files={'custNo':(None,custNo),'phoneNo':(None,registNo),'feedbackDesc':(None,'test123456789'),'feedbackType':(None,'11110007'),'feedbackPage':(None,'NEW'),
               'feedbackOption':(None,'Carga prolongada de la página de pago'),'imgs':('key.png',open(r'D:\pic\app.jpg', 'rb'),'text/plain')}
        r=requests.post(host_api+"/api/cust/feedback/record",files=files,headers=headt_api_f)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
    def test_get_cust_promote_switch(self):
        '''【lanaPlus】/api/cust/promote/switch/分销-获取三级分销开关状态接口-正案例'''
        registNo='2222225555'
        headt_api=login_code(registNo)
        data={"phoneNo":registNo}
        r=requests.post(host_api+'/api/cust/promote/switch/'+registNo,data=json.dumps(data),headers=headt_api)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertTrue(t['data'])
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
