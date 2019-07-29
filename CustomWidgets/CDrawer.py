#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月24日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: CustomWidgets.CDrawer
@description: 
"""
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QPointF
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QApplication


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class CDrawer(QWidget):

    LEFT, TOP, RIGHT, BOTTOM = range(4)

    def __init__(self, *args, stretch=1 / 3, direction=0, widget=None, **kwargs):
        super(CDrawer, self).__init__(*args, **kwargs)
        self.setWindowFlags(self.windowFlags(
        ) | Qt.FramelessWindowHint | Qt.Popup | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 进入动画
        self.animIn = QPropertyAnimation(
            self, duration=500, easingCurve=QEasingCurve.OutCubic)
        self.animIn.setPropertyName(b'pos')
        # 离开动画
        self.animOut = QPropertyAnimation(
            self, duration=500, finished=self.onAnimOutEnd,
            easingCurve=QEasingCurve.OutCubic)
        self.animOut.setPropertyName(b'pos')
        self.animOut.setDuration(500)
        self.setStretch(stretch)        # 占比
        self.direction = direction      # 方向
        # 半透明背景
        self.alphaWidget = QWidget(
            self, objectName='CDrawer_alphaWidget',
            styleSheet='#CDrawer_alphaWidget{background:rgba(55,55,55,100);}')
        self.alphaWidget.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setWidget(widget)          # 子控件

    def resizeEvent(self, event):
        self.alphaWidget.resize(self.size())
        super(CDrawer, self).resizeEvent(event)

    def mousePressEvent(self, event):
        pos = event.pos()
        if pos.x() >= 0 and pos.y() >= 0 and self.childAt(pos) == None and self.widget:
            if not self.widget.geometry().contains(pos):
                self.animationOut()
                return
        super(CDrawer, self).mousePressEvent(event)

    def show(self):
        super(CDrawer, self).show()
        parent = self.parent().window() if self.parent() else self.window()
        if not parent or not self.widget:
            return
        # 设置Drawer大小和主窗口一致
        self.setGeometry(parent.geometry())
        geometry = self.geometry()
        self.animationIn(geometry)

    def animationIn(self, geometry):
        """进入动画
        :param geometry:
        """
        if self.direction == self.LEFT:
            # 左侧抽屉
            self.widget.setGeometry(
                0, 0, int(geometry.width() * self.stretch), geometry.height())
            self.widget.hide()
            self.animIn.setStartValue(QPoint(-self.widget.width(), 0))
            self.animIn.setEndValue(QPoint(0, 0))
            self.animIn.start()
            self.widget.show()
        elif self.direction == self.TOP:
            # 上方抽屉
            self.widget.setGeometry(
                0, 0, geometry.width(), int(geometry.height() * self.stretch))
            self.widget.hide()
            self.animIn.setStartValue(QPoint(0, -self.widget.height()))
            self.animIn.setEndValue(QPoint(0, 0))
            self.animIn.start()
            self.widget.show()
        elif self.direction == self.RIGHT:
            # 右侧抽屉
            width = int(geometry.width() * self.stretch)
            self.widget.setGeometry(
                geometry.width() - width, 0, width, geometry.height())
            self.widget.hide()
            self.animIn.setStartValue(QPoint(self.width(), 0))
            self.animIn.setEndValue(
                QPoint(self.width() - self.widget.width(), 0))
            self.animIn.start()
            self.widget.show()
        elif self.direction == self.BOTTOM:
            # 下方抽屉
            height = int(geometry.height() * self.stretch)
            self.widget.setGeometry(
                0, geometry.height() - height, geometry.width(), height)
            self.widget.hide()
            self.animIn.setStartValue(QPoint(0, self.height()))
            self.animIn.setEndValue(
                QPoint(0, self.height() - self.widget.height()))
            self.animIn.start()
            self.widget.show()

    def animationOut(self):
        """离开动画
        """
        self.animIn.stop()  # 停止进入动画
        geometry = self.widget.geometry()
        if self.direction == self.LEFT:
            # 左侧抽屉
            self.animOut.setStartValue(geometry.topLeft())
            self.animOut.setEndValue(QPoint(-self.widget.width(), 0))
            self.animOut.start()
        elif self.direction == self.TOP:
            # 上方抽屉
            self.animOut.setStartValue(QPoint(0, geometry.y()))
            self.animOut.setEndValue(QPoint(0, -self.widget.height()))
            self.animOut.start()
        elif self.direction == self.RIGHT:
            # 右侧抽屉
            self.animOut.setStartValue(QPoint(geometry.x(), 0))
            self.animOut.setEndValue(QPoint(self.width(), 0))
            self.animOut.start()
        elif self.direction == self.BOTTOM:
            # 下方抽屉
            self.animOut.setStartValue(QPoint(0, geometry.y()))
            self.animOut.setEndValue(QPoint(0, self.height()))
            self.animOut.start()

    def onAnimOutEnd(self):
        """离开动画结束
        """
        # 模拟点击外侧关闭
        QApplication.sendEvent(self, QMouseEvent(
            QMouseEvent.MouseButtonPress, QPointF(-1, -1), Qt.LeftButton, Qt.NoButton, Qt.NoModifier))

    def setWidget(self, widget):
        """设置子控件
        :param widget:
        """
        self.widget = widget
        if widget:
            widget.setParent(self)
            self.animIn.setTargetObject(widget)
            self.animOut.setTargetObject(widget)

    def setEasingCurve(self, easingCurve):
        """设置动画曲线
        :param easingCurve:
        """
        self.animIn.setEasingCurve(easingCurve)

    def getStretch(self):
        """获取占比
        """
        return self.stretch

    def setStretch(self, stretch):
        """设置占比
        :param stretch:
        """
        self.stretch = max(0.1, min(stretch, 0.9))

    def getDirection(self):
        """获取方向
        """
        return self.direction

    def setDirection(self, direction):
        """设置方向
        :param direction:
        """
        direction = int(direction)
        if direction < 0 or direction > 3:
            direction = self.LEFT
        self.direction = direction
