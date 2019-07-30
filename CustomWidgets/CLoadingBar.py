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
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QProgressBar


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'

Style = """
QProgressBar {
    border: none;
    border-radius: 2px;
    background-color: transparent;
}
QProgressBar::chunk {
    border-radius: 2px;
    background-color: %s;
}
"""


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
        self._height = None
        self._color = None
        self._failedColor = None
        self._direction = None
        self.setOrientation(Qt.Horizontal)
        self.setTextVisible(False)

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
            widget.setStyleSheet(
                Style % (widget._color or CLoadingBar.Color).name())
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
        CLoadingBar.Instances[parent].hide()

    @classmethod
    def error(cls, parent):
        if parent not in CLoadingBar.Instances:
            return
        CLoadingBar.Instances[parent].hide()

    @classmethod
    def update(cls, parent, value):
        if parent in CLoadingBar.Instances:
            widget = CLoadingBar.Instances[parent]
            widget.show()
            widget.setValue(value)
