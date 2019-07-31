#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月30日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: CustomWidgets.CLoadingBar
@description: 加载条
"""
from PyQt5.QtCore import Qt, QRectF, pyqtProperty, QPropertyAnimation,\
    QEasingCurve
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QProgressBar


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class CLoadingBar(QProgressBar):

    Instances = {}
    Height = 2
    Color = QColor('#2d8cf0')
    FailedColor = QColor('#ed4014')
    # 位置
    TOP = 0
    BOTTOM = 1
    Direction = 0

    def __init__(self, *args, **kwargs):
        super(CLoadingBar, self).__init__(*args, **kwargs)
        self._height = None         # 进度条高度
        self._color = None          # 正常颜色
        self._failedColor = None    # 失败颜色
        self._direction = None      # 进度条位置（上下）
        self._alpha = 255           # 透明度
        self.isError = False        # 是否错误
        self.setOrientation(Qt.Horizontal)
        self.setTextVisible(False)
        self.animation = QPropertyAnimation(
            self, b'alpha', self, loopCount=1, duration=1000)
        self.animation.setEasingCurve(QEasingCurve.SineCurve)
        self.animation.setStartValue(0)
        self.animation.setEndValue(255)

    @pyqtProperty(int)
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, alpha):
        self._alpha = alpha
        QProgressBar.update(self)

    def paintEvent(self, _):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        # 背景
        painter.fillRect(self.rect(), Qt.transparent)
        # 进度块
        ratio = (self.value() - self.minimum()) / \
            (self.maximum() - self.minimum())
        width = self.rect().width() * ratio
        if self.isError:
            color = QColor(self._failedColor or CLoadingBar.FailedColor)
        else:
            color = QColor(self._color or CLoadingBar.Color)
        color.setAlpha(self._alpha)
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRectF(0, 0, width, self.height()), 2, 2)

    def eventFilter(self, obj, event):
        if event.type() == event.Resize:
            # 重新调整大小
            widget = CLoadingBar.Instances.get(obj, None)
            if widget:
                direction = widget._direction or CLoadingBar.Direction
                height = widget._height or CLoadingBar.Height
                widget.setGeometry(
                    0, 0 if direction == CLoadingBar.TOP else obj.height() - height,
                    obj.width(), height
                )
        return super(CLoadingBar, self).eventFilter(obj, event)

    @classmethod
    def config(cls, height=2, direction=0, color='#2d8cf0', failedColor='#ed4014'):
        """全局配置
        :param cls:
        :param height:            进度条高度
        :param direction:         进度条位置
        :param color:             进度条加载颜色
        :param failedColor:       进度条失败颜色
        """
        CLoadingBar.Height = height
        CLoadingBar.Color = QColor(color)
        CLoadingBar.FailedColor = QColor(failedColor)
        CLoadingBar.Direction = direction
        return cls

    @classmethod
    def start(cls, parent, minimum=0, maximum=100, height=None, direction=None, color=None, failedColor=None):
        """创建加载条
        :param cls:
        :param widget:            目标对象
        :param minimum:           进度条最小值
        :param maximum:           进度条最大值
        :param height:            进度条高度
        :param direction:         进度条位置
        :param color:             进度条加载颜色
        :param failedColor:       进度条失败颜色
        """
        if parent not in CLoadingBar.Instances:
            widget = CLoadingBar(parent)
            CLoadingBar.Instances[parent] = widget
            # 对父控件安装事件过滤器
            parent.installEventFilter(widget)
        else:
            widget = CLoadingBar.Instances[parent]
        widget._height = height
        widget._color = color
        widget._failedColor = failedColor
        widget._direction = direction
        widget.setRange(minimum, maximum)
        widget.setValue(minimum)
        direction = widget._direction or CLoadingBar.Direction
        height = widget._height or CLoadingBar.Height
        widget.setGeometry(
            0, 0 if direction == CLoadingBar.TOP else parent.height() - height,
            parent.width(), height
        )

    @classmethod
    def finish(cls, parent):
        if parent not in CLoadingBar.Instances:
            return
        widget = CLoadingBar.Instances[parent]
        widget._alpha = 255
        widget.isError = False
        widget.setValue(widget.maximum())
        widget.animation.start()

    @classmethod
    def error(cls, parent):
        if parent not in CLoadingBar.Instances:
            return
        widget = CLoadingBar.Instances[parent]
        widget._alpha = 255
        widget.isError = True
        widget.setValue(widget.maximum())
        widget.animation.start()

    @classmethod
    def update(cls, parent, value):
        if parent in CLoadingBar.Instances:
            widget = CLoadingBar.Instances[parent]
            widget._alpha = 255
            widget.isError = False
            widget.show()
            widget.setValue(value)
