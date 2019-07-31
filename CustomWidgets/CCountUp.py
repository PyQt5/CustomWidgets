#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月31日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: CustomWidgets.CCountUp
@description: 数字动画
"""
from PyQt5.QtCore import QTimeLine, QEasingCurve
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class CCountUp(QLabel):

    def __init__(self, *args, **kwargs):
        super(CCountUp, self).__init__(*args, **kwargs)
        self.isFloat = False        # 是否是小数
        font = self.font() or QFont()
        font.setBold(True)
        self.setFont(font)
        self.timeline = QTimeLine(6000, self)
        self.timeline.setEasingCurve(QEasingCurve.OutExpo)
        self.timeline.frameChanged.connect(self.onFrameChanged)

    def pause(self):
        """暂停
        """
        self.timeline.setPaused(True)

    def resume(self):
        """继续
        """
        self.timeline.resume()

    def isPaused(self):
        """是否暂停
        """
        return self.timeline.state() == QTimeLine.Paused

    def reset(self):
        """重置
        """
        self.timeline.stop()
        self.isFloat = False        # 是否是小数
        self.setText('0')

    def onFrameChanged(self, value):
        if self.isFloat:
            value = round(value / 100.0 + 0.00001, 2)
        value = str(format(value, ','))
        self.setText(value + '0' if value.endswith('.0') else value)

    def setDuration(self, duration):
        """设置动画持续时间
        :param duration:
        """
        self.timeline.setDuration(duration)

    def setNum(self, number):
        """设置数字
        :param number:        int or float
        """
        if isinstance(number, int):
            self.isFloat = False
            self.timeline.setFrameRange(0, number)
        elif isinstance(number, float):
            self.isFloat = True
            self.timeline.setFrameRange(0, number * 100)
        self.timeline.stop()
        self.setText('0')
        self.timeline.start()
