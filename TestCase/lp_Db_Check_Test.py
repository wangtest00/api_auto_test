from api_auto_test.public.base_lp import *
from api_auto_test.public.dataBase import *
from api_auto_test.public.var_lp import *
from api_auto_test.public.cx_table import *
import unittest,requests,json,decimal
from HTMLTestRunner_Chart import HTMLTestRunner


class LP_Db_Check_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  #在所有用例执行之前运行的
        print('我是setUpclass，我位于所有用例的开始')
    def setUp(self):  #每个用例运行之前运行的
        print('setup_test')
    def tearDown(self): #每个用例运行之后运行的
        print('teardown_test')
    def test_check_withdraw_success(self):
        '''【lanaPlus】放款成功后，无还款和减免，相关10个表关键字段值核对-正案例'''
        loan_no=cx_loan_no()
        print(loan_no)
        t1=cx_lo_loan_dtl(loan_no)
        self.assertEqual(t1,[('1500.00', '1500.00', '3', '10000001', '10260005', '10270002', 'None')])
        t2=cx_fin_tran_pay_dtl(loan_no)
        self.assertEqual(t2,[('1500.00', '10420002')])
        t3=cx_pay_tran_dtl(loan_no)
        self.assertEqual(t3,[('10320003', '10330001', 'C', '1500.00', '10220002')])
        t4=cx_lo_loan_prod_rel(loan_no)
        self.assertEqual(t4,('28070110', '28070110'))
        t5=cx_dc_flow_dtl(loan_no)
        self.assertEqual(t5,[('1001', '1', '500.00', 'C'), ('1001', '2', '500.00', 'C'), ('1001', '3', '500.00', 'C'), ('1201', '1', '100.00', 'C'), ('1201', '2', '100.00', 'C'), ('1201', '3', '100.00', 'C')])
        t6=cx_lo_loan_plan_dtl(loan_no)
        repay_date=jisuan_repay_date(loan_no)
        self.assertEqual(t6,((1, repay_date[0], '10270002'), (2, repay_date[1], '10270002'), (3, repay_date[2], '10270002')))
        t7=cx_fin_ac_dtl(loan_no)
        self.assertEqual(t7,[('1500.00', '10440002', '10350002')])
        t8=cx_fin_ad_dtl(loan_no)
        self.assertEqual(t8,[(repay_date[0], '600.00', '10360001', '10370001', '10440002'), (repay_date[1], '600.00', '10360001', '10370001', '10440002'), (repay_date[2], '600.00', '10360001', '10370001', '10440002')])
        t9=cx_fin_ad_detail_dtl(loan_no)
        self.assertEqual(t9,[(repay_date[0], '1001', '500.00', '10370001', '10440002'), (repay_date[0], '1201', '100.00', '10370001', '10440002'), (repay_date[1], '1001', '500.00', '10370001', '10440002'), (repay_date[1], '1201', '100.00', '10370001', '10440002'), (repay_date[2], '1001', '500.00', '10370001', '10440002'), (repay_date[2], '1201', '100.00', '10370001', '10440002')])
        t10=cx_fin_rc_dtl(loan_no)
        self.assertEqual(t10,[('1500.00', '10440002', '10390004')])
    # def test_check_withdraw_failed(self):
    #     '''【lanaPlus】无还款无对公和减免，放款失败后回滚数据（每次新造数据and相关11个表关键字段值核对）-正案例'''
    #     loan_no=for_stp_payout_fail()
    #     print(loan_no)
    #     t1=cx_lo_loan_dtl(loan_no)
    #     self.assertEqual(t1,[('1500.00', 'None', '3', '10000001', '10260004', 'None', 'None')])
    #     t2=cx_fin_tran_pay_dtl(loan_no)
    #     self.assertEqual(t2,[('1500.00', '10420003')])
    #     t3=cx_pay_tran_dtl(loan_no)
    #     self.assertEqual(t3,[('10320003', '10330001', 'C', '1500.00', '10220003')])
    #     t4=cx_lo_loan_prod_rel(loan_no)
    #     self.assertEqual(t4,('28070110', '28070110'))
    #     t5=cx_dc_flow_dtl(loan_no)
    #     self.assertEqual(t5,[])
    #     t6=cx_lo_loan_plan_dtl(loan_no)
    #     self.assertEqual(t6,())
    #     t7=cx_fin_ac_dtl_for_huigun(loan_no)
    #     self.assertIsNone(t7)
    #     t8=cx_fin_ad_dtl(loan_no)
    #     self.assertEqual(t8,[])
    #     t9=cx_fin_ad_detail_dtl(loan_no)
    #     self.assertEqual(t9,[])
    #     t10=cx_fin_rc_dtl_for_huigun(loan_no)
    #     self.assertIsNone(t10)
    #     t11=cx_pay_tran_log(loan_no)
    #     self.assertEqual(t11[0],'交易失败[cancelled]')
    #     self.assertEqual(t11[1],'10220003')
    @classmethod
    def tearDownClass(cls): #在所有用例都执行完之后运行的
        DataBase(which_db).closeDB()
        print('我是tearDownClass，我位于多有用例运行的结束')