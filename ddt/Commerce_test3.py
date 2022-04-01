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

import time, pytest,allure,logging
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


    @allure.step
    def run_step(self,func, values):
        func(*values)


    @allure.story('登录')
    @allure.description('登录测试用例')
    @pytest.mark.parametrize('params',datas['loginPage'])
    def test_login(self,params):
        allure.dynamic.title(params['title'])
        allure.description(params['description'])
        logger = logging.getLogger()
        logger.info(params)
        login_cases = params['cases']    #将case.yaml中的cases取出来，得到的是一个字典
        for login_case in login_cases:
            listcase = list(login_case.values())  # 获取字典的列表值
            self.stepname = listcase[0]
            func = getattr(self.web, listcase[1])
            values = list(login_case.values())[2:]    #获取字典的列表值
            with allure.step(self.stepname):
                try:
                    res = self.run_step(func,values)
                except Exception as err:
                    logger.error(login_case)
                    logger.exception(err)
                    #allure.attach(body, name, attachment_type, extension)
                    allure.attach(self.web.screenshot(),"失败截图",allure.attachment_type.PNG)
                    pytest.fail('用例执行失败：{}'.format(err))
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
