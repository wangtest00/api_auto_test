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
    def test_loan_latest(self):
        '''【lanaPlus】/api/loan/latest/registNo获取最近一笔贷款接口-已有一笔贷款（贷后正常状态）正案例'''
        registNo=cx_registNo()
        headt_api=headtt(registNo)
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
