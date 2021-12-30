from api_auto_test.public.dataBase import *
from decimal import Decimal
import datetime

def zhuan_huan(result):
    m=[]
    m.append(result)
    t=[tuple(str(n) for n in m) for  m in m]  #python列表数字里混入一个Decimal，转换方式
    return t

def cx_lo_loan_dtl(loan_no):
    sql='''#lo_贷款基本明细表
    select APPR_AMT,LOAN_AMT,INST_NUM,BEFORE_STAT,AFTER_STAT,SETTLEMENT_TIME from lo_loan_dtl where loan_no="'''+loan_no+'''";
    '''
    result=DataBase(which_db).get_one(sql)
    t=zhuan_huan(result)
    return t

def cx_fin_tran_pay_dtl(loan_no):
    sql='''#fin_渠道放款明细表
    select TRAN_AMT,TRAN_PAY_STAT from fin_tran_pay_dtl where loan_no="'''+loan_no+'''";
    '''
    result=DataBase(which_db).get_one(sql)
    t=zhuan_huan(result)
    return t
def cx_pay_tran_dtl(loan_no):
    sql='''#交易明细表
    SELECT TRAN_TYPE, TRAN_USE,TRAN_DC,ACT_TRAN_AMT,TRAN_STAT from pay_tran_dtl where loan_no="'''+loan_no+'''";
    '''
    result=DataBase(which_db).get_one(sql)
    t=zhuan_huan(result)
    #print(t)
    return t
def cx_lo_loan_prod_rel(loan_no):
    sql='''#lo_贷款与产品的关系表
    SELECT PROD_NO,PROD_NAME from lo_loan_prod_rel where loan_no="'''+loan_no+'''";
    '''
    result=DataBase(which_db).get_one(sql)
    #print(result)
    return result
def cx_dc_flow_dtl(loan_no):
    sql='''#dc_借贷流水表 注意交易科目及借贷方向，已结清则能平账     C的总和-D的总和=0
    select SUBJ_NO,INST_NUM,TRAN_AMT,DC_DIRECT from dc_flow_dtl where LOAN_NO="'''+loan_no+'''" order by subj_no asc;
    '''
    result=DataBase(which_db).get_all(sql)
    m=[]
    for i in range(len(result)):
        t=zhuan_huan(result[i])
        m.append(t[0])
    #print(m)
    return m
def cx_lo_loan_plan_dtl(loan_no):
    sql='''#lo_还款计划明细表 注意还款状态及还款金额和时间 repay_stat=10270005结清
    select INST_NUM,REPAY_DATE,REPAY_STAT from lo_loan_plan_dtl where LOAN_NO="'''+loan_no+'''" order by inst_num asc;
    '''
    result=DataBase(which_db).get_all(sql)
    #print(result)
    return result
def cx_fin_ac_dtl(loan_no):
    sql='''#fin_应付明细表
    select PAY_AMT,TRANSTER_TYPE, AC_STAT from fin_ac_dtl where LOAN_NO="'''+loan_no+'''";
    '''
    result=DataBase(which_db).get_one(sql)
    t=zhuan_huan(result)
    #print(t)
    return t

def cx_fin_ac_dtl_for_huigun(loan_no):
    sql='''#fin_应付明细表
    select PAY_AMT,TRANSTER_TYPE, AC_STAT from fin_ac_dtl where LOAN_NO="'''+loan_no+'''";
    '''
    result=DataBase(which_db).get_one(sql)
    #print(t)
    return result
def cx_fin_ad_dtl(loan_no):
    sql='''#fin_应收表,结清后,该表数据移入备份表
    select REPAY_DATE,RECEIVE_AMT,AD_STAT,AD_TYPE,TRANSTER_TYPE from fin_ad_dtl where LOAN_NO="'''+loan_no+'''" order by repay_date asc;
    '''
    result=DataBase(which_db).get_all(sql)
    m=[]
    for i in range(len(result)):
        t=zhuan_huan(result[i])
        m.append(t[0])
    #print(m)
    return m
def cx_fin_ad_detail_dtl(loan_no):
    sql='''#应收明细表，结清后，该表数据清空
    select repay_date,SUBJ_NO, RECEIVE_AMT,AD_TYPE,TRANSTER_TYPE from fin_ad_detail_dtl  where LOAN_NO="'''+loan_no+'''" order by repay_date,SUBJ_NO asc;
    '''
    result=DataBase(which_db).get_all(sql)
    m=[]
    for i in range(len(result)):
        t=zhuan_huan(result[i])
        m.append(t[0])
    #print(m)
    return m
def cx_fin_rc_dtl(loan_no):
    sql='''#fin_实付明细表，付给客户及付给内部账户金额检查
    select REAL_PAY_AMT,TRANSTER_TYPE,RC_STAT from fin_rc_dtl  where LOAN_NO="'''+loan_no+'''";
    '''
    result=DataBase(which_db).get_one(sql)
    t=zhuan_huan(result)
    #print(t)
    return t
def cx_fin_rc_dtl_for_huigun(loan_no):
    sql='''#fin_实付明细表，付给客户及付给内部账户金额检查
    select REAL_PAY_AMT,TRANSTER_TYPE,RC_STAT from fin_rc_dtl  where LOAN_NO="'''+loan_no+'''";
    '''
    result=DataBase(which_db).get_one(sql)
    return result
def cx_pay_tran_log(loan_no):
    sql='''select TRAN_MSG,TRAN_STAT from pay_tran_log where LOAN_NO="'''+loan_no+'''" order by INST_TIME desc;
'''
    result=DataBase(which_db).get_one(sql)
    return result
def jisuan_repay_date(loan_no):
    sql='''select date(WITHDRAW_SUCCESS_TIME),INST_NUM from lo_loan_dtl where loan_no="'''+loan_no+'''";'''
    result=DataBase(which_db).get_one(sql)
    m=[]
    for i in range(result[1]):
        d=str(result[0]+datetime.timedelta(days=+7*(i+1)))
        repay_date=d[:4]+d[5:7]+d[8:10]
        m.append(repay_date)
    return m
def jisuan_repay_date_fr(loan_no):
    sql='''select date(WITHDRAW_SUCCESS_TIME),INST_NUM from lo_loan_dtl where loan_no="'''+loan_no+'''";'''
    result=DataBase(which_db).get_one(sql)
    m=[]
    for i in range(result[1]):
        d=str(result[0]+datetime.timedelta(days=+3*(i+1)))  #25002400:三天周期
        repay_date=d[:4]+d[5:7]+d[8:10]
        m.append(repay_date)
    return m
def jisuan_repay_date_huigun():
    sql='''select date(now());'''
    result=DataBase(which_db).get_one(sql)
    nowdate=result[0]
    d=str(nowdate+datetime.timedelta(days=+2))  #25002400:三天周期
    repay_date=d[:4]+d[5:7]+d[8:10]
    print(repay_date)
    return repay_date

if __name__ == '__main__':
    #cx_lo_loan_plan_dtl("L2012112038155060734586454016")
    jisuan_repay_date_huigun()