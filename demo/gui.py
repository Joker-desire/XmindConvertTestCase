# -*- coding utf-8 -*-
# @Time    : 2020/11/21 15:55
# @Author  : DesireYang
# @Email   : yangyin1106@163.com
# @File    : gui.py
# Software : PyCharm
# Explain  :

import sys

# 这里提供必要的引用，基本空间位于pyqt5.qtwidegets模块中
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout

# 每一个pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数
app = QApplication(sys.argv)

# QWidget部件是pyqt5所有用户界面对象的基类。他为QWidget提供默认构造函数。默认构造函数没有父类
w = QWidget()

# resize()方法调整窗口的大小。这里是400px宽400px高
w.resize(400, 400)
# 垂直布局
layout = QHBoxLayout()

label = QLabel()
label.setText("Hello World!")
layout.addWidget(label)

label2 = QLabel()
label2.setText("Hello Python!")
layout.addWidget(label2)
w.setLayout(layout)
# 设置窗口的标题
w.setWindowTitle('简单的例子')
# 显示在屏幕上
w.show()

# 系统exit()方法确保应用程序干净的退出
# 的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
sys.exit(app.exec_())
