import unittest,os,datetime
from BeautifulReport import BeautifulReport as bf  #导入BeautifulReport模块，这个模块也是生成报告的模块，但是比HTMLTestRunner模板好看
from HTMLTestRunner_Chart import HTMLTestRunner

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")

current_path=os.getcwd()  #获取当前路径
case_path=os.path.join(current_path,"TestCase")
report_path=os.path.join(current_path,"Report")

riqi=str(datetime.datetime.now().strftime('%Y_%m_%d'))

def load_all_case():
    discover=unittest.defaultTestLoader.discover(case_path,pattern='*.py')
    return discover

if __name__=='__main__':
    bf(load_all_case()).report(filename='App_Api_Auto_Test_Report'+riqi, description='app接口自动化测试')    #log_path='.'把report放到当前目录下
    #print(load_all_case())
