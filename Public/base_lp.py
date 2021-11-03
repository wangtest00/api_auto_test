import requests,json
from api_auto_test.public.dataBase import *
from api_auto_test.public.var_lp import *
from api_auto_test.public.check_api import *
import random,string,datetime
#短信验证码，默认手机号后4位单个+5后取个位数，在逆序排列。注意非中国手机号规则.现在实际规则改为手机号后6位。。。没区别
def compute_code(m):
    m=m[-4:]
    x1=str(int(m[0])+5)
    x2=str(int(m[1])+5)
    x3=str(int(m[2])+5)
    x4=str(int(m[3])+5)
    x=x4[-1:]+x3[-1:]+x2[-1:]+x1[-1:]
    return x
#查询客户号不为空的用户手机号，GAID='Exception:null'我的标记数据
def cx_old_registNo():
    sql="select REGIST_NO from cu_cust_reg_dtl where GAID='Exception:null' and CUST_NO is not null and app_no='"+appNo+"';"
    registNo=DataBase(which_db).get_one(sql)
    registNo=registNo[0]
    return registNo

def cx_registNo():
    sql='''#查询贷后状态为正常的贷款用户手机号，产品号写死，实收表数据为空（未还过款）
          select REGIST_NO from lo_loan_dtl a left join lo_loan_prod_rel b   on a.LOAN_NO=b.LOAN_NO left join fin_rd_dtl c on a.LOAN_NO=c.LOAN_NO
          left join cu_cust_reg_dtl d on a.CUST_NO=d.CUST_NO
          where a.AFTER_STAT='10270002' and b.APP_NO="'''+appNo+'''" and b.PROD_NO='28070110' and c.TRAN_TIME is NULL order by a.INST_TIME desc limit 1;'''
    registNo=DataBase(which_db).get_one(sql)
    registNo=str(registNo[0])
    #print(registNo)
    return registNo

def cx_registNo_02():
    sql='''#查询只借过一笔款且已结清的手机号
select  c.REGIST_NO ,count(1) as loan_cnt from
(select  a.cust_no from lo_loan_dtl a
WHERE a.BEFORE_STAT = '10260005' AND a.AFTER_STAT = '10270005'
GROUP BY a.cust_no
HAVING count(1) =1
)a INNER JOIN lo_loan_dtl b on a.cust_no=b.cust_no left join cu_cust_reg_dtl c on b.CUST_NO=c.CUST_NO where c.APP_NO="'''+appNo+'''"
group by  b.cust_no
HAVING loan_cnt=1  order by c.INST_TIME desc limit 1;'''
    phone=DataBase(which_db).get_one(sql)
    phone=str(phone[0])
    return phone

def cx_registNo_03():
    sql='''#查询手机号，不在人工或自动审批通过，拒绝状态，201，非空,非撤销状态
select c.REGIST_NO from apr_appr_flow_dtl a left join lo_loan_dtl b on a.loan_no=b.LOAN_NO left join cu_cust_reg_dtl c on b.CUST_NO=c.CUST_NO
where a.APPR_TYPE='10290002' and a.APPR_STAT not in('10200001','10200002','10200005','10200006','10200009') and a.APPR_NO='201001' and c.REGIST_NO is not null
order by a.INST_TIME desc limit 1;'''
    phone=DataBase(which_db).get_one(sql)
    phone=str(phone[0])
    return phone
def cx_registNo_04():
    sql='''#查询手机号c.REGIST_NO,c.CUST_NO,a.LOAN_NO,a.INST_NUM，有在贷未结清
    select c.REGIST_NO,c.CUST_NO,a.LOAN_NO,a.INST_NUM from lo_loan_dtl a  left join lo_loan_prod_rel b on a.LOAN_NO=b.LOAN_NO left join cu_cust_reg_dtl c on a.CUST_NO=c.CUST_NO
where a.BEFORE_STAT='10260005' and b.APP_NO='201' and c.app_no='201' and a.AFTER_STAT='10270002' or a.AFTER_STAT='10270003'  order by a.INST_TIME desc limit 1;
'''
    phone=DataBase(which_db).get_one(sql)
    return phone

