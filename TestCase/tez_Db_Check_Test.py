import unittest
from api_auto_test.public.base_tez import *
from api_auto_test.dataBase.cx_table_tez import *


class Tez_Db_Check_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  #在所有用例执行之前运行的
        print('我是setUpclass，我位于所有用例的开始')
    def setUp(self):  #每个用例运行之前运行的
        print('setup_test')
    def tearDown(self): #每个用例运行之后运行的
        print('teardown_test')
    def test_check_withdraw_success_01(self):
        '''【tez_loan】放款成功后，未出账单，无还款和减免，相关10个表关键字段值核对-正案例'''
        loan_no=cx_loan_no()
        print(loan_no)
        t1=cx_lo_loan_dtl(loan_no)
        self.assertEqual(t1,[('2000.00', '2000.00', '1', '10260005', '10270001')])
        t2=cx_fin_tran_pay_dtl(loan_no)
        self.assertEqual(t2,[('1300.00', '10420002')])
        t3=cx_pay_tran_dtl(loan_no,'10330001')
        self.assertEqual(t3,[('10320003', '10330001', 'C', '1300.00', '10220002')])
        t4=cx_lo_loan_prod_rel(loan_no)
        self.assertEqual(t4,('10003', '10003'))
        t5=cx_dc_flow_dtl(loan_no)   #未出账单不生成该表数据
        self.assertEqual(t5,[])
        t6=cx_lo_loan_plan_dtl(loan_no)#未出账单不生成该表数据
        self.assertEqual(t6,())
        t7=cx_fin_ac_dtl(loan_no)
        self.assertEqual(t7,[('700.00', '10440001', '10350002')])
        t8=cx_fin_ad_dtl(loan_no)
        repay_date=jisuan_repay_date(loan_no)
        print(repay_date)
        self.assertEqual(t8,[(repay_date[0], '700.00', '10360002', '10370001', '10440001')])
        t9=cx_fin_ad_detail_dtl(loan_no)
        self.assertEqual(t9,[(repay_date[0], '20', '88.00', '10370001', '10440001')])
        t10=cx_fin_rc_dtl(loan_no)
        self.assertEqual(t10,[('912.00', '10440002', '10390002')])
    def test_check_withdraw_success_02(self):
        '''【tez_loan】放款成功后，正常-已出账单，无还款和减免，相关10个表关键字段值核对-正案例'''
        loan_no=cx_loan_no2()
        print(loan_no)
        t1=cx_lo_loan_dtl(loan_no)
        self.assertEqual(t1,[('2000.00', '2000.00', '1', '10260005', '10270002')])
        t2=cx_fin_tran_pay_dtl(loan_no)
        self.assertEqual(t2,[('1300.00', '10420002')])
        t3=cx_pay_tran_dtl(loan_no,'10330001')
        self.assertEqual(t3,[('10320003', '10330001', 'C', '1300.00', '10220002')])
        t4=cx_lo_loan_prod_rel(loan_no)
        self.assertEqual(t4,('10003', '10003'))
        t5=cx_dc_flow_dtl(loan_no)
        self.assertEqual(t5,[('1001', '1', '2000.00', 'C'), ('1201', '1', '14.00', 'C'), ('1202', '1', '14.00', 'D'), ('1401', '1', '36.00', 'C'), ('1402', '1', '36.00', 'D'), ('2001', '1', '650.00', 'C'), ('2002', '1', '650.00', 'D')])
        t6=cx_lo_loan_plan_dtl(loan_no)
        repay_date=jisuan_repay_date(loan_no)
        self.assertEqual(t6,((1, repay_date[0], '10270002'),))
        t7=cx_fin_ac_dtl(loan_no)
        #print(t7)                                   #内部账户                                        #外部账户
        self.assertEqual(t7,[("(Decimal('700.00'), '10440001', '10350002')", "(Decimal('1300.00'), '10440002', '10350002')")])
        t8=cx_fin_ad_dtl(loan_no)
        self.assertEqual(t8,[(repay_date[0], '2000.00', '10360001', '10370001', '10440002')])
        t9=cx_fin_ad_detail_dtl(loan_no)
        self.assertEqual(t9,[(repay_date[0], '1001', '2000.00', '10370001', '10440002')])
        t10=cx_fin_rc_dtl(loan_no)
        self.assertEqual(t10,[('1300.00', '10440002', '10390002')])
    @classmethod
    def tearDownClass(cls): #在所有用例都执行完之后运行的
        DataBase(which_db).closeDB()
        print('我是tearDownClass，我位于多有用例运行的结束')