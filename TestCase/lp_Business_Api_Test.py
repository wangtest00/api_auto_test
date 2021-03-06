import json
import unittest
import requests
from dataBase.dataBase import *
from data.var_lp import *

class LP_Business_Api_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  #在所有用例执行之前运行的
        print('我是setUpclass，我位于所有用例的开始')
    def setUp(self):  #每个用例运行之前运行的
        print('setup_test')
    def tearDown(self): #每个用例运行之后运行的
        print('teardown_test')
    def test_handle_closed(self):
        '''【lanaPlus】-还款结清后，支付调通知出催接口-正案例'''     #处理最大数据量500    补偿次数（小于等于50）0也是默认补5次
        r=requests.post(host_pay+"/api/common/anon/handle/closed?count=500&maxNumber=50",headers=head_pay,verify=False)
        t=r.json()
        self.assertEqual(t['errorCode'],0)
    def test_task_case_handlingOverdue(self):
        '''【lanaPlus】-催收自动毁约定时任务接口（先承诺了还款时间，过期后则会更改标签为“毁约”）-正案例'''
        r=requests.post(host_coll+"/api/insecure/task/case/handlingOverdue",verify=False)
        t=r.json()
        self.assertEqual(t['errorCode'],0)
    def test_payout_retry(self):
        '''【lanaPlus】-支付申请放款重试接口（进入重试表的数据才会去发起重试申请且不会重复）-正案例'''
        r=requests.post(host_pay+"/api/trade/retry/payout_retry",verify=False)
        t=r.json()
        self.assertEqual(t['errorCode'],0)
    def test_payment_retry(self):
        '''【lanaPlus】-支付还款重试接口（pay_stp_repayment_record和pay_conekta_record表的数据状态为0且未做过清结算的数据）-正案例'''
        r=requests.post(host_pay+"/api/trade/retry/payment_retry",verify=False)
        t=r.json()
        self.assertEqual(t['errorCode'],0)
    def test_third_batch_send_test(self):
        '''【lanaPlus】-msg发送短信接口(指定手机号+模板+携带deeplink)-正案例'''
        data={"channelNo": "Mex-LanaPlus",
              "templateNo": "LP-CRT-0011",
              "messageData": [
                    {
                        "phone": "9383893927",
                        "language": "90000002",
                        "requestParams": {
                            "link": "t.liy.mx/o8tuH1"
                        }
                    }
                ]
            }
        r=requests.post(host_msg+"/api/interface/third/batch/send/test",data=json.dumps(data),headers=head_msg,verify=False)
        t=r.json()
        self.assertEqual(t['errorCode'],0)
    def test_coupon_event_dispatch(self):
        '''【lanaPlus】-api扫描是否达到发放优惠券节点接口-正案例'''
        r=requests.post(host_api+"/api/cust/coupon/event/dispatch",verify=False)
        t=r.json()
        self.assertEqual(t['errorCode'],0)
    def test_coupon_stat_check(self):
        '''【lanaPlus】-api过期优惠券状态处理接口（根据优惠券结束时间来判断是否失效）-正案例'''
        r=requests.post(host_api+"/api/cust/coupon/stat/check",verify=False)
        t=r.json()
        self.assertEqual(t['errorCode'],0)
    def test_email_send_third(self):
        '''【lanaPlus】-msg发送邮件接口-正案例'''
        data={"appNo":"201",
               "templateNo": "test_templateNo",
               "subject": "test_subject",
               "type": 1,
               "param": {
                   "userName": "王先生"
               },
               "toList": ["370558913@qq.com"],
               "ccList": [""]}
        r=requests.post(host_msg+"/api/email/send/third",data=json.dumps(data),headers=head_msg,verify=False)
        t=r.json()
        self.assertEqual(t['errorCode'],0)
    def test_repayment_callback(self):
        '''【lanaPlus】-催收通知结案接口（案件移入结案管理列表）-正案例'''
        data={
    "loanNo": "L2012106098091147837788430336",
    "channelNo": "C9123001",
    "repayDateList": [
        {
            "repayDate": "20210612",
            "afterStat": "10270005"
        }
    ]
}
        r=requests.post(host_coll+"/api/insecure/repayment/callback",data=json.dumps(data),headers=head_coll,verify=False)
        t=r.json()
        self.assertEqual(t['errorCode'],0)
    @classmethod
    def tearDownClass(cls): #在所有用例都执行完之后运行的
        DataBase(which_db).closeDB()
        print('我是tearDownClass，我位于多有用例运行的结束')