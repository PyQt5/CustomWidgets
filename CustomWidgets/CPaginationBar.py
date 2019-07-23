#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月23日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: CustomWidgets.CPaginationBar
@description: 分页条
"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSpacerItem, QSizePolicy,\
    QPushButton


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class CPaginationBar(QWidget):

    onPageChanged = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super(CPaginationBar, self).__init__(*args, **kwargs)
        self.previousPage = -1
        self.currentPage = 1
        self.totalPages = 0
        self._totalButtons = 7  # 总的按钮个数
        self.setupUi()

    def setTotalPages(self, totalPages):
        """设置总页数，后需要重新安排按钮
        :param totalPages:
        """
        if self.totalPages == totalPages:
            return
        self.totalPages = totalPages
        self.currentPage = 1
        self._clearButtons()
        
        layout = self.layout()
        # 左侧拉伸占位
        layout.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Preferred))
        
        if totalPages > 1:
            # 添加上一页按钮
            self.buttonPrevious.setVisible(True)
            layout.addWidget(self.buttonPrevious)
        
        if self._totalButtons > totalPages:
            self._totalButtons = totalPages
        
        self._initButtons()
        
        if totalPages > 1:
            # 添加下一页按钮
            self.buttonNext.setVisible(True)
            self.buttonNext.setEnabled(True)
            layout.addWidget(self.buttonNext)
        
        # 右侧拉伸占位
        layout.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Preferred))

        self._calculate()
    
    def _initButtons(self):
        # 初始化按钮
        for i in range(self._totalButtons):
            button = QPushButton(self)
            pageNumber = -1
            if self.totalPages >= self._totalButtons+1:
                pass

    def _clearButtons(self):
        """清空中间的按钮
        """
        layout = self.layout()
        for _ in range(layout.count()):
            child = layout.takeAt(0)
            if not child:
                break
            widget = child.widget()
            del child
            if widget and (widget != self.buttonPrevious or widget != self.buttonPrevious):
                widget.deleteLater()
                del widget

    def _calculate(self):
        pass

    def _doPageTurning(self):
        """上、下一页按钮
        """
        self.previousPage = self.currentPage
        if self.sender() == self.buttonPrevious:
            self.currentPage -= 1
        elif self.sender() == self.buttonNext:
            self.currentPage += 1
        self._calculate()
        self.onPageChanged.emit(self.currentPage)

    def setupUi(self):
        # 横向布局
        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        # 上一页按钮
        self.buttonPrevious = QPushButton(
            '<', self, enabled=False, visible=False, clicked=self._doPageTurning,
            objectName='CPaginationBar_buttonPrevious')
        # 下一页按钮
        self.buttonNext = QPushButton(
            '>', self, enabled=False, visible=False, clicked=self._doPageTurning,
            objectName='CPaginationBar_buttonNext')
