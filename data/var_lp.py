__all__=['host_api','host_action','host_mgt','head_api','host_pay','host_coll','head_coll','head_mgt','head_pay','head_msg','host_msg','CONFIGS','prodNo','which_db','appNo','shenpiren']

appNo='201'    #当前产品号，测试201用多期，马甲包只支持单期
shenpiren={'201':['wangs2@whalekun.com','https://test-mgt.lanaplus.mx','28070110','mex_pdl_loan','LanaPlus'],'202':['wangs@whalekun.com','https://test-mgt.feriarapida.mx','25002400','mex_pdl_loan','FeriaRapida']}
which_db=shenpiren[appNo][3]   #数据库库名
prodNo=shenpiren[appNo][2]     #产品编号
host_mgt=shenpiren[appNo][1]   #MGT域名
host_api="https://test-api.quantx.mx"        #APP
host_action="https://test-action.quantx.mx"  #埋点
host_pay="https://test-pay.quantx.mx"        #支付
host_coll="https://test-coll.quantx.mx"      #催收
host_msg="https://test-msg.quantx.mx"        #消息
head_api={"User-Agent": "PostmanRuntime/7.29.0","X-User-Language": "es","X-Auth-Token": "Bearer" ,"Accept-Encoding": "gzip","Accept": "*/*",
          "Content-Length": "106","Host": host_mgt[8:],"X-App-Name": "LanaPlus","Content-Type": "application/json","Connection":"keep-alive",
          "X-App-Type": "10090001","X-App-Version": "1.3.6","X-App-No": appNo}
head_mgt={"Host": host_mgt[8:],"Connection": "keep-alive","Content-Length": "55",
"sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',"Accept": "application/json, text/plain, */*","sec-ch-ua-mobile": "?0",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
"Content-Type": "application/json;charset=UTF-8","Origin":host_mgt,"Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty","Referer": host_mgt,"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9","Cookie": "language=zh"}
head_pay={"Host": host_pay[8:],"Connection": "keep-alive","Content-Length": "55",
"sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',"Accept": "application/json, text/plain, */*","sec-ch-ua-mobile": "?0",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
"Content-Type": "application/json;charset=UTF-8","Origin": host_pay,"Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty","Referer": host_pay,"Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Cookie": "language=zh"}
CONFIGS = {
    'mex_pdl_loan': {'host':'192.168.0.60','port':3306, 'user': 'cs_wangs','password': 'cs_wangs!qw####','database': 'mex_pdl_loan'},
    'manage_need_loan': {'host':'13.235.214.155','port':3306, 'user': 'cs_wangs','password': 'cs_wangs!qw####','database': 'manage_need_loan'}
}


head_msg={"Content-Type": "application/json",
"User-Agent": "PostmanRuntime/7.28.4",
"Accept": "*/*",
"Postman-Token": "bc11f9a5-e351-4f92-85cb-a590c0557047",
"Host": "test-msg.quantx.mx",
"Accept-Encoding": "gzip, deflate, br",
"Connection": "keep-alive",
"Content-Length": "286"}
head_coll={"Content-Type": "application/json",
"User-Agent": "PostmanRuntime/7.28.4",
"Accept": "*/*",
"Postman-Token": "2e87c93f-3a5f-4070-b579-e14787d344ab",
"Host": "test-coll.quantx.mx",
"Accept-Encoding": "gzip, deflate, br",
"Connection": "keep-alive",
"Content-Length": "210"}