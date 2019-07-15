#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月15日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: CTitleBar.CTitleBar
@description: 自定义标题栏
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWindowStateChangeEvent, QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QLabel, QPushButton


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class CTitleBar(QWidget):

    Radius = 38

    def __init__(self, *args, title='', **kwargs):
        super(CTitleBar, self).__init__(*args, **kwargs)
        self.setupUi()
        # 支持设置背景
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.mPos = None
        # 找到父控件(或者自身)
        self._root = self.window()  # self.parent() or self

        self.labelTitle.setText(title)
        self.buttonNormal.setVisible(False)
        # 是否需要隐藏最小化或者最大化按钮
        self.buttonMinimum.setVisible(
            self.testWindowFlags(Qt.WindowMinimizeButtonHint))
        self.buttonMaximum.setVisible(
            self.testWindowFlags(Qt.WindowMaximizeButtonHint))

        # 绑定信号
        self.buttonMinimum.clicked.connect(self._root.showMinimized)
        self.buttonMaximum.clicked.connect(self._root.showMaximized)
        self.buttonNormal.clicked.connect(self._root.showNormal)
        self.buttonClose.clicked.connect(self._root.close)
        # 对父控件(或者自身)安装事件过滤器
        self._root.installEventFilter(self)

    def eventFilter(self, target, event):
        if isinstance(event, QWindowStateChangeEvent):
            if self._root.isVisible() and not self._root.isMinimized() and \
                    self.testWindowFlags(Qt.WindowMinMaxButtonsHint):
                # 如果当前是最大化则隐藏最大化按钮
                maximized = self._root.isMaximized()
                self.buttonMaximum.setVisible(not maximized)
                self.buttonNormal.setVisible(maximized)
                # 修复最大化边距空白问题
                if maximized:
                    self._oldMargins = self._root.layout().getContentsMargins()
                    self._root.layout().setContentsMargins(0, 0, 0, 0)
                elif hasattr(self, '_oldMargins'):
                    self._root.layout().setContentsMargins(*self._oldMargins)
        return super(CTitleBar, self).eventFilter(target, event)

    def mouseDoubleClickEvent(self, event):
        """双击标题栏最大化
        :param event:
        """
        if not self.testWindowFlags(Qt.WindowMinMaxButtonsHint):
            return
        if self._root.isMaximized():
            self._root.showNormal()
        else:
            self._root.showMaximized()

    def mousePressEvent(self, event):
        """鼠标按下记录坐标
        :param event:
        """
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()

    def mouseReleaseEvent(self, event):
        """鼠标释放删除坐标
        :param event:
        """
        self.mPos = None

    def mouseMoveEvent(self, event):
        """鼠标移动移动窗口
        :param event:
        """
        if self._root.isMaximized():
            return
        if event.buttons() == Qt.LeftButton and self.mPos:
            pos = event.pos() - self.mPos
            self._root.move(self._root.pos() + pos)

    def testWindowFlags(self, windowFlags):
        """判断当前窗口是否有该flags
        :param windowFlags:
        """
        return bool(self._root.windowFlags() & windowFlags)

    def setWindowTitle(self, title):
        """设置标题
        :param title:
        """
        self.labelTitle.setText(title)

    def setupUi(self):
        """创建UI
        """
        self.setMinimumSize(0, self.Radius)
        self.setMaximumSize(16777215, self.Radius)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addItem(QSpacerItem(
            114, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))
        layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        # 标题
        self.labelTitle = QLabel(self, alignment=Qt.AlignCenter)
        self.labelTitle.setObjectName('CTitleBar_labelTitle')
        layout.addWidget(self.labelTitle)
        layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        # 最小化,最大化,还原,关闭按钮
        for name, text in (('buttonMinimum', '0'), ('buttonMaximum', '1'),
                           ('buttonNormal', '2'), ('buttonClose', 'r')):
            button = QPushButton(text, self, font=QFont('Webdings'))
            button.setMinimumSize(self.Radius, self.Radius)
            button.setMaximumSize(self.Radius, self.Radius)
            button.setObjectName('CTitleBar_%s' % name)
            setattr(self, name, button)
            layout.addWidget(button)
