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

from PyQt5.QtCore import Qt, QSortFilterProxyModel, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLineEdit, QListView,\
    QMainWindow, QStatusBar, QToolButton, QGridLayout, QLabel, QPushButton

from CustomWidgets.CFontIcon.CFontIcon import CFontIcon


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'
__Version__ = 'Version 1.0'


class FontViewWidget(QWidget):

    def __init__(self, statusBar, config, *args, **kwargs):
        super(FontViewWidget, self).__init__(*args, **kwargs)
        self.statusBar = statusBar
        layout = QVBoxLayout(self)
        self.retButton = QToolButton(self)
        self.retButton.setIconSize(QSize(60, 60))
        self.retButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.retButton.setMinimumSize(200, 100)
        self.retButton.setMaximumSize(200, 100)
        layout.addWidget(self.retButton)
        # 过滤输入框
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
        self.listView.entered.connect(self.onEntered)
        self.dmodel = QStandardItemModel(self.listView)
        self.fmodel = QSortFilterProxyModel(self.listView)
        self.fmodel.setSourceModel(self.dmodel)
        self.fmodel.setFilterRole(Qt.ToolTipRole)
        self.listView.setModel(self.fmodel)
        layout.addWidget(self.listView)

        # 字体
        icon = config[0]

        # 添加Item
        fontMap = json.loads(open(config[1], 'rb').read().decode(
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

    def onEntered(self, index):
        index = self.fmodel.mapToSource(index)
        text = index.data(Qt.ToolTipRole)
        if text:
            self.retButton.setText(text)
            self.retButton.setIcon(self.dmodel.itemFromIndex(index).icon())

    def onDoubleClicked(self, index):
        index = self.fmodel.mapToSource(index)
        text = index.data(Qt.ToolTipRole)
        if text:
            QApplication.clipboard().setText(text)
            self.statusBar.showMessage('已复制: %s' % text)


class ButtonsWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(ButtonsWidget, self).__init__(*args, **kwargs)
        layout = QGridLayout(self)
        layout.addWidget(QLabel('Normal', self), 0, 0)
        layout.addWidget(QPushButton('Normal', self), 0, 1)
        layout.addWidget(QLabel('Disabled', self), 1, 0)
        layout.addWidget(QPushButton('Disabled', self, enabled=False), 1, 1)
        layout.addWidget(QLabel('Active', self), 2, 0)
        layout.addWidget(QPushButton('Active', self), 2, 1)
        layout.addWidget(QLabel('Selected', self), 3, 0)
        layout.addWidget(QPushButton('Selected', self,
                                     checkable=True, checked=True), 3, 1)


class Window(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.tabWidget = QTabWidget(self)
        self.setCentralWidget(self.tabWidget)
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage('双击复制')
        self.tabWidget.addTab(FontViewWidget(
            self.statusBar(),
            [
                CFontIcon.fontMaterial(),
                'CustomWidgets/CFontIcon/Fonts/materialdesignicons-webfont.json'
            ],
            self.tabWidget), 'Material Font')
        self.tabWidget.addTab(FontViewWidget(
            self.statusBar(),
            [
                CFontIcon.fontAwesome(),
                'CustomWidgets/CFontIcon/Fonts/fontawesome-webfont.json'
            ],
            self.tabWidget), 'Awesome Font')
        self.tabWidget.addTab(ButtonsWidget(self.tabWidget), '按钮状态')


if __name__ == '__main__':
    import sys
    import cgitb
    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
