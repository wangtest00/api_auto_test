from api_auto_test.public.base_lp import *
from api_auto_test.public.dataBase import *
from api_auto_test.public.var_lp import *
import unittest,requests,json
from HTMLTestRunner_Chart import HTMLTestRunner


class LP_DaiHou_Api_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  #在所有用例执行之前运行的
        print('我是setUpclass，我位于所有用例的开始')
    def setUp(self):  #每个用例运行之前运行的
        print('setup_test')
    def tearDown(self): #每个用例运行之后运行的
        print('teardown_test')
    def test_loan_latest_00(self):
        '''【lanaPlus】/api/loan/latest/registNo获取最近一笔贷款接口-已有一笔贷款（贷后逾期状态且未还过款）正案例'''
        registNo=cx_registNo_00()
        headt_api=login_code(registNo)
        r=requests.get(host_api+"/api/loan/latest/"+registNo,headers=headt_api,verify=False)
        t=r.json()
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(t['data']['repaymentDetail']['realPaymentAmt'],'1500.00')
        repaymentDetailList=t['data']['repaymentDetail']['repaymentDetailList']
        for i in range(len(repaymentDetailList)):
            print(repaymentDetailList[i])
            print(i)
            self.assertEqual(repaymentDetailList[i]['loanAmt'],'500.00')
            self.assertEqual(repaymentDetailList[i]['originalLoanAmt'],'500.00')
            #self.assertEqual(repaymentDetailList[i]['repaymentAmt'],'600.00')
            self.assertEqual(repaymentDetailList[i]['alreadyRepaymentAmt'],None)
            self.assertEqual(repaymentDetailList[i]['totalAfterFee'],'100.00')
            self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['feeValue'],'100.00')
            self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['originalFeeValue'],'100.00')
            self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['realRepayAmt'],'0.00')
            #self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['reduceAmt'],'0.00')
            self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['order'],'2')
            self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['feeType'],None)
            self.assertEqual(repaymentDetailList[i]['deductionDetail']['otherReduceAmt'],None)
            if i==0:
                self.assertEqual(repaymentDetailList[i]['deductionDetail']['coinDeductionAble'],True)   #积分减免状态（首期可减免）
                self.assertEqual(repaymentDetailList[i]['deductionDetail']['couponDeductionAble'],True) #优惠券减免状态（首期可减免）
                self.assertEqual(repaymentDetailList[i]['originalRepaymentAmt'],'650.00')
                self.assertEqual(repaymentDetailList[i]['originalOverdueAmt'],'50.00')                  #首期逾期有滞纳金
                self.assertEqual(repaymentDetailList[i]['stat'],'OVERDUE')
                self.assertEqual(repaymentDetailList[i]['overdueAmt'],'50.00')
            else:
                self.assertEqual(repaymentDetailList[i]['deductionDetail']['coinDeductionAble'],False)   #积分减免状态（非首期不可减免）
                self.assertEqual(repaymentDetailList[i]['deductionDetail']['couponDeductionAble'],False) #优惠券减免状态（非首期不可减免）
                self.assertEqual(repaymentDetailList[i]['originalRepaymentAmt'],'600.00')
                self.assertEqual(repaymentDetailList[i]['originalOverdueAmt'],None)
                self.assertEqual(repaymentDetailList[i]['stat'],'NORMAL')
                self.assertEqual(repaymentDetailList[i]['overdueAmt'],None)
                self.assertEqual(repaymentDetailList[i]['repaymentAmt'],'600.00')
                self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['reduceAmt'],'0.00')
                self.assertEqual(repaymentDetailList[i]['deductionDetail']['coinDeductionAmt'],None)
                self.assertEqual(repaymentDetailList[i]['deductionDetail']['couponDeductionAmt'],None)
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
            #self.assertEqual(repaymentDetailList[i]['repaymentAmt'],'600.00')
            self.assertEqual(repaymentDetailList[i]['alreadyRepaymentAmt'],None)
            self.assertEqual(repaymentDetailList[i]['originalRepaymentAmt'],'600.00')
            self.assertEqual(repaymentDetailList[i]['totalAfterFee'],'100.00')
            self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['feeValue'],'100.00')
            self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['originalFeeValue'],'100.00')
            self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['realRepayAmt'],'0.00')
            #self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['reduceAmt'],'0.00')
            self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['order'],'2')
            self.assertEqual(repaymentDetailList[i]['afterFeeList'][0]['feeType'],None)
            self.assertEqual(repaymentDetailList[i]['overdueAmt'],None)
            self.assertEqual(repaymentDetailList[i]['originalOverdueAmt'],None)
            self.assertEqual(repaymentDetailList[i]['stat'],'NORMAL')
            self.assertEqual(repaymentDetailList[i]['deductionDetail']['otherReduceAmt'],None)
            #self.assertEqual(repaymentDetailList[i]['deductionDetail']['coinDeductionAmt'],None)
            #self.assertEqual(repaymentDetailList[i]['deductionDetail']['couponDeductionAmt'],None)
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
        '''【lanaPlus】/api/loan/latest/registNo获取最近一笔贷款接口-无在贷(当前非人工或自动审批通过和拒绝状态)正案例'''
        registNo=cx_registNo_03()
        headt_api=login_code(registNo)
        r=requests.get(host_api+"/api/loan/latest/"+registNo,headers=headt_api,verify=False)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(t['data']['loanStat'],'UNDER_RISK')
        self.assertIsNotNone(t['data']['loanNo'])
        self.assertIsNotNone(t['data']['custNo'])
        #self.assertIsNone(t['data']['bankAcctInfo'])
        self.assertIsNone(t['data']['paymentDetail'])
        self.assertIsNone(t['data']['trailPaymentDetail'])
        self.assertIsNone(t['data']['repaymentDetail'])
        self.assertIsNone(t['data']['reapplyDate'])
        self.assertIsNone(t['data']['certStatus'])
        self.assertIsNone(t['data']['applyButtonDetail'])
    def test_loan_latest_04(self):
        '''【lanaPlus】/api/loan/latest/registNo获取最近一笔贷款接口-无在贷(未认证)正案例'''
        registNo=cx_registNo_07()
        headt_api=login_code(registNo)
        r=requests.get(host_api+"/api/loan/latest/"+registNo,headers=headt_api,verify=False)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(t['data']['loanStat'],'NEW')
        self.assertIsNone(t['data']['loanNo'])
        self.assertIsNone(t['data']['custNo'])
        self.assertIsNone(t['data']['bankAcctInfo'])
        self.assertIsNone(t['data']['paymentDetail'])
        self.assertIsNone(t['data']['trailPaymentDetail'])
        self.assertIsNone(t['data']['repaymentDetail'])
        self.assertIsNone(t['data']['reapplyDate'])
        self.assertIsNone(t['data']['certStatus']['custNo'])
        self.assertEqual(t['data']['certStatus']['certAuth'],False)
        self.assertEqual(t['data']['certStatus']['kycAuth'],False)
        self.assertEqual(t['data']['certStatus']['workAuth'],False)
        self.assertEqual(t['data']['certStatus']['bankAuth'],False)    #目前bankauth字段无实际作用
        self.assertEqual(t['data']['certStatus']['otherContactAuth'],False)
    def test_loan_latest_05(self):
        '''【lanaPlus】/api/loan/latest/registNo获取最近一笔贷款接口-无在贷(先拿人工撤销查询，贷前有撤销，拒绝状态)正案例-重点'''
        list=cx_registNo_08()
        registNo=list[1]
        before_stat=list[0]
        headt_api=login_code(registNo)
        r=requests.get(host_api+"/api/loan/latest/"+registNo,headers=headt_api,verify=False)
        t=r.json()
        print(t)
        if before_stat=='10260007':
            stat='CANCEL'
            #self.assertTrue(t['data']['certStatus']['certAuth'])
            self.assertIsNone(t['data']['reapplyDate'])
            self.assertTrue(t['data']['certStatus']['kycAuth'])
            self.assertFalse(t['data']['certStatus']['bankAuth'])
            self.assertFalse(t['data']['certStatus']['otherContactAuth'])
        elif before_stat=='10260006':
            stat='REFUSE'
            self.assertIsNotNone(t['data']['reapplyDate'])
        else:
            print("非撤销或拒绝状态")
            stat='0'
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(stat,t['data']['loanStat'])
        self.assertIsNotNone(t['data']['loanNo'])
        self.assertIsNotNone(t['data']['custNo'])
        self.assertIsNone(t['data']['bankAcctInfo'])
        self.assertIsNone(t['data']['paymentDetail'])
        self.assertIsNone(t['data']['trailPaymentDetail'])
        self.assertIsNone(t['data']['repaymentDetail'])
        self.assertIsNone(t['data']['applyButtonDetail'])
    def test_loan_latest_06(self):
        '''【lanaPlus】/api/loan/latest/registNo获取最近一笔贷款接口-无在贷(先拿拒绝查询，贷前有撤销，拒绝状态)正案例-重点'''
        list=cx_registNo_09()
        registNo=list[1]
        before_stat=list[0]
        headt_api=login_code(registNo)
        r=requests.get(host_api+"/api/loan/latest/"+registNo,headers=headt_api,verify=False)
        t=r.json()
        print(t)
        if before_stat=='10260007':
            stat='CANCEL'
            self.assertTrue(t['data']['certStatus']['certAuth'])
            self.assertIsNone(t['data']['reapplyDate'])
            self.assertTrue(t['data']['certStatus']['kycAuth'])
            self.assertFalse(t['data']['certStatus']['bankAuth'])
            self.assertFalse(t['data']['certStatus']['otherContactAuth'])
        elif before_stat=='10260006':
            stat='REFUSE'
            self.assertIsNotNone(t['data']['reapplyDate'])
        else:
            print("非撤销或拒绝状态")
            stat='0'
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(stat,t['data']['loanStat'])
        self.assertIsNotNone(t['data']['loanNo'])
        self.assertIsNotNone(t['data']['custNo'])
        self.assertIsNone(t['data']['bankAcctInfo'])
        self.assertIsNone(t['data']['paymentDetail'])
        self.assertIsNone(t['data']['trailPaymentDetail'])
        self.assertIsNone(t['data']['repaymentDetail'])
        self.assertIsNone(t['data']['applyButtonDetail'])
    def test_loan_latest_07(self):
        '''【lanaPlus】/api/loan/latest/registNo获取最近一笔贷款接口-(提现中状态)正案例'''
        registNo=cx_under_withdraw()
        headt_api=login_code(registNo)
        r=requests.get(host_api+"/api/loan/latest/"+registNo,headers=headt_api,verify=False)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(t['data']['loanStat'],'UNDER_WITHDRAW')
        self.assertIsNotNone(t['data']['loanNo'])
        self.assertIsNotNone(t['data']['custNo'])
        self.assertIsNotNone(t['data']['bankAcctInfo'])
        self.assertIsNotNone(t['data']['paymentDetail'])
        self.assertIsNotNone(t['data']['paymentDetail']['repaymentPlanList'])
        self.assertIsNone(t['data']['trailPaymentDetail'])
        self.assertIsNone(t['data']['repaymentDetail'])
        self.assertIsNone(t['data']['reapplyDate'])
        self.assertIsNone(t['data']['applyButtonDetail'])
    def test_loan_latest_08(self):
        '''【lanaPlus】/api/loan/latest/registNo获取最近一笔贷款接口-(当前通过状态)正案例'''
        registNo=cx_tongguo()
        headt_api=login_code(registNo)
        r=requests.get(host_api+"/api/loan/latest/"+registNo,headers=headt_api,verify=False)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(t['data']['loanStat'],'TRAIL')
        self.assertIsNotNone(t['data']['loanNo'])
        self.assertIsNotNone(t['data']['custNo'])
        self.assertIsNotNone(len(t['data']['trailPaymentDetail'][0]['repaymentPlanList']))
        self.assertIsNone(t['data']['paymentDetail'])
        self.assertEqual(str(t['data']['trailPaymentDetail'][0]['loanAmt']),"1500.00")
        self.assertEqual(str(t['data']['trailPaymentDetail'][0]['prodNo']),"28070110")
        self.assertFalse(t['data']['trailPaymentDetail'][0]['showLoanDay'])
        self.assertEqual(str(t['data']['trailPaymentDetail'][0]['instNum']),"3")
        self.assertEqual(str(t['data']['trailPaymentDetail'][0]['paymentAmt']),"1500.00")
        self.assertEqual(str(t['data']['trailPaymentDetail'][0]['repaymentAmt']),"1800.00")
        self.assertEqual(str(t['data']['trailPaymentDetail'][0]['loanDays']),"21")
        self.assertEqual(str(t['data']['trailPaymentDetail'][0]['feeList']),"[{'feeName': 'lixi', 'feeValue': '300', 'originalFeeValue': None, 'realRepayAmt': None, 'reduceAmt': None, 'order': '2', 'feeType': 'AFTER'}]")
        self.assertIsNone(t['data']['repaymentDetail'])
        self.assertIsNone(t['data']['reapplyDate'])
        self.assertIsNone(t['data']['applyButtonDetail'])
        self.assertIsNone(t['data']['showWithSucessPage'])
    def test_loan_latest_09(self):
        '''【lanaPlus】/api/loan/latest/registNo获取最近一笔贷款接口-无在贷(先拿自动撤销查询，贷前有撤销，拒绝状态)正案例-重点'''
        list=cx_registNo_081()
        registNo=list[1]
        before_stat=list[0]
        headt_api=login_code(registNo)
        r=requests.get(host_api+"/api/loan/latest/"+registNo,headers=headt_api,verify=False)
        t=r.json()
        print(t)
        if before_stat=='10260007':
            stat='NEW'
            #self.assertTrue(t['data']['certStatus']['certAuth'])
            self.assertIsNone(t['data']['reapplyDate'])
            self.assertTrue(t['data']['certStatus']['kycAuth'])
            self.assertFalse(t['data']['certStatus']['bankAuth'])
            self.assertFalse(t['data']['certStatus']['otherContactAuth'])
            self.assertEqual(t['data']['applyButtonDetail'],{'buttonName': '234', 'desc': '234'})
        elif before_stat=='10260006':
            stat='REFUSE'
            self.assertIsNotNone(t['data']['reapplyDate'])
        else:
            print("非撤销或拒绝状态")
            stat='0'
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(stat,t['data']['loanStat'])
        self.assertIsNotNone(t['data']['loanNo'])
        self.assertIsNotNone(t['data']['custNo'])
        self.assertIsNone(t['data']['bankAcctInfo'])
        self.assertIsNone(t['data']['paymentDetail'])
        self.assertIsNone(t['data']['trailPaymentDetail'])
        self.assertIsNone(t['data']['repaymentDetail'])
    def test_fin_repay_stp(self):
        '''【lanaPlus】/api/trade/fin/repay-STP申请还款接口-有在贷(正常)-正案例'''
        registNo=cx_registNo_04()
        print(registNo)
        phone=registNo[0]
        custNo=registNo[1]
        loanNo=registNo[2]
        headt_api=login_code(phone)
        list=cx_inst_num(loanNo)
        data={"advance":"10000000","custNo":custNo,"defer":False,"loanNo":loanNo,"paymentMethod":"STP","repayInstNumList":list,"tranAppType":"Android"}
        r=requests.post(host_api+"/api/trade/fin/repay",data=json.dumps(data),headers=headt_api,verify=False)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(t['data']['code'],10000)
        self.assertEqual(t['data']['msg'],'apply success')
        self.assertEqual(t['data']['settle'],False)
        self.assertEqual(t['data']['paymentMethod'],'STP')
        self.assertEqual(t['data']['stpRepayment']['nombre'],'LANAPLUS')
        self.assertEqual(t['data']['stpRepayment']['tipoDeCuenta'],'CLABE')
        self.assertEqual(t['data']['stpRepayment']['destinatario'],'STP')
        self.assertEqual(t['data']['stpRepayment']['concepto'],phone)
        self.assertIsNone(t['data']['conektaRepayment'])
    def test_fin_repay_oxxo(self):
        '''【lanaPlus】/api/trade/fin/repay-OXXO申请还款接口-有在贷-正案例'''
        registNo=cx_registNo_04()
        #print(registNo)
        phone=registNo[0]
        custNo=registNo[1]
        loanNo=registNo[2]
        headt_api=login_code(phone)
        list=cx_inst_num(loanNo)
        data={"advance":"10000000","custNo":custNo,"defer":False,"loanNo":loanNo,"paymentMethod":"CONEKTA","repayInstNumList":list,"tranAppType":"Android"}
        r=requests.post(host_api+"/api/trade/fin/repay",data=json.dumps(data),headers=headt_api,verify=False)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(t['data']['code'],10000)
        self.assertEqual(t['data']['msg'],'apply success')
        self.assertEqual(t['data']['settle'],False)
        self.assertEqual(t['data']['paymentMethod'],'CONEKTA')
        self.assertIsNone(t['data']['stpRepayment'])
        self.assertEqual(t['data']['conektaRepayment']['concepto'],phone)
    def test_stp_repayment(self):
        '''【lanaPlus】/api/trade/stp_repayment/annon/event/webhook-还款接口-STP模拟银行回调-有在贷（逾期）验证结清-正案例'''
        registNo=cx_registNo_05()
        print(registNo)
        phone=registNo[0]
        cuentaBeneficiario=registNo[1]
        headt_api=login_code(phone)
        r=requests.get(host_api+"/api/loan/latest/"+phone,headers=headt_api,verify=False)
        t=r.json()
        print('获取最近一笔贷款接口返回值=',t)
        self.assertEqual('REPAYMENT',t['data']['loanStat'])
        repaymentDetailList=t['data']['repaymentDetail']['repaymentDetailList']
        sum=0
        for i in range(len(repaymentDetailList)):
            #print(repaymentDetailList[i])
            if repaymentDetailList[i]['stat']=='SETTLE_MENT':       #该期已结清
                pass
            else:
                sum=sum+float(repaymentDetailList[i]['repaymentAmt'])
        print('总待还金额=',sum)
        monto=str(sum)
        loanNo=t['data']['loanNo']
        data={"abono":{"id":"37755992","fechaOperacion":"20210108","institucionOrdenante":"40012","institucionBeneficiaria":"90646","claveRastreo":"MBAN01002101080089875109","monto":monto,
                   "nombreOrdenante":"HAZEL VIRIDIANA RUIZ RICO               ","tipoCuentaOrdenante":"40","cuentaOrdenante":"012420028362208190","rfcCurpOrdenante":"RURH8407075F8","nombreBeneficiario":"STP                                     ",
                   "tipoCuentaBeneficiario":"40","cuentaBeneficiario":cuentaBeneficiario,"rfcCurpBeneficiario":"null","conceptoPago":"ESTELA SOLICITO TRANSFERENCIA","referenciaNumerica":"701210","empresa":"QUANTX_TECH"}}
        r=requests.post(host_pay+"/api/trade/stp_repayment/annon/event/webhook",data=json.dumps(data),headers=head_pay,verify=False)
        t=r.json()
        self.assertEqual(t['errorCode'],0)
        afterstat=cx_beforeStat_afterStat(loanNo)
        self.assertEqual('10270005',afterstat[1])  #验证贷后状态是否更新为【已结清】
    def test_oxxo_repayment(self):
        '''【lanaPlus】/api/trade/conekta/annon/event/webhook-还款接口-OXXO模拟银行回调-有在贷（正常）,结清(先申请还款后模拟还款回调)-正案例'''
        registNo=cx_registNo_04()
        print(registNo)
        phone=registNo[0]
        custNo=registNo[1]
        loanNo=registNo[2]
        headt_api=login_code(phone)
        list=cx_inst_num(loanNo)
        data={"advance":"10000000","custNo":custNo,"defer":False,"loanNo":loanNo,"paymentMethod":"CONEKTA","repayInstNumList":list,"tranAppType":"Android"}
        r=requests.post(host_api+"/api/trade/fin/repay",data=json.dumps(data),headers=headt_api,verify=False)
        t=r.json()
        print("OXXO申请还款接口响应=",t)
        self.assertEqual(t['errorCode'],0)
        r=requests.get(host_api+"/api/loan/latest/"+phone,headers=headt_api,verify=False)
        t=r.json()
        print('获取最近一笔贷款接口响应值=',t)
        repaymentDetailList=t['data']['repaymentDetail']['repaymentDetailList']
        amount=0
        for i in range(len(repaymentDetailList)):
            #print(repaymentDetailList[i])  #每期费用列表
            if repaymentDetailList[i]['stat']=='SETTLE_MENT':       #该期已结清
                pass
            else:
                amount=amount+float(repaymentDetailList[i]['repaymentAmt'])
        print('总待还金额=',amount)
        list=cx_registNo_06(loanNo)
        tran_order_no=list[1]
        in_acct_no=list[2]
        data_for_oxxo={"data": {"object": {
			"livemode": False,
			"amount": int(amount*100),
			"currency": "",
			"payment_status": "paid",
			"amount_refunded": 0,
			"customer_info": {"email": "","phone": "","name": "","object": ""},"object": "",
			"id": tran_order_no,
			"metadata": {},
			"created_at": 0,
			"updated_at": 0,
			"line_items": {
				"object": "",
				"has_more": False,
				"total": 0,
				"data": [
					{"name": "",
						"unit_price": 0,
						"quantity": 0,
						"object": "",
						"id": "",
						"parent_id": "",
						"metadata": {},
						"antifraud_info": {}
					}]},
			"charges": {"object": "",
				"has_more": False,
				"total": 0,
				"data": [
					{
						"id": "",
						"livemode": False,
						"created_at": 0,
						"currency": "",
						"payment_method": {
							"service_name": "OxxoPay",
							"barcode_url": "https://s3.amazonaws.com/cash_payment_barcodes/84000964785462.png",
							"object": "",
							"type": "",
							"expires_at": 0,
							"store_name": "OXXO",
							"reference": in_acct_no
						},
						"object": "",
						"description": "",
						"status": "",
						"amount": 0,
						"paid_at": 0,
						"fee": 0,
						"customer_id": "",
						"order_id": ""
					}
				]
			}
		},
                "previous_attributes": {}
            },
            "livemode": False,
            "webhook_status": "",
            "id": "",
            "object": "",
            "type": "order.paid",
            "created_at": 0,
            "webhook_logs": [
                {
                    "id": "",
                    "url": "",
                    "failed_attempts": 0,
                    "last_http_response_status": 0,
                    "object": "",
                    "last_attempted_at": 0
                }
            ]
        }
        #print(data_for_oxxo)
        r=requests.post(host_pay+"/api/trade/conekta/annon/event/webhook",data=json.dumps(data_for_oxxo),verify=False)
        print(r.json())
        self.assertEqual(r.status_code,200)
        afterstat=cx_beforeStat_afterStat(loanNo)
        self.assertEqual('10270005',afterstat[1])  #验证贷后状态是否更新为【已结清】
    def test_get_deduction_details(self):
        '''【lanaPlus】/api/cust/repayment/deduction-查询lanacoin列表接口-正案例'''
        list=cx_registNo_11()
        print(list)
        registNo=list[0]
        headt_api=login_code(registNo)
        r=requests.get(host_api+"/api/cust/coin/deduction/details/"+registNo,headers=headt_api,verify=False)
        t=r.json()
        print(t)
        self.assertEqual(t['errorCode'],0)
        #self.assertEqual(str(len(t['data']['details'])),t['data']['totalCoins'][:2])
    def test_repayment_deduction_coin(self):
        '''【lanaPlus】/api/cust/repayment/deduction-减免接口-lanacoin减免成功-正案例'''
        registNo=cx_registNo_12()
        headt_api=login_code(registNo)
        r=requests.get(host_api+"/api/loan/latest/"+registNo,headers=headt_api,verify=False)
        t=r.json()
        print(t)
        loanNo=t['data']['loanNo']
        self.assertEqual(t['errorCode'],0)
        repaymentDetailList=t['data']['repaymentDetail']['repaymentDetailList']
        for i in range(len(repaymentDetailList)):
            #print(repaymentDetailList[i]['deductionDetail'])
            if repaymentDetailList[i]['deductionDetail']['coinDeductionAble'] is True:
                #print(repaymentDetailList[i])
                repayDate=repaymentDetailList[i]['repayDate']
            else:
                pass
        r=requests.get(host_api+"/api/cust/coin/deduction/details/"+registNo,headers=headt_api,verify=False)
        t=r.json()
        print(t)
        x=t['data']['details'][0]
        print(x)
        data={"coinDeductionDetail":x,"couponDeductionDetail":None,"deductionType":"COIN","loanNo":loanNo,"repayDate":repayDate}
        r=requests.post(host_api+'/api/cust/repayment/deduction',data=json.dumps(data),headers=headt_api,verify=False)
        s=r.json()
        print(s)
        self.assertEqual(s['errorCode'],0)
    def test_repayment_deduction_coupon(self):
        '''【lanaPlus】/api/cust/repayment/deduction-减免接口-coupon减免成功-正案例'''
        registNo=cx_registNo_13()
        headt_api=login_code(registNo)
        r=requests.get(host_api+"/api/loan/latest/"+registNo,headers=headt_api,verify=False)
        t=r.json()
        print(t)
        loanNo=t['data']['loanNo']
        self.assertEqual(t['errorCode'],0)
        repaymentDetailList=t['data']['repaymentDetail']['repaymentDetailList']
        for i in range(len(repaymentDetailList)):
            #print(repaymentDetailList[i]['deductionDetail'])
            if repaymentDetailList[i]['deductionDetail']['couponDeductionAble'] is True:
                #print(repaymentDetailList[i])
                repayDate=repaymentDetailList[i]['repayDate']
            else:
                pass
        r=requests.get(host_api+"/api/cust/coupon/type/details/"+registNo+"?stat=USABLE",headers=headt_api,verify=False)
        t=r.json()
        print(t)
        data={"coinDeductionDetail":None,"couponDeductionDetail":{"couponChannelNo":"test-满3减3","couponNo":"减3块"},"deductionType":"COUPON","loanNo":loanNo,"repayDate":repayDate}
        r=requests.post(host_api+'/api/cust/repayment/deduction',data=json.dumps(data),headers=headt_api,verify=False)
        s=r.json()
        print(s)
        self.assertEqual(s['errorCode'],0)
    def test_repay_methods(self):
        '''【lanaPlus】/api/trade/fin/repay/methods/loan_no-获取贷款支持的还款方式接口（stp+oxxo）-正案例'''
        registNo=cx_registNo_04()
        phone=registNo[0]
        loanNo=registNo[2]
        headt_api=login_code(phone)
        r=requests.post(host_api+"/api/trade/fin/repay/methods/"+loanNo,headers=headt_api,verify=False)
        t=r.json()
        self.assertEqual(t['errorCode'],0)
        self.assertEqual(t['data'],{"stp":{"paymentMethod":"STP","free":True,"recommended":True,"serviceCharge":"0","supportTime":"24/7"},"oxxo":{"paymentMethod":"CONEKTA","free":False,"recommended":False,"serviceCharge":"12.00","supportTime":"24/7"}})
    @classmethod
    def tearDownClass(cls): #在所有用例都执行完之后运行的
        DataBase(which_db).closeDB()
        print('我是tearDownClass，我位于多有用例运行的结束')