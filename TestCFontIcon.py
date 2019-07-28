#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月28日
@author: Irony
@site: https://pyqt5.com https://github.com/PyQt5
@email: 892768447@qq.com
@file: TestCFontIcon
@description: 
"""
import json

from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLineEdit, QListView,\
    QMainWindow, QStatusBar

from CustomWidgets.CFontIcon.CFontIcon import CFontIcon


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'
__Version__ = 'Version 1.0'


class MaterialWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(MaterialWidget, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        layout.addWidget(
            QLineEdit(self, textChanged=self.doFilter, placeholderText='过滤...'))
        # Material Font
        self.listView = QListView(self)
        self.listView.setMouseTracking(True)
        self.listView.setViewMode(QListView.IconMode)
        self.listView.setMovement(QListView.Static)
        self.listView.setFlow(QListView.LeftToRight)
        self.listView.setWrapping(True)
        self.listView.setEditTriggers(QListView.NoEditTriggers)
        self.listView.setResizeMode(QListView.Adjust)
        self.listView.doubleClicked.connect(self.onDoubleClicked)
        self.dmodel = QStandardItemModel(self.listView)
        self.fmodel = QSortFilterProxyModel(self.listView)
        self.fmodel.setSourceModel(self.dmodel)
        self.fmodel.setFilterRole(Qt.ToolTipRole)
        self.listView.setModel(self.fmodel)
        layout.addWidget(self.listView)

        # 字体
        icon = CFontIcon.fontMaterial()

        # 添加Item
        fontMap = json.loads(open(
            'CustomWidgets/CFontIcon/Fonts/materialdesignicons-webfont.json', 'rb').read().decode(
            encoding='utf_8', errors='ignore'), encoding='utf_8')
        for name, _ in fontMap.items():
            item = QStandardItem(icon.icon(name), '')
            item.setData(name, Qt.ToolTipRole)
            item.setData(name, Qt.StatusTipRole)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(item.flags())
            self.dmodel.appendRow(item)

    def doFilter(self, _):
        self.fmodel.setFilterRegExp(self.sender().text())

    def onDoubleClicked(self, index):
        text = index.data(Qt.ToolTipRole)
        if text:
            print(text)


class Window(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.tabWidget = QTabWidget(self)
        self.setCentralWidget(self.tabWidget)
        self.setStatusBar(QStatusBar(self))
        self.tabWidget.addTab(MaterialWidget(self.tabWidget), 'Material Font')


if __name__ == '__main__':
    import sys
    import cgitb
    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
