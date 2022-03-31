# -*- coding:utf-8 -*-
"""
@Time:
@Auth:
@Company:
@Function:使用pytest编写实现模拟手动登录AcFun网站https://www.acfun.cn，最原始的代码，未进行任何参数化、数据驱动等操作
"""

from selenium import webdriver
import time,os,pytest,allure

from selenium.webdriver.remote.webelement import WebElement


class Test_Comm:
    """
    PO封装
    """
    def setup_class(self):
        """
        构造函数，创建对象的时候会执行
        初始化浏览器
        """
        self.driver = webdriver.Chrome()
        #隐式等待
        #每隔一秒钟找一次元素，如果找到了就继续运行
        #如果超过10s还没找到，那么就是no such element
        self.driver.implicitly_wait(10)

    def test_login(self):
        """
        登录成功的用例
        :return: None
        """
        self.driver.get('https://www.acfun.cn/login/')
        #浏览器最大化
        self.driver.maximize_window()
        #打印当前界面的句柄
        current_handle = self.driver.current_window_handle
        print('current_handle',current_handle)
        self.driver.implicitly_wait(2)#如果找到了就继续，否则等待两秒

        #账号登录
        self.driver.find_element_by_xpath('//*[@id="login-account-switch"]').click()
        #输入账号、密码，点击“登录”按钮
        self.driver.find_element_by_xpath('//*[@id="ipt-account-login"]').send_keys('1292510200@qq.com')
        self.driver.find_element_by_xpath('//*[@id="ipt-pwd-login"]').send_keys('123456')
        self.driver.find_element_by_xpath('//*[@id="form-login"]/div[4]/div').click()

    def test_userinfo(self):
        """
        需要先调用登录成功的用例
        :return:
        """

        #获取当前打开页面的所有句柄并打印，应该只有一个
        all_handles1=self.driver.window_handles
        print('all_handles',all_handles1)
        self.driver.implicitly_wait(2)

        #进入个人中心
        time.sleep(5)
        self.driver.find_element_by_xpath('//*[@id="header-guide"]/li[2]/a/img').click()
        #self.driver.get('https://www.acfun.cn/member/')
        time.sleep(3)

        #获取进入新窗口后所有的句柄，并打印当前所有的句柄，此次应该有2个了
        all_handles2=self.driver.window_handles
        print('all_handles',all_handles2)
        self.driver.implicitly_wait(2)

        #拿到新窗口句柄
        newhandle = [handle for handle in all_handles2 if handle not in all_handles1]
        print('newhandle',newhandle[0])
        #切换到新窗口
        self.driver.switch_to.window(newhandle[0])

        #编辑资料》修改头像》点击“重新选择图片”按钮》选择图片》“确定”上传
        self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/main/div/div/div/div[1]/div[1]/div[2]/a').click()
        self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/main/div/div/div/div/div/div[1]/div/div[1]/div/img').click()
        time.sleep(3)
        #点击“重新选择图片”按钮
        self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[1]/div/div[4]/div[1]/button').click()

        #使用AutoIt工具生成
        os.system('D:/image/uploadFile.exe')

        time.sleep(3)
        #点击确定
        self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div/div[1]/div/div[4]/div[2]/button').click()

    def test_search(self):
        """
        依赖登录
        :return:
        """
        time.sleep(1)
        self.driver.get('https://www.acfun.cn/member/')
        self.driver.find_element_by_xpath('//*[@id="header"]/div/div[5]/span/input').send_keys('胖胖的山头')
        self.driver.find_element_by_xpath('//*[@id="header"]/div/div[5]/span/div/span/i').click()

    def teardown_class(self):
        self.driver.quit()


if __name__=="__main__":
    comm = Test_Comm()
    comm.test_login()
    comm.test_userinfo()
    comm.test_search()
