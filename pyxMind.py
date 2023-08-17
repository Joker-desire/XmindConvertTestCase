# -*- coding utf-8 -*-
# @Time    : 2020/11/11 20:57
# @Author  : DesireYang
# @Email   : yangyin1106@163.com
# @File    : pyxMind.py
# Software : PyCharm
# Explain  :
from PyQt5.QtGui import QIcon

from common.ExcelData import ExcelData
from common.XMindData import XMindData

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QTableWidget, \
    QTableWidgetItem, QAbstractItemView, QMessageBox, QComboBox
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl


class PyxMind(QWidget):

    def __init__(self):
        super(PyxMind, self).__init__()
        self.row = 1
        self.column = 4
        self.initUi()

    def initUi(self):
        self.setWindowTitle("XMind转换成Excel")
        self.setWindowIcon(QIcon("./Icon/window.ico"))
        self.resize(500, 400)

        # 使用水平布局
        layout = QVBoxLayout()

        self.tablewidget = QTableWidget()

        self.tablewidget.setColumnCount(self.column)
        self.tablewidget.setSelectionBehavior(
            QAbstractItemView.SelectRows)  # 设置表格的选取方式是行选取
        self.tablewidget.setSelectionMode(
            QAbstractItemView.SingleSelection)  # 设置选取方式为单个选取
        self.tablewidget.setHorizontalHeaderLabels(
            ['#ID', '需求名', '用例目录', '用例名称'])
        self.tablewidget.itemChanged.connect(self.table_update)

        self.button1 = QPushButton("选择XMind文件")
        self.button1.clicked.connect(self.read_XMind)

        self.button2 = QPushButton("转成Excel")
        self.button2.clicked.connect(self.to_Excel)

        self.comboBox = QComboBox()
        self.comboBox.addItems(["请选择项目去上传", "aaaa", "bbbb", "ccccc", "ddddd"])
        self.comboBox.currentIndexChanged.connect(self.selectionChange)

        # self.button3 = QPushButton("点击去上传")
        # self.button3.clicked.connect(self.go_upload)

        layout.addWidget(self.tablewidget)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.comboBox)
        # layout.addWidget(self.button3)

        self.setLayout(layout)

    def read_XMind(self):
        """
        读取XMind数据
        """
        # 打开XMind文件
        fileName, _ = QFileDialog.getOpenFileName(
            self, "打开文件", ".", "XMind(*.xmind)")
        if fileName == "":
            return
        # 读取XMind，获取第一个画布，然后获取头节点内容
        ds = XMindData.read_XMind_to_list(fileName)[0]["topic"]
        # 获取头节点title，就是需求名
        title = ds["title"]
        # 获取头节点下的其余所有节点内容
        nodes_data = ds["topics"]
        # 创建XMData格式化xMind读取的数据
        md = XMindData()
        # 清空缓存数据
        md.clear_init_list_data()
        # 调用
        data = md.get_lists_data(data=nodes_data)
        # 动态设置行
        self.row = len(data)
        # 设置表格的行
        self.tablewidget.setRowCount(self.row)
        for case in enumerate(data):
            # id
            item1 = QTableWidgetItem(str(case[0] + 1))
            # 需求名
            item2 = QTableWidgetItem(title)
            # 模块名
            item3 = QTableWidgetItem(case[1][0])
            # 用例
            item4 = QTableWidgetItem("_".join(case[1][1:]))

            self.tablewidget.setItem(case[0], 0, item1)
            self.tablewidget.setItem(case[0], 1, item2)
            self.tablewidget.setItem(case[0], 2, item3)
            self.tablewidget.setItem(case[0], 3, item4)

    def table_update(self):
        """
        如果表格被编辑，则会保存编辑后的数据
        """
        self.tablewidget.selectedItems()

    def to_Excel(self):
        """
        保存到Excel中
        """
        # 返回值是一个元祖，需要两个参数接收，第一个是文件名，第二个是文件类型
        fileName, fileType = QFileDialog.getSaveFileName(
            self, "保存Excel", ".", "xlsx(*.xlsx)")

        if fileName == "":
            return
        else:
            try:
                if not fileName.endswith('.xlsx'):
                    # 如果后缀不是.xlsx，那么就加上后缀
                    fileName = fileName + '.xlsx'
                we = ExcelData(file_name=fileName)
                # 创建Excel
                we.create_excel_and_set_title(
                    titles=['#ID', '需求名', '用例目录', '用例名称'])
                # 保存并写入(表格中更新后的数据)写入从第二行开始写入(行需要+1，列需要+1)
                for r in range(self.row):
                    for c in range(self.column):
                        we.write_excel_data(
                            row=r + 2, column=c + 1, value=self.tablewidget.item(r, c).text())
                QMessageBox.about(
                    self, "写入Excel", "写入Excel成功！\n路径：{}".format(fileName))
            except Exception as e:
                QMessageBox.critical(self, "写入Excel", "出错了，请重试！！！\n错误信息：{}".format(
                    e), QMessageBox.Yes, QMessageBox.Yes)

    def go_upload(self):
        """
        去上传，点击跳转到指定的网址
        """
        QDesktopServices.openUrl(
            QUrl('https://www.baidu.com'))

    def selectionChange(self, i):
        """
        通过选择的下拉列表，跳转到置顶的网址
        """
        text = self.comboBox.currentText()
        if text == "aaaa":
            QDesktopServices.openUrl(
                QUrl('https://www.baidu.com'))
        print(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = PyxMind()
    main.show()
    sys.exit(app.exec_())
