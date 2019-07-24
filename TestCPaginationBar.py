#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月23日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: TestCpaginationBar1
@description: 
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem,\
    QSizePolicy, QLineEdit, QPushButton

from CustomWidgets.CPaginationBar import CPaginationBar, FlatStyle, Style


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)

        # 测试1
        self.pageLabel1 = QLabel('当前页: 1', self, alignment=Qt.AlignCenter)
        layout.addWidget(self.pageLabel1)
        # 分页控件
        self.paginationBar1 = CPaginationBar(self, totalPages=20)
        # 设置扁平样式
        self.paginationBar1.setStyleSheet(FlatStyle)
        self.paginationBar1.pageChanged.connect(
            lambda page: self.pageLabel1.setText('当前页: %d' % page))
        layout.addWidget(self.paginationBar1)
        layout.addItem(QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum))

        # 测试2
        self.pageLabel2 = QLabel('当前页: 1', self, alignment=Qt.AlignCenter)
        layout.addWidget(self.pageLabel2)
        # 分页控件
        self.paginationBar2 = CPaginationBar(self, totalPages=20)
        # 设置普通样式
        self.paginationBar2.setStyleSheet(Style)
        self.paginationBar2.pageChanged.connect(
            lambda page: self.pageLabel2.setText('当前页: %d' % page))
        layout.addWidget(self.paginationBar2)
        layout.addItem(QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum))

        # 测试3
        self.pageLabel3 = QLabel('当前页: 1', self, alignment=Qt.AlignCenter)
        layout.addWidget(self.pageLabel3)
        # 分页控件
        self.paginationBar3 = CPaginationBar(self, totalPages=20)
        # 设置信息
        self.paginationBar3.setInfos('共 400 条')
        # 设置扁平样式
        self.paginationBar3.setStyleSheet(FlatStyle)
        self.paginationBar3.pageChanged.connect(
            lambda page: self.pageLabel3.setText('当前页: %d' % page))
        layout.addWidget(self.paginationBar3)
        layout.addItem(QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum))

        # 测试4
        self.pageLabel4 = QLabel('当前页: 1', self, alignment=Qt.AlignCenter)
        layout.addWidget(self.pageLabel4)
        # 分页控件
        self.paginationBar4 = CPaginationBar(self, totalPages=20)
        # 设置信息
        self.paginationBar4.setInfos('共 400 条')
        # 开启跳转功能
        self.paginationBar4.setJumpWidget(True)
        # 设置普通样式
        self.paginationBar4.setStyleSheet(Style)
        self.paginationBar4.pageChanged.connect(
            lambda page: self.pageLabel4.setText('当前页: %d' % page))
        layout.addWidget(self.paginationBar4)
        layout.addItem(QSpacerItem(
            40, 40, QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.pageEdit = QLineEdit(self)
        self.pageEdit.setValidator(QIntValidator(self.pageEdit))
        self.pageEdit.setPlaceholderText('输入总页数')
        layout.addWidget(self.pageEdit)
        self.setButton = QPushButton(
            '设置总页数', self, clicked=self.doSetPageNumber)
        layout.addWidget(self.setButton)

    def doSetPageNumber(self):
        page = self.pageEdit.text().strip()
        if not page:
            return
        page = int(page)
        self.paginationBar1.setTotalPages(page)
        self.paginationBar2.setTotalPages(page)
        self.paginationBar3.setTotalPages(page)
        self.paginationBar4.setTotalPages(page)


if __name__ == '__main__':
    import sys
    import cgitb
    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
