# -*- coding:utf-8 -*-
"""
@Time:
@Auth:
@Company:
@Function:
"""

import yaml

datas = None

#读取数据驱动的数据
with open('./lib/cases/cases.yaml',encoding='utf-8') as f:
    datas = yaml.safe_load(f)

print(datas)