# -*- coding utf-8 -*-
# @Time    : 2020/11/11 20:57
# @Author  : DesireYang
# @Email   : yangyin1106@163.com
# @File    : pyxMind2.0.py
# Software : PyCharm
# Explain  :
from PyQt5.QtGui import QIcon

from common.ExcelData import ExcelData
from common.XMindData import XMindData

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QTableWidget, \
    QTableWidgetItem, QAbstractItemView, QMessageBox, QHBoxLayout, QComboBox
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl


class PyxMind(QWidget):

    def __init__(self):
        super(PyxMind, self).__init__()
        self.title = ['用例目录', '用例名称', '需求ID', '前置条件',
                      '用例步骤', '预期结果', '用例类型', '用例状态', '用例等级']
        self.row = 1
        self.column = len(self.title)
        self.initUi()

    def initUi(self):
        self.setWindowTitle("XMind转换成Excel")
        self.setWindowIcon(QIcon("./Icon/window.ico"))
        self.resize(500, 400)
        # 使用水平布局
        layout = QHBoxLayout()

        self.tablewidget = QTableWidget()

        self.tablewidget.setColumnCount(self.column)
        self.tablewidget.setSelectionBehavior(
            QAbstractItemView.SelectRows)  # 设置表格的选取方式是行选取
        self.tablewidget.setSelectionMode(
            QAbstractItemView.SingleSelection)  # 设置选取方式为单个选取
        self.tablewidget.setHorizontalHeaderLabels(self.title)
        # 自动换行
        self.tablewidget.setWordWrap(True)
        # 自动调整行高
        self.tablewidget.resizeRowsToContents()

        # table中有改动的时候调用
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

        w2 = QWidget()
        layout2 = QVBoxLayout()

        layout2.addWidget(self.button1)
        layout2.addWidget(self.button2)
        layout2.addWidget(self.comboBox)

        layout.addWidget(self.tablewidget)
        w2.setLayout(layout2)
        layout.addWidget(w2)
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
            self.tablewidget.resizeColumnToContents(case[0])
            # 用例步骤
            step = ""
            # 预期结果
            er = ""
            # 前置条件
            pt = ""
            # 后面数据需要剔除掉的列表索引
            pop_index: list = []
            # 处理步骤、前置条件、预期结果
            for c in enumerate(case[1]):
                if c[1].startswith('step'):
                    step = c[1].strip('step>')
                    pop_index.append(c[0])
                elif c[1].startswith('er'):
                    er = c[1].strip('er>')
                    pop_index.append(c[0])
                elif c[1].startswith('pt'):
                    pt = c[1].strip('pt>')
                    pop_index.append(c[0])

            # 剔除步骤前置条件的列表
            case_data = [case[1][i] for i in range(len(case[1])) if i not in pop_index]
            print(case_data)
            # 用例目录
            self.tablewidget.setItem(
                case[0], 0, QTableWidgetItem(case_data[0]))
            # 用例名称
            self.tablewidget.setItem(
                case[0], 1, QTableWidgetItem("_".join(case_data[1:])))
            # 需求ID
            self.tablewidget.setItem(case[0], 2, QTableWidgetItem(''))
            # 前置条件
            self.tablewidget.setItem(case[0], 3, QTableWidgetItem(pt))
            # 用例步骤
            self.tablewidget.setItem(case[0], 4, QTableWidgetItem(step))
            # 预期结果
            self.tablewidget.setItem(case[0], 5, QTableWidgetItem(er))
            # 用例类型
            self.tablewidget.setItem(case[0], 6, QTableWidgetItem('功能测试'))
            # 用例状态
            self.tablewidget.setItem(case[0], 7, QTableWidgetItem('正常'))
            # 用例等级
            self.tablewidget.setItem(case[0], 8, QTableWidgetItem('中'))

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
                    titles=self.title)
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
        Numbering = 0000
        if text == "aaaa":
            Numbering = 78945612
        elif text == "bbbb":
            Numbering = 12121212
        elif text == "ccccc":
            Numbering = 13131313
        elif text == "ddddd":
            Numbering = 14141414
        elif text == "请选择项目去上传":
            return
        QDesktopServices.openUrl(
            QUrl(f'https://www.baidu.com/{Numbering}'))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = PyxMind()
    main.show()
    sys.exit(app.exec_())
