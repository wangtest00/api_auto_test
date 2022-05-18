import random,string,time,datetime
from data.var_tur_app import *
from dataBase.dataBase_tur import *

def certlist():
    st=''
    for j in range(5):  #生成5个随机英文大写字母
        st+=random.choice(string.ascii_uppercase)
    num = str(random.randint(1000, 9999))
    certNo=num+"6666"+num
    panNo=st+num+"W"
    certlist=[]
    certlist.append(certNo)
    certlist.append(panNo)
    #print(certlist)
    return certlist
#插入白名单
def insert_white_list(registNo):
    t =str(time.time() * 1000000)[:15]
    inst_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    sql='''INSERT INTO `manage_need_loan`.`cu_white_list_dtl`(`ID`, `WHITE_LIST_TYPE`, `WHITE_LIST_VALUE`, `APP_NO`, `RISK_SCORE`, `USEABLE`, `VALID_START_DATE`, `VALID_END_DATE`, `ORIGIN`, `DESCRIPTION`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) 
    VALUES ("'''+t+'''", '10140001', "'''+registNo+'''", "'''+appNo+'''", "'''+prodNo+'''", '10000001', '20220415', '20220715', 'auto_test', NULL, NULL, "'''+inst_time+'''", 'wangs@whalekun.com', "'''+inst_time+'''", 'wangs@whalekun.com');'''
    DataBase(inter_db).executeUpdateSql(sql)
 #退出登录
def logout(driver):
    driver.find_element_by_id('com.turrant:id/radio_mine').click()
    time.sleep(3)
    driver.find_element_by_id('com.turrant:id/exit_layout').click()
    time.sleep(3)
    driver.find_element_by_id('com.turrant:id/btn_sure').click()

if __name__ == '__main__':
    insert_white_list('7474742222')