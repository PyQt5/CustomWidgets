#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月16日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: CustomWidgets.CFramelessBase
@description: 无边框窗口
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QEnterEvent
from PyQt5.QtWidgets import QWidget, QDialog


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'

LEFT = 1
TOP = 2
RIGHT = 4
BOTTOM = 8
LEFTTOP = LEFT | TOP
RIGHTTOP = RIGHT | TOP
LEFTBOTTOM = LEFT | BOTTOM
RIGHTBOTTOM = RIGHT | BOTTOM


class CFramelessBase:

    Margins = 4
    BaseClass = QWidget

    def __init__(self, *args, **kwargs):
        super(CFramelessBase, self).__init__(*args, **kwargs)
        self.dragParams = {'type': 0, 'x': 0,
                           'y': 0, 'margin': 0, 'draging': False}
        self.originalCusor = None
        self.setMouseTracking(True)
        # 设置背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 设置无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

    def isResizable(self):
        """是否可调整
        """
        return self.minimumSize() != self.maximumSize()

    def getEdge(self, pos):
        """返回点与边距接触的边的方向
        :param pos:
        """
        rect = self.rect()
        edge = 0
        if not self.isResizable():
            return edge
        if pos.x() <= rect.left() + self.Margins:
            edge |= LEFT
        elif pos.x() >= rect.right() - self.Margins:
            edge |= RIGHT
        if pos.y() <= rect.top() + self.Margins:
            edge |= TOP
        elif pos.y() >= rect.bottom() - self.Margins:
            edge |= BOTTOM
        return edge

    def adjustCursor(self, edge):
        """根据边方向调整光标样式
        :param edge:
        """
        cursor = None
        if edge in (TOP, BOTTOM):
            cursor = Qt.SizeVerCursor
        elif edge in (LEFT, RIGHT):
            cursor = Qt.SizeHorCursor
        elif edge in (LEFT | TOP, RIGHT | BOTTOM):
            cursor = Qt.SizeFDiagCursor
        elif edge in (TOP | RIGHT, BOTTOM | LEFT):
            cursor = Qt.SizeBDiagCursor
        if cursor and cursor != self.cursor():
            self.setCursor(cursor)

    def eventFilter(self, obj, event):
        """事件过滤器,用于解决鼠标进入其它控件后还原为标准鼠标样式
        """
        if isinstance(event, QEnterEvent):
            self.setCursor(self.originalCusor or Qt.ArrowCursor)
        return self.BaseClass.eventFilter(self, obj, event)

    def paintEvent(self, event):
        """由于是全透明背景窗口,重绘事件中绘制透明度为1的难以发现的边框,用于调整窗口大小
        """
        self.BaseClass.paintEvent(self, event)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 1), 2 * self.Margins))
        painter.drawRect(self.rect())

    def showEvent(self, event):
        """第一次显示时设置控件的layout的边距
        :param event:
        """
        layout = self.layout()
        if self.originalCusor == None and layout:
            self.originalCusor = self.cursor()
            layout.setContentsMargins(
                self.Margins, self.Margins, self.Margins, self.Margins)
            # 对所有子控件增加事件过滤器
            for w in self.children():
                if isinstance(w, QWidget):
                    w.installEventFilter(self)
        self.BaseClass.showEvent(self, event)

    def mousePressEvent(self, event):
        """鼠标按下设置标志
        :param event:
        """
        if not self.isResizable() or self.childAt(event.pos()):
            return
        self.dragParams['x'] = event.x()
        self.dragParams['y'] = event.y()
        self.dragParams['globalX'] = event.globalX()
        self.dragParams['globalY'] = event.globalY()
        self.dragParams['width'] = self.width()
        self.dragParams['height'] = self.height()
        if event.button() == Qt.LeftButton and self.dragParams['type'] != 0 \
                and not self.isMaximized() and not self.isFullScreen():
            self.dragParams['draging'] = True

    def mouseReleaseEvent(self, event):
        """释放鼠标还原光标样式
        :param event:
        """
        self.dragParams['draging'] = False
        self.dragParams['type'] = 0

    def mouseMoveEvent(self, event):
        """鼠标移动用于设置鼠标样式或者调整窗口大小
        :param event:
        """
        if self.isMaximized() or self.isFullScreen() or not self.isResizable():
            return

        # 判断鼠标类型
        cursorType = self.dragParams['type']
        if not self.dragParams['draging']:
            cursorType = self.dragParams['type'] = self.getEdge(event.pos())
            self.adjustCursor(cursorType)

        # 判断窗口拖动
        if self.dragParams['draging']:
            x = self.x()
            y = self.y()
            width = self.width()
            height = self.height()

            if cursorType & TOP == TOP:
                y = event.globalY() - self.dragParams['margin']
                height = self.dragParams['height'] + \
                    self.dragParams['globalY'] - event.globalY()
            if cursorType & BOTTOM == BOTTOM:
                height = self.dragParams['height'] - \
                    self.dragParams['globalY'] + event.globalY()
            if cursorType & LEFT == LEFT:
                x = event.globalX() - self.dragParams['margin']
                width = self.dragParams['width'] + \
                    self.dragParams['globalX'] - event.globalX()
            if cursorType & RIGHT == RIGHT:
                width = self.dragParams['width'] - \
                    self.dragParams['globalX'] + event.globalX()

            minw = self.minimumWidth()
            maxw = self.maximumWidth()
            minh = self.minimumHeight()
            maxh = self.maximumHeight()
            if width < minw or width > maxw or height < minh or height > maxh:
                return

            self.setGeometry(x, y, width, height)


class CFramelessWidget(QWidget, CFramelessBase):

    BaseClass = QWidget


class CFramelessDialog(QDialog, CFramelessBase):

    BaseClass = QDialog
