# -*- coding utf-8 -*-
# @Time    : 2020/11/21 15:31
# @Author  : DesireYang
# @Email   : yangyin1106@163.com
# @File    : toExcel.py
# Software : PyCharm
# Explain  : 操作例子

from common.XMindData import XMindData
from common.ExcelData import ExcelData

xd = XMindData()
all_data = xd.read_XMind_to_list(XMindName="../data/case.xmind")
# print(all_data)
data = all_data[0]['topic']['topics']
print(data)
cases_data = xd.get_lists_data(data)
print(cases_data)
ed = ExcelData(file_name="../data/case.xlsx")
ed.create_excel_and_set_title(['用例目录', '用例名称'])
for case in enumerate(cases_data):
    print(case)
    num = case[0]
    print(type(num))
    ed.write_excel_data(row=num + 2, column=1, value=case[1][0])
    ed.write_excel_data(row=num + 2, column=2, value='_'.join(case[1][1:]))