def cx_registNo_05():
    sql='''#查询有还款申请记录，逾期状态的贷款，手机号和还款入账账号
select DISTINCT c.REGIST_NO,d.IN_ACCT_NO from pay_tran_dtl d left join lo_loan_dtl a  on d.loan_no=a.loan_no
left join lo_loan_prod_rel b on a.LOAN_NO=b.LOAN_NO left join cu_cust_reg_dtl c on a.CUST_NO=c.CUST_NO
where d.TRAN_CHAN_NAME='STP支付渠道' and d.tran_use='10330002'  and b.APP_NO='201' and a.AFTER_STAT='10270003' and a.BEFORE_STAT='10260005'
order by a.INST_TIME desc limit 1;  '''
    phone=DataBase(which_db).get_one(sql)
    return phone
def cx_registNo_06(loanNo):
    sql='''#查询OXXO还款申请记录
select SHD_TRAN_AMT,tran_order_no,in_acct_no,INST_TIME from pay_tran_dtl t where LOAN_NO="'''+loanNo+'''" and  ACT_TRAN_AMT is null and TRAN_CHAN_NAME !='STP支付渠道' order by INST_TIME desc limit 1;'''
    phone=DataBase(which_db).get_one(sql)
    #print(phone)
    return phone
def cx_registNo_07():
    sql='''#查询无客户号的手机号
select a.REGIST_NO from cu_cust_reg_dtl a where a.GAID='Exception:null' and a.CUST_NO is null and a.APP_NO='201'
order by a.INST_TIME desc limit 1; '''
    phone=DataBase(which_db).get_one(sql)
    phone=str(phone[0])
    return phone

def cx_registNo_08():
    sql='''#查询手机号，同一个手机号可能有贷款在拒绝，撤销等多种状态
select c.BEFORE_STAT,d.REGIST_NO from lo_loan_dtl c left join cu_cust_reg_dtl d on c.cust_no=d.cust_no where c.cust_no=(select b.CUST_NO from lo_loan_dtl a left join cu_cust_reg_dtl b on a.CUST_NO=b.CUST_NO
where  a.BEFORE_STAT='10260007' and a.AFTER_STAT is null and b.APP_NO='201'
order by a.INST_TIME desc limit 1) order by c.inst_time desc limit 1; '''
    phone=DataBase(which_db).get_one(sql)
    phone=list(phone)   #元祖转列表
    return phone
def cx_registNo_09():
    sql='''#查询手机号，同一个手机号可能有贷款在拒绝，撤销等多种状态
select c.BEFORE_STAT,d.REGIST_NO from lo_loan_dtl c left join cu_cust_reg_dtl d on c.cust_no=d.cust_no where c.cust_no=(select b.CUST_NO from lo_loan_dtl a left join cu_cust_reg_dtl b on a.CUST_NO=b.CUST_NO
where  a.BEFORE_STAT='10260006' and a.AFTER_STAT is null and b.APP_NO='201'
order by a.INST_TIME desc limit 1) order by c.inst_time desc limit 1; '''
    phone=DataBase(which_db).get_one(sql)
    phone=list(phone)   #元祖转列表
    return phone
def cx_registNo_10():
    sql='''#查询有客户号的手机号
select a.REGIST_NO from cu_cust_reg_dtl a where a.GAID='Exception:null' and a.CUST_NO is not null and a.APP_NO='201'
order by a.INST_TIME desc limit 1; '''
    phone=DataBase(which_db).get_one(sql)
    phone=str(phone[0])
    return phone
