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
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtWidgets import QWidget


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class CDrawer(QWidget):

    LEFT, TOP, RIGHT, BOTTOM = range(4)

    def __init__(self, *args, stretch=1 / 3, direction=0, **kwargs):
        super(CDrawer, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.Popup)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStretch(stretch)        # 占比
        self.direction = direction      # 方向
        self.animation = QPropertyAnimation(self, b'geometry', self)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.setDuration(500)

    def show(self):
        super(CDrawer, self).show()
        parent = self.parent().window() if self.parent() else self.window()
        if not parent:
            return
        geometry = parent.geometry()
        if self.direction == self.LEFT:
            startGeometry = QRect(
                geometry.x(), geometry.y(), 0, geometry.height())
            endGeometry = QRect(geometry.x(), geometry.y(), int(
                geometry.width() * self.stretch), geometry.height())
            self.setGeometry(endGeometry)
            self.animation.setStartValue(startGeometry)
            self.animation.setEndValue(endGeometry)
        elif self.direction == self.TOP:
            self.setGeometry(geometry.x(), geometry.y(), geometry.width(), int(
                geometry.height() * self.stretch))

        elif self.direction == self.RIGHT:
            width = int(geometry.width() * self.stretch)
            self.setGeometry(geometry.x() + geometry.width() - width,
                             geometry.y(), width, geometry.height())

        elif self.direction == self.BOTTOM:
            height = int(geometry.height() * self.stretch)
            self.setGeometry(geometry.x(), geometry.y() + geometry.height() -
                             height, geometry.width(), height)

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
