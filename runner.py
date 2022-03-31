# -*- coding:utf-8 -*-
"""
@Time:
@Auth:
@Company:
@Function:
"""
import os,pytest
from lib.cases.params import datas

print(datas)

# 执行pytest单元测试，生成 Allure 报告需要的数据存在 /temp 目录
pytest.main(['-s','ddt/Commerce_test3.py','--alluredir', './temp'])
# 执行命令 allure generate ./temp -o ./report --clean ，生成测试报告
# 使用Jenkins持续集成时，此句写到Jenkins中
os.system('allure generate ./temp -o ./report --clean')