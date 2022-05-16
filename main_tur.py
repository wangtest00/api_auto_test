import unittest,os,io,sys
from BeautifulReport import BeautifulReport as bf  #导入BeautifulReport模块，这个模块也是生成报告的模块，但是比HTMLTestRunner模板好看
#from HTMLTestRunner_Chart import HTMLTestRunner
from XTestRunner import HTMLTestRunner
from unittestreport import TestRunner

current_path=os.getcwd()  #获取当前路径
case_path=os.path.join(current_path,"TestCase")
report_path=os.path.join(current_path,"Report")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")

def load_all_case():
    discover=unittest.defaultTestLoader.discover(case_path,pattern='Test_*.py')
    return discover

if __name__=='__main__':
    #bf(load_all_case()).report(filename='LP_FR_Api_Auto_Test_Report', description='LP_FR接口自动化测试')    #log_path='.'把report放到当前目录下
    suite=load_all_case()
    # 执行用例
    runner = TestRunner(suite,
                        filename='Turrant_Test_Reports.html',
                        title='Turrant_Test_Reports',
                        tester='WANGSHUANG',
                        desc="Turrant_Ui_Auto_Test",
                        templates=1
                        )
    # 指定三个线程运行测试用例
    runner.run(thread_count=3)