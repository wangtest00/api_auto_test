from api_auto_test.public.daihou import *
from api_auto_test.public.heads import *

randnum=str(random.randint(10000000,99999999))
#插入允许展期的记录
def inst_lo_extension_log(loan_no,cust_no):
    inst_time=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    sql='''INSERT INTO `mex_pdl_loan`.`lo_extension_log`(`ID`, `LOAN_NO`, `CUST_NO`, `OPER_TYPE`, `OPER_NAME`, `OPER_TIME`, `REMARK`, `INST_TIME`) VALUES
    ('bfd576b0fb2d11ebb44'''+randnum+'''', "'''+loan_no+'''", "'''+cust_no+'''", 'STAFF', 'wangshuang', "'''+inst_time+'''", NULL, "'''+inst_time+'''");'''
    DataBase(which_db).executeUpdateSql(sql)

def zhanqi(cust_no):
    r1=requests.get(host_api+"/api/h5/anon/id/"+cust_no,verify=False)
    t1=r1.json()
    print("t1=",t1)
    data=t1['data']
    data2={"customerId": data}
    r2=requests.post(host_api+"/api/h5/login/"+data,data=json.dumps(data2),headers=head_api,verify=False)
    t2=r2.json()
    print("t2=",t2)
    loanNo=t2['data']['loanNo']
    token=t2['data']['token']
    phone=t2['data']['phone']
    headt=head_zhanqi(token)
    #最近一笔贷款接口h5
    r3=requests.get(host_api+"/api/h5/latest/"+phone,headers=headt,verify=False)
    t3=r3.json()
    print("t3=",t3)
    currentRepayDate=t3['data']['loanInfoData']['loanDateInfo']['currentRepayDate']
    rollOverAmt=t3['data']['rollOverDetails']['rollOverAmt']
    data4={"advance": "10000000",
          "custNo": cust_no,
          "defer": True,
          "loanNo": loanNo,
          "paymentMethod": "STP",
          "repayDate": currentRepayDate,
          "repayInstNum": 1,
          "tranAppType": "Android",
          "transAmt": rollOverAmt}
    #发起展期申请
    r4=requests.post(host_api+"/api/h5/repay",data=json.dumps(data4),headers=headt,verify=False)
    t4=r4.json()
    print("t4=",t4)
    m=[]
    m.append(t4['data']['stpRepayment']['clabeNo'])
    m.append(t4['data']['stpRepayment']['transAmt'])
    print(m)
    return m

def cx_for_zhanqi():
    sql=''' #查询实收表只有一笔内部账户收款的记录，无外部账户收款记录
    SELECT a.loan_no,a.CUST_NO FROM
            lo_loan_dtl a
            LEFT JOIN lo_loan_prod_rel b ON a.LOAN_NO = b.LOAN_NO
            LEFT JOIN fin_rd_dtl c ON a.LOAN_NO = c.LOAN_NO
             WHERE
                a.AFTER_STAT = '10270002'
              and  b.APP_NO = '201'
               AND b.PROD_NO = '25002400'
               AND c.TRANSTER_TYPE = '10440001'
            GROUP BY  a.LOAN_NO
            HAVING count(c.LOAN_NO) = 1
            order by c.INST_TIME desc limit 1;'''
    cust_no=DataBase(which_db).get_one(sql)
    print(cust_no)
    return cust_no

def test_for_zhanqi():
    cust_no=cx_for_zhanqi()
    inst_lo_extension_log(cust_no[0],cust_no[1])
    return cust_no

def new_loanNo(old_loanNo):
    if len(old_loanNo)==32:   #原始已带后缀
        x=str(int(old_loanNo[-2:])+1)
        if len(x)==1:  #后缀位数=1
            x=old_loanNo[:30]+"0"+x
            return x
        else:
            x=old_loanNo[:30]+x
            return x
    else: #原始未带后缀，则加上01后缀
        x=old_loanNo+"_01"
        return x


if __name__ == '__main__':
    #test_zhanqi()
    #check_zhanqi("L2012112168159712308449443840")
    new_loanNo("L2012112168159712308449443840_02")