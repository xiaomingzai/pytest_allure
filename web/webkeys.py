# -*- coding:utf-8 -*-
"""
@Time:
@Auth:
@Company:
@Function:关键字封装
"""
import allure
from selenium import webdriver
import time,os,logging

# logging.basicConfig(
#     level=logging.INFO,
#     filename = "test.log",
#     format="%(asctime)s   %(levelname)-8s  [%(filename)s:%(lineno)s]  %(message)s"
# )

class  WebKey:

    def __init__(self):
        """
        构造函数，创建必要的实例变量
        """
        #self.driver = None
        self.driver = None


    def openbrowser(self,br = 'gc'):
        """
        打开浏览器
        :param br: gc=谷歌浏览器;ff=Firefox浏览器;ie=IE浏览器
        :return:
        """
        if br == 'gc':
            self.driver=webdriver.Chrome()
        elif br == 'ff':
            self.driver = webdriver.Firefox()
        elif br == 'ie':
            self.driver = webdriver.Ie()
        else:
            print('浏览器不支持！请在此添加实现代码')
            #pass
        #默认隐式等待10s
        self.driver.implicitly_wait(10)

    def geturl(self,url=None):
        """
        打开网站
        :param url:网站地址
        :return:
        """
        self.driver.get(url)

    def __find_ele(self,locator=''):
        """
        支持八种定位方式
        :param locator: xpath=//*[@id="username"]
        :return: 返回定位到的元素
        """
        ele = None
        self.ele = None
        if locator.startswith('xpath='):
            ele = self.driver.find_element_by_xpath(locator[locator.find('=')+1:])
        elif locator.startswith('id='):
            ele = self.driver.find_element_by_id(locator[locator.find('=')+1:])
        elif locator.startswith('name='):
            ele = self.driver.find_element_by_name(locator[locator.find('=')+1:])
        elif locator.startswith('tag_name='):
            ele = self.driver.find_element_by_tag_name(locator[locator.find('=')+1:])
        elif locator.startswith('link_text='):
            ele = self.driver.find_element_by_link_text(locator[locator.find('=')+1:])
        elif locator.startswith('partial_link_text='):
            ele = self.driver.find_element_by_partial_link_text(locator[locator.find('=')+1:])
        elif  locator.startswith('css_selector='):
            ele = self.driver.find_element_by_css_selector(locator[locator.find('=')+1:])
        else:
            ele = self.driver.find_element_by_xpath(locator)

        self.ele = ele
        return ele



    def click(self,locator=None):
        """
        找到，并点击元素
        :param locator: 定位器，默认xpath
        :return:
        """
        #self.driver.find_element_by_xpath(locator).click()
        ele = self.__find_ele(locator)
        ele.click()

    def input(self,locator=None,value=None):
        """
        找到元素，并完成输入
        :param locator: 定位器，默认xpath
        :param value:需要输入的字符串
        :return:
        """
        #self.driver.find_element_by_xpath(locator).send_keys(str(value))
        ele = self.__find_ele(locator)
        ele.send_keys(str(value))

    def intoiframe(self,locator=None):
        """
        进入iframe
        :param locator: 定位器，默认xpath
        :return:
        """
        ele = self.__find_ele(locator)
        self.driver.switch_to.frame(ele)

    def quit(self):
        """
        退出浏览器
        :return:
        """
        self.driver.quit()

    def max_window(self):
        self.driver.maximize_window()

    def open_new_bookmark(self, url=None):
        """
        一个浏览器打开多个页签
        如果当前没有打开任何页面，直接调用此函数会出现一个空白页后再打开open_new_bookmark要访问的url
        需要先调用open
        :param url: 网址
        """
        js = f"window.open('{url}')"
        self.driver.execute_script(js)
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def sleep(self,value=1):
        """
        固定等待
        :param value:等待时间（s）
        :return:
        """
        time.sleep(int(value))

    def implicitly_wait(self,value=None):
        self.driver.implicitly_wait(value)

     def screenshot(self):
         self.driver.get_screenshot_as_png()

    @allure.step
    def run_step(self,func, values):
        func(*values)

        
    # def logger(self):
    #     self.logger = logging.getLogger(f"{self.id()}")  # id的方法

    # def save_scree_image(self):
    #     """
    #     对当前页面进行截图
    #     :return:
    #     """
    #     start_time = time.time()
    #     filename = '{}.png'.format(start_time)
    #     file_path = os.path.join(error_img, filename)
    #     self.driver.save_screenshot(file_path)
    #     log.info("错误页面截图成功，图表保存的路径:{}".format(file_path))
    #     return file_path
    #
    # def save_image_to_allure(self):
    #     """
    #     保存失败的截图到allure报告中
    #     :return:
    #     """
    #     file_path = self.save_scree_image()
    #     with open(file_path, "rb") as f:
    #         file = f.read()
    #         allure.attach(file, "失败截图", allure.attachment_type.PNG)

