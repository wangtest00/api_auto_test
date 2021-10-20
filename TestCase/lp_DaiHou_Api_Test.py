from api_auto_test.public.base_lp import *
from api_auto_test.public.dataBase import *
from api_auto_test.public.var_lp import *
import random
import unittest,requests,json
from HTMLTestRunner_Chart import HTMLTestRunner

class DaiHou_Api_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  #在所有用例执行之前运行的
        print('我是setUpclass，我位于所有用例的开始')
    def setUp(self):  #每个用例运行之前运行的
        print('setup_test')
    def tearDown(self): #每个用例运行之后运行的
        print('teardown_test')
    def test_loan_latest_01(self):
        '''【lanaPlus】/api/loan/latest/registNo获取最近一笔贷款接口-已有一笔贷款（贷后正常状态且未还过款）正案例'''
        registNo=cx_registNo()
        headt_api=login_code(registNo)
        r=requests.get(host_api+"/api/loan/latest/"+registNo,headers=headt_api,verify=False)
        t=r.json()
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(t['data']['repaymentDetail']['realPaymentAmt'],'1500.00')
        repaymentDetailList=t['data']['repaymentDetail']['repaymentDetailList']
        for i in range(len(repaymentDetailList)):
            print(repaymentDetailList[i])
            self.assertEqual(repaymentDetailList[i]['loanAmt'],'500.00')
            self.assertEqual(repaymentDetailList[i]['originalLoanAmt'],'500.00')
            self.assertEqual(repaymentDetailList[i]['repaymentAmt'],'600.00')
            self.assertEqual(repaymentDetailList[i]['alreadyRepaymentAmt'],None)
            self.assertEqual(repaymentDetailList[i]['originalRepaymentAmt'],'600.00')
            self.assertEqual(repaymentDetailList[i]['totalAfterFee'],'100.00')
            self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['feeValue'],'100.00')
            self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['originalFeeValue'],'100.00')
            self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['realRepayAmt'],'0.00')
            self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['reduceAmt'],'0.00')
            self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['order'],'2')
            self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['feeType'],None)
            self.assertEqual(repaymentDetailList[i]['overdueAmt'],None)
            self.assertEqual(repaymentDetailList[i]['originalOverdueAmt'],None)
            self.assertEqual(repaymentDetailList[i]['stat'],'NORMAL')
            self.assertEqual(repaymentDetailList[i]['deductionDetail']['otherReduceAmt'],None)
            self.assertEqual(repaymentDetailList[i]['deductionDetail']['coinDeductionAmt'],None)
            self.assertEqual(repaymentDetailList[i]['deductionDetail']['couponDeductionAmt'],None)
            if i==0:
                self.assertEqual(repaymentDetailList[i]['deductionDetail']['coinDeductionAble'],True)   #积分减免状态（首期可减免）
                self.assertEqual(repaymentDetailList[i]['deductionDetail']['couponDeductionAble'],True) #优惠券减免状态（首期可减免）
            else:
                self.assertEqual(repaymentDetailList[i]['deductionDetail']['coinDeductionAble'],False)   #积分减免状态（非首期不可减免）
                self.assertEqual(repaymentDetailList[i]['deductionDetail']['couponDeductionAble'],False) #优惠券减免状态（非首期不可减免）
    def test_loan_latest_02(self):
        '''【lanaPlus】/api/loan/latest/registNo获取最近一笔贷款接口-无在贷(已结清一笔贷款)正案例'''
        registNo=cx_registNo_02()
        headt_api=login_code(registNo)
        r=requests.get(host_api+"/api/loan/latest/"+registNo,headers=headt_api,verify=False)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        print(t['data'])
        self.assertEqual(t['data']['loanStat'],'NEW')
        self.assertIsNotNone(t['data']['loanNo'])
        self.assertIsNotNone(t['data']['custNo'])
        self.assertIsNone(t['data']['bankAcctInfo'])
        self.assertIsNone(t['data']['paymentDetail'])
        self.assertIsNone(t['data']['trailPaymentDetail'])
        self.assertIsNone(t['data']['repaymentDetail'])
        self.assertIsNone(t['data']['reapplyDate'])
        self.assertIsNotNone(t['data']['certStatus']['custNo'])
        self.assertEqual(t['data']['certStatus']['certAuth'],True)
        self.assertEqual(t['data']['certStatus']['kycAuth'],True)
        self.assertEqual(t['data']['certStatus']['workAuth'],True)
        self.assertEqual(t['data']['certStatus']['bankAuth'],False)    #目前bankauth字段无实际作用
        self.assertEqual(t['data']['certStatus']['otherContactAuth'],True)
    def test_loan_latest_03(self):
        '''【lanaPlus】/api/loan/latest/registNo获取最近一笔贷款接口-无在贷(已结清一笔贷款)正案例'''
        registNo=cx_registNo_03()
        headt_api=login_code(registNo)
        r=requests.get(host_api+"/api/loan/latest/"+registNo,headers=headt_api,verify=False)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)

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
