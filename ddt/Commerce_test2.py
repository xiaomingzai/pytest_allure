# -*- coding:utf-8 -*-
"""
@Time:
@Auth:
@Company:
@Function:使用pytest编写实现模拟手动登录AcFun网站https://www.acfun.cn，并生成有一定程度定制化的allure报告
关键字封装在./web/webkeys.py中，
使用yaml数据驱动将参数写在了./lib/cases/目录中，cases.yaml是测试用例数据，params.py用于读取数据驱动的数据，
生成allure报告的代码写在了根目录下的runner.py，修改指向需要执行的.py文件，执行runner.py即可运行
"""

from web.webkeys import WebKey

import time, pytest,allure
from lib.cases.params import datas

@allure.feature('电商项目Web自动化')
class Test_Commerce:
    """
    电商项目Web自动化
    """

    @allure.title('打开浏览器')
    def setup_class(self):
        """
        构造函数，创建对象的时候会执行
        初始化浏览器
        """
        self.web = WebKey()
        #打开浏览器
        self.web.openbrowser()
        #浏览器最大化
        self.web.max_window()
        time.sleep(3)

    @allure.story('登录')
    @allure.description('登录测试用例')
    @pytest.mark.parametrize('listcases',datas['loginPage'])
    def test_login(self,listcases):
        try:
            #如果没有title或者description会报错，添加try except 让缺少title或者description时不会报错
            allure.dynamic.title(listcases['title'])
            allure.description(listcases['description'])
        except Exception as e:
            pass

        testcases = listcases['cases']   #将case.yaml中的cases取出来，得到的是一个字典
        for cases in testcases:
            listcase =list(cases.values()) #获取字典的列表值
            """
            ['打开登录页', 'geturl', 'https://www.acfun.cn/login']
            ['切换到账号登录', 'click', 'xpath=//*[@id="login-account-switch"]']
            ['输入用户名', 'input', 'xpath=//*[@id="ipt-account-login"]', '1292510200@qq.com']
            ['输入密码', 'input', 'xpath=//*[@id="ipt-pwd-login"]', '123456']
            ['点击登录', 'click', 'xpath=//*[@id="form-login"]/div[4]/div']
            """
            with allure.step(listcase[0]):
                func = getattr(self.web,listcase[1])
                values=listcase[2:]
                func(*values)

    def teardown_class(self):
        self.web.quit()

    # @allure.step
    # def run_step(self,func,parmas):
    #     #获取参数列表
    #     params = params[:params.index('')]
    #     logger.info(params)
    #     #开始执行
    #     if params：
    #         func(*params)
    #     else:
    #         func()

if __name__=="__main__":
    comm = Test_Commerce()
    comm.test_login()
    comm.teardown_class()


    # # 执行pytest单元测试，生成 Allure 报告需要的数据存在 /temp 目录
    # pytest.main(['--alluredir', './temp'])
    # # 执行命令 allure generate ./temp -o ./report --clean ，生成测试报告
    # os.system('allure generate ./temp -o ./report --clean')



# try：
#     aaaaaaaa
# except:
#     pytest.fail('用例执行失败')
# finally：
#     allure.attach(self.web.get_screenshot_as_png(), '运行结果截图', allure.attachment_type.PNG)
