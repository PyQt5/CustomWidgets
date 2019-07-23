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
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSpacerItem, QSizePolicy,\
    QPushButton


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

# 扁平样式
FlatStyle = """
CPaginationBar > QPushButton {
    border: none;
    qproperty-minimumSize: 36px 36px;
    qproperty-maximumSize: 36px 36px;
    font-weight: 500;
    font-size: 16px;
}
CPaginationBar > QPushButton:hover {
    color: #409eff;
}
CPaginationBar > QPushButton:disabled {
    color: #409eff;
}
#CPaginationBar_buttonPrevious:disabled, #CPaginationBar_buttonNext:disabled {
    color: #c0c4cc;
}
"""

# 普通样式
Style = """
CPaginationBar > QPushButton {
    border: 1px solid #dcdee2;
    border-radius: 4px;
    qproperty-minimumSize: 36px 36px;
    qproperty-maximumSize: 36px 36px;
    font-weight: 500;
    font-size: 16px;
}
CPaginationBar > QPushButton:hover {
    color: #409eff;
    border-color: #409eff;
}
CPaginationBar > QPushButton:disabled {
    color: #409eff;
    border-color: #409eff;
}
#CPaginationBar_buttonPrevious:disabled, #CPaginationBar_buttonNext:disabled {
    color: #c0c4cc;
    border-color: #c0c4cc;
}
"""


class CPaginationBar(QWidget):

    pageChanged = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        totalPages = kwargs.pop('totalPages', 0)
        super(CPaginationBar, self).__init__(*args, **kwargs)
        self.currentPage = 1
        self.totalPages = 0
        self._buttons = []
        self.setupUi()
        if totalPages > 0 and isinstance(totalPages, int):
            self.setTotalPages(totalPages)

    def getCurrentPage(self):
        """得到当前页
        """
        return self.currentPage

    def setCurrentPage(self, currentPage):
        """设置当前页
        :param currentPage:
        """
        if self.currentPage > self.totalPages:
            currentPage = 1
        self.currentPage = currentPage

    def setTotalPages(self, totalPages):
        """设置总页数，后需要重新安排按钮
        :param totalPages:
        """
        if totalPages < 1:
            totalPages = 1
        if self.totalPages == totalPages:
            return
        self.totalPages = totalPages
        if self.currentPage > totalPages:
            self.currentPage = 1
        self.previousPage = -1
        self.totalButtons = 7  # 总的按钮个数
        self._clearButtons()

        layout = self.layout()
        # 左侧拉伸占位
        layout.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # 添加上一页按钮
        self.buttonPrevious.setVisible(totalPages > 1)
        layout.addWidget(self.buttonPrevious)

        if self.totalButtons > totalPages:
            self.totalButtons = totalPages

        self._initButtons()

        # 添加下一页按钮
        self.buttonNext.setVisible(totalPages > 1)
        self.buttonNext.setEnabled(totalPages > 1)
        layout.addWidget(self.buttonNext)

        # 右侧拉伸占位
        layout.addItem(QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self._calculate()

    def _initButtons(self):
        # 初始化按钮
        for i in range(self.totalButtons):
            button = QPushButton(self)
            pageNumber = -1
            if self.totalPages >= self.totalButtons + 1:
                if i == 0:
                    button.setProperty('page', 1)
                    pageNumber = 1
                elif i == self.totalButtons - 1:
                    button.setProperty('page', self.totalPages)
                    pageNumber = self.totalPages
                else:
                    if i <= 4:
                        pageNumber = i + 1
            else:
                pageNumber = i + 1

            button.setProperty('page', pageNumber)
            button.setText(str(pageNumber) if pageNumber > 0 else '...')
            self.layout().addWidget(button)
            self._buttons.append(button)
            button.clicked.connect(self._doButtonTurning)

    def _clearButtons(self):
        """清空按钮
        """
        layout = self.layout()
        self._buttons.clear()
        for _ in range(layout.count()):
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                if widget == self.buttonPrevious:
                    self.buttonPrevious = widget
                elif widget == self.buttonNext:
                    self.buttonNext = widget
                else:
                    widget.deleteLater()
                    del widget
            del item

    def _updateButton(self, index, pageNumber):
        """更新按钮的文本和属性
        :param index:
        :param pageNumber:
        """
        button = self._buttons[index]
        button.setText(str(pageNumber) if pageNumber > 0 else '...')
        button.setProperty('page', pageNumber)

    def _calculate(self):
        """重新计算并更新按钮
        """
        if self.totalPages > self.totalButtons:
            button1 = False
            button5 = False
            if self.currentPage - 1 > 3:
                button1 = True
                self._updateButton(1, -2)
            else:
                self._updateButton(1, 2)
                self._updateButton(2, 3)
                self._updateButton(3, 4)
                self._updateButton(4, 5)

            if self.totalPages - self.currentPage > 3:
                button5 = True
                self._updateButton(5, -1)
            else:
                self._updateButton(2, self.totalPages - 4)
                self._updateButton(3, self.totalPages - 3)
                self._updateButton(4, self.totalPages - 2)
                self._updateButton(5, self.totalPages - 1)

            if button1 and button5:
                self._updateButton(2, self.currentPage - 1)
                self._updateButton(3, self.currentPage)
                self._updateButton(4, self.currentPage + 1)

        for button in self._buttons:
            page = button.property('page')
            button.setEnabled(self.currentPage != page)
            button.setCursor(
                Qt.PointingHandCursor if button.isEnabled() else Qt.ArrowCursor)

        self.buttonPrevious.setEnabled(self.currentPage > 1)
        self.buttonNext.setEnabled(self.currentPage < self.totalPages)

        # 这里ForbiddenCursor不会生效,这可能是一个Bug,当按钮不可用时忽略了鼠标样式
        self.buttonPrevious.setCursor(
            Qt.PointingHandCursor if self.buttonPrevious.isEnabled() else Qt.ForbiddenCursor)
        self.buttonNext.setCursor(
            Qt.PointingHandCursor if self.buttonNext.isEnabled() else Qt.ForbiddenCursor)

    def _doButtonTurning(self):
        """按钮点击切换
        """
        pageNumber = self.sender().property('page')
        newCurrentPage = self.currentPage

        if pageNumber > 0:
            newCurrentPage = pageNumber
        elif pageNumber == -1:
            newCurrentPage = self.currentPage + 3
        elif pageNumber == -2:
            newCurrentPage = self.currentPage - 3

        if newCurrentPage < 1:
            newCurrentPage = 1
        elif newCurrentPage > self.totalPages:
            newCurrentPage = self.totalPages

        self.previousPage = self.currentPage
        self.currentPage = newCurrentPage
        self._calculate()
        self.pageChanged.emit(self.currentPage)

    def _doPageTurning(self):
        """上、下一页按钮
        """
        self.previousPage = self.currentPage
        if self.sender() == self.buttonPrevious:
            self.currentPage -= 1
        elif self.sender() == self.buttonNext:
            self.currentPage += 1
        self._calculate()
        self.pageChanged.emit(self.currentPage)

    def setupUi(self):
        # 横向布局
        layout = QHBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(0, 0, 0, 0)
        # 上一页按钮
        self.buttonPrevious = QPushButton(
            '<', self, enabled=False, visible=False, clicked=self._doPageTurning,
            objectName='CPaginationBar_buttonPrevious')
        # 下一页按钮
        self.buttonNext = QPushButton(
            '>', self, enabled=False, visible=False, clicked=self._doPageTurning,
            objectName='CPaginationBar_buttonNext')
