# -*- coding:utf-8 -*-
"""
@Time:
@Auth:
@Company:
@Function:使用pytest编写实现模拟手动登录AcFun网站https://www.acfun.cn，并生成allure报告
在Commerce_test0.py的基础上进行了关键字封装
关键字封装在./web/webkeys.py中，
使用yaml数据驱动将参数写在了./lib/cases/目录中，cases.yaml是测试用例数据，params.py用于读取cases.yaml的数据
"""

from web.webkeys import WebKey
import time, pytest,os
from lib.cases.params import datas

class Test_Commerce:
    """
    PO封装
    """
    def setup_class(self):
        """
        构造函数，创建对象的时候会执行
        初始化浏览器
        """
        self.web = WebKey()
        self.web.openbrowser()

        time.sleep(3)

    @pytest.mark.parametrize('listcases',datas['loginPage'])
    def test_login(self,listcases):
        testcases = listcases['cases']   #将case.yaml中的cases取出来，得到的是一个字典
        for cases in testcases:
            listcase =list(cases.values())   #获取字典的列表值
            """
            ['打开登录页', 'geturl', 'https://www.acfun.cn/login']
            ['切换到账号登录', 'click', 'xpath=//*[@id="login-account-switch"]']
            ['输入用户名', 'input', 'xpath=//*[@id="ipt-account-login"]', '1292510200@qq.com']
            ['输入密码', 'input', 'xpath=//*[@id="ipt-pwd-login"]', '123456']
            ['点击登录', 'click', 'xpath=//*[@id="form-login"]/div[4]/div']
            """
            func = getattr(self.web,listcase[1])
            values=listcase[2:]
            func(*values)
            self.web.time_sleep(5)

    def teardown_class(self):
        self.web.quit()

if __name__=="__main__":
    comm = Test_Commerce()
    comm.test_login()
    comm.teardown_class()

    #allure报告
    # 执行pytest单元测试，生成 Allure 报告需要的数据存在 /temp 目录
    pytest.main(['--alluredir', './temp'])
    # 执行命令 allure generate ./temp -o ./report --clean ，生成测试报告
    os.system('allure generate ./temp -o ./report --clean')
