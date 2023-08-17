# -*- coding utf-8 -*-
# @Time    : 2020/11/21 14:59
# @Author  : DesireYang
# @Email   : yangyin1106@163.com
# @File    : readXmind.py
# Software : PyCharm
# Explain  :

import jsonpath
from xmindparser import xmind_to_dict

data = xmind_to_dict(file_path="../data/case.xmind")
print(data[0]['topic']['topics'])
result = jsonpath.jsonpath(data[0]['topic']['topics'][0], "$.topics")
print(result)

result = jsonpath.jsonpath(result[0][0], "$.topics")
print(result)