def cx_registNo_11():
    sql='''#查询获取lanacoin大于1000且正常的手机号
select PHONE_NO,OBTAIN_VALUE from cu_cust_coin_dtl where OBTAIN_VALUE>1000 and stat='11360001' order by INST_TIME desc limit 1;'''
    phone=DataBase(which_db).get_one(sql)
    phone=list(phone)
    return phone
def cx_registNo_12():
    sql='''#查询手机号：在贷，有lanacoin，且无减免记录，无实收
    select d.REGIST_NO from lo_loan_dtl a left join lo_loan_prod_rel b   on a.LOAN_NO=b.LOAN_NO left join fin_rd_dtl c on a.LOAN_NO=c.LOAN_NO
    left join cu_cust_reg_dtl d on a.CUST_NO=d.CUST_NO left join fin_fee_reduce_dtl e on a.LOAN_NO=e.loan_no left join cu_cust_coin_dtl f on d.REGIST_NO=f.PHONE_NO
    where a.AFTER_STAT='10270002' and b.APP_NO="201" and b.PROD_NO='28070110' and c.TRAN_TIME is NULL and e.loan_no is null and f.OBTAIN_VALUE>1000 and f.stat='11360001' order by a.INST_TIME desc limit 1;'''
    phone=DataBase(which_db).get_one(sql)
    phone=phone[0]
    return phone
def cx_registNo_13():
    sql='''#查询手机号：在贷，有coupon，且无减免记录，无实收
    select d.REGIST_NO from lo_loan_dtl a left join lo_loan_prod_rel b   on a.LOAN_NO=b.LOAN_NO left join fin_rd_dtl c on a.LOAN_NO=c.LOAN_NO
    left join cu_cust_reg_dtl d on a.CUST_NO=d.CUST_NO left join fin_fee_reduce_dtl e on a.LOAN_NO=e.loan_no left join cu_coupon_dtl f on d.REGIST_NO=f.PHONE_NO
    where a.AFTER_STAT='10270002' and b.APP_NO="201" and b.PROD_NO='28070110' and c.TRAN_TIME is NULL and e.loan_no is null and f.COUPON_NO='减3块' and f.USE_TIME is null  and f.STATUS='11320001' order by a.INST_TIME desc limit 1;'''
    phone=DataBase(which_db).get_one(sql)
    phone=phone[0]
    print(phone)
    return phone
cx_registNo_13()
def get_yijieqing_custNo():
    sql='''select  b.cust_no,count(1) as loan_cnt from
(select  a.cust_no from
lo_loan_dtl a
WHERE
	a.BEFORE_STAT = '10260005'
AND a.AFTER_STAT = '10270005'
GROUP BY a.cust_no
HAVING count(1) =1
)a INNER JOIN lo_loan_dtl b on a.cust_no=b.cust_no
group by  b.cust_no
HAVING loan_cnt=1;'''
    custNo=DataBase(which_db).get_one(sql)
    return custNo[0]
def cx_beforeStat_afterStat(loanNo):
    sql='''select BEFORE_STAT,AFTER_STAT from lo_loan_dtl where LOAN_NO="'''+loanNo+'''";'''
    stat=DataBase(which_db).get_one(sql)
    return stat
def cx_under_withdraw():
    sql='''select b.REGIST_NO from lo_loan_dtl a left join cu_cust_reg_dtl b on a.CUST_NO=b.CUST_NO
where a.BEFORE_STAT='10260008' and a.AFTER_STAT is null and b.APP_NO='201' order by a.INST_TIME desc limit 1; '''
    registNo=DataBase(which_db).get_one(sql)
    registNo=registNo[0]
    return registNo
def cx_inst_num(loanNo):
    sql='''select INST_NUM from lo_loan_plan_dtl where loan_no="'''+loanNo+'''" and REPAY_STAT!='10270005' order by INST_NUM asc;'''
    inst_num=DataBase(which_db).get_all(sql)
    list=[]
    for i in range(len(inst_num)):
        list.append(str(inst_num[i][0]))
    return list
#更新登录密码，包含了用验证码方式注册登录的步骤
def update_pwd(registNo):
    token=login_code(registNo)
    headt=head_token(token)
    data={"registNo":registNo,"newPwd":"123456"}
    r=requests.post(host_api+"/api/cust/pwd/update",data=json.dumps(data),headers=headt,verify=False)
    check_api(r)
def random_four_zm():
    st=''
    for j in range(4):  #生成4个随机英文大写字母
        st+=random.choice(string.ascii_uppercase)
    return st
#通过密码登录，返回token
def login_pwd(registNo):
    data={"registNo":registNo,"password":"123456","gaid":"Exception:null"}
    r=requests.post(host_api+"/api/cust/pwd/login",data=json.dumps(data),headers=head_api,verify=False)
    t=r.json()
    token=t['data']['token']
    return token
def headtt(registNo):
    token=login_pwd(registNo)
    headtt=head_token(token)
    return headtt

def for_test_auth_other():
    st=random_four_zm()
    registNo=str(random.randint(8000000000,9999999999)) #10位随机数作为手机号
    code=compute_code(registNo)
    data={"registNo":registNo,"code":code,"gaid":"Exception:null"}
    r=requests.post(host_api+"/api/cust/login",data=json.dumps(data),headers=head_api,verify=False)
    t=r.json()
    token=t['data']['token']
    head=head_token(token)
    data0={"birthdate":"1999-5-18","civilStatus":"10050001","curp":st+"990518MM"+st+"V8","delegationOrMunicipality":"zxcvbbbccxxx","education":"10190005","fatherLastName":"WANG","gender":"10030001",
          "motherLastName":"TEST","name":"SHUANG","outdoorNumber":"qweetyyu","phoneNo":registNo,"postalCode":"55555","state":"11130001","street":"444444","suburb":"asdfhhj","email":""}
    r=requests.post(host_api+'/api/cust/auth/cert',data=json.dumps(data0),headers=head)
    s=r.json()
    custNo=s['data']['custNo']
    list=[]
    list.append(registNo)
    list.append(custNo)
    list.append(head)
    return list
def login_code(registNo):
    code=compute_code(registNo)
    data={"registNo":registNo,"code":code,"gaid":"Exception:null"}
    r=requests.post(host_api+"/api/cust/login",data=json.dumps(data),headers=head_api,verify=False)
    t=r.json()
    token=t['data']['token']
    head=head_token(token)
    return head
def login_code_f(registNo):
    code=compute_code(registNo)
    data={"registNo":registNo,"code":code,"gaid":"Exception:null"}
    r=requests.post(host_api+"/api/cust/login",data=json.dumps(data),headers=head_api,verify=False)
    t=r.json()
    token=t['data']['token']
    head=head_token_f(token)
    return head
def for_apply_loan():
    test_data=for_test_auth_other()
    custNo=test_data[1]
    registNo=test_data[0]
    head=test_data[2]
    data1={"certType":"WORK","custNo":custNo}
    r1=requests.post(host_api+'/api/cust/auth/review',data=json.dumps(data1),headers=head)
    data2={"companyAddress":"","companyName":"","companyPhone":"","custNo":custNo,"income":"10870004","industry":"","jobType":"10130006"}#工作收入来源
    r2=requests.post(host_api+'/api/cust/auth/work',data=json.dumps(data2),headers=head)
    data3={"certType":"CONTACT","custNo":custNo}
    r3=requests.post(host_api+'/api/cust/auth/review',data=json.dumps(data3),headers=head)
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
        time.sleep(1)
    #联系人的联系方式
    data9={"contacts":[{"name":"test","phone":"8888455666","relationship":"10110004"},{"name":"test2","phone":"8883355777","relationship":"10110003"}],"custNo":custNo}
    r9=requests.post(host_api+'/api/cust/auth/other/contact',data=json.dumps(data9),headers=head)#最后一步，填写2个联系人的联系方式
    t9=r9.json()
    update_kyc_auth(registNo,custNo)
    update_batch_log()
    list=[]
    list.append(custNo)
    list.append(head)
    return list
#更新kyc认证状态及其值
def update_kyc_auth(registNo,custNo):
    t=str(time.time()*1000000)[:15]
    tnum1=str(random.randrange(10000,99999))
    tnum2=str(random.randrange(10000,99999))
    tnum3=str(random.randrange(10000,99999))
    inst_time=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    sql="update cu_cust_auth_dtl set KYC_AUTH='1' WHERE CUST_NO='"+custNo+"';"  #客户认证信息明细表kyc认证状态
    DataBase(which_db).executeUpdateSql(sql)
    sql2="INSERT INTO `mex_pdl_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum1+"', '"+registNo+"', '"+custNo+"', '201', '10070001', '100700011621408803787.jpg', '100700011621408803787.jpg', NULL, '.jpg', '307350', '201/20210519/9999990000/', NULL, NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    sql3="INSERT INTO `mex_pdl_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum2+"', '"+registNo+"', '"+custNo+"', '201', '10070002', '100700021621408806923.jpg', '100700021621408806923.jpg', NULL, '.jpg', '317778', '201/20210519/9999990000/', NULL, NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    sql4="INSERT INTO `mex_pdl_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum3+"', '"+registNo+"', '"+custNo+"', '201', '10070004', '100700041621408812009.jpg', '100700041621408812009.jpg', NULL, '.jpg', '190855', '201/20210519/9999990000/', NULL, NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    DataBase(which_db).executeUpdateSql(sql2)
    DataBase(which_db).executeUpdateSql(sql3)
    DataBase(which_db).executeUpdateSql(sql4)
def for_bank_auth():
    test_data=for_apply_loan()
    custNo=test_data[0]
    head=test_data[1]
    data10={"custNo":custNo}
    r=requests.post(host_api+'/api/loan/apply',data=json.dumps(data10),headers=head)
    t=r.json()
    loanNo=t['data']['loanNo']
    list=[]
    list.append(custNo)
    list.append(head)
    list.append(loanNo)
    return list
#当前时间的前一天=跑批业务日期，才能正常申请借款
def update_batch_log():
    sql='select now();'
    date_time=DataBase(which_db).get_one(sql)
    d=str(date_time[0]+datetime.timedelta(days=-1))
    yudate=d[:4]+d[5:7]+d[8:10]
    sql2='select BUSI_DATE from sys_batch_log order by BUSI_DATE desc limit 1;'
    BUSI_DATE=DataBase(which_db).get_one(sql2)
    if yudate==BUSI_DATE[0]:
        print("当前服务器日期为:",date_time[0])
        print("当期系统跑批业务日期为:",BUSI_DATE[0],"无需修改批量日期")
    else:
        sql3="update sys_batch_log set BUSI_DATE='"+yudate+"' where BUSI_DATE='"+BUSI_DATE[0]+"';"
        DataBase(which_db).executeUpdateSql(sql3)
    DataBase(which_db).closeDB()

def head_token(token):
    head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "es","accept-encoding": "gzip","content-length": "24","host_api": "test-api.quantx.mx","x-app-name": "LanaPlus","content-type": "application/json",
        "x-app-type": "10090001","x-app-version": "116","x-app-no": appNo,"x-auth-token":'Bearer '+token }
    return head
def head_token_f(token):
    head={"user-agent": "Dart/2.13 (dart:io)","x-user-language": "es","accept-encoding": "gzip","content-length": "2894270","host_api": "test-api.quantx.mx","x-app-name": "LanaPlus",
          "content-type": "multipart/form-data; boundary=--dioBoundary&Happycoding-2462877051",
          "x-app-type": "10090001","x-app-version": "131","x-app-no": appNo,"x-auth-token":'Bearer '+str(token) }
    return head
