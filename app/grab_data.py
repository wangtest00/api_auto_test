from dataBase.dataBase_tur import *

def cx_grab_data(registNo):
    sql1="select IMEI from lo_loan_cust_third_gps_dtl WHERE PHONE_NO='"+registNo+"';" #GPS
    sql2="select FILE_PATH from lo_loan_msg_dtl WHERE PHONE_NO='"+registNo+"';"       #msg
    sql3="select PATH from lo_applist_file_dtl WHERE PHONE_NO='"+registNo+"';"        #applist
    sql4="select IMEI from lo_loan_cust_third_device_dtl WHERE PHONE_NO='"+registNo+"';"#设备信息
    sql5="select PATH from lo_address_book_file_dtl WHERE PHONE_NO='"+registNo+"';"   #通讯录
    data_list=[]
    data_list.append(DataBase(inter_db).get_one(sql1)[0])
    data_list.append(DataBase(inter_db).get_one(sql2)[0])
    data_list.append(DataBase(inter_db).get_one(sql3)[0])
    data_list.append(DataBase(inter_db).get_one(sql4)[0])
    data_list.append(DataBase(inter_db).get_one(sql5)[0])
    print(data_list)
    return data_list


if __name__ == '__main__':
    cx_grab_data('8931096039')