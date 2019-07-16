#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月16日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: CFramelessWidget.CFramelessWidget
@description: 无边框窗口
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QRegion, QEnterEvent
from PyQt5.QtWidgets import QWidget


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'

OUTSIDE = 0
LEFT = 1
TOP = 2
RIGHT = 4
BOTTOM = 8


class CFramelessWidget(QWidget):

    Margins = 4

    def __init__(self, *args, **kwargs):
        super(CFramelessWidget, self).__init__(*args, **kwargs)
        self.dragging = False
        self.dragpos = None
        self.dragedge = 0
        self.originalCusor = None
        self.setMouseTracking(True)
        # 设置背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 设置无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

    def getEdge(self, pos):
        """返回点与边距接触的边的方向
        :param pos:
        """
        rect = self.rect()
        edge = 0
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
        return super(CFramelessWidget, self).eventFilter(obj, event)

    def paintEvent(self, event):
        """由于是全透明背景窗口,重绘事件中绘制透明度为1的难以发现的边框,用于调整窗口大小
        """
        super(CFramelessWidget, self).paintEvent(event)
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
        super(CFramelessWidget, self).showEvent(event)

    def mousePressEvent(self, event):
        """鼠标按下设置标志
        :param event:
        """
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.dragpos = event.pos()
            self.dragedge = self.getEdge(event.pos())

    def mouseReleaseEvent(self, event):
        """释放鼠标还原光标样式
        :param event:
        """
        if self.dragging and event.button() == Qt.LeftButton:
            self.dragging = False

    def mouseMoveEvent(self, event):
        """鼠标移动用于设置鼠标样式或者调整窗口大小
        :param event:
        """
        if self.isMaximized() or self.isFullScreen():
            return
        if self.dragging:
            # 拖动调整大小
            pos = event.pos() - self.dragpos
            self.dragpos = event.pos()
            geometry = self.geometry().adjusted(
                pos.x() if self.dragedge & LEFT else 0,
                pos.y() if self.dragedge & TOP else 0,
                pos.x() if self.dragedge & RIGHT else 0,
                pos.y() if self.dragedge & BOTTOM else 0
            )
            if geometry.isValid() and geometry.width() > self.minimumWidth() \
                    and geometry.height() > self.minimumHeight() and not geometry.contains(event.pos()):
                print(geometry.contains(event.pos()), geometry,
                      event.pos(), self.minimumSize())
                self.setGeometry(geometry)
            return
        radius = self.Margins - 1
        rect = self.rect().adjusted(radius, radius, -radius, -radius)
        region = QRegion(self.rect()).subtracted(QRegion(rect))
        if not region.contains(event.pos()):
            # 鼠标不在可调整区域则需要还原光标样式
            self.setCursor(self.originalCusor)
        else:
            self.dragedge = self.getEdge(event.pos())
            self.adjustCursor(self.dragedge)
