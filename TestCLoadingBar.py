#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月30日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: TestCLoadingBar
@description: 
"""

from PyQt5.QtCore import QTimeLine
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from CustomWidgets.CLoadingBar import CLoadingBar


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(600, 200)
        layout = QVBoxLayout(self)

        # 配置全局属性（也可以通过start方法里的参数配置单独的属性）
        CLoadingBar.config(
            height=2, direction=CLoadingBar.TOP,
            color='#2d8cf0', failedColor='#ed4014')

        # 子控件顶部进度
        self.widget1 = QWidget(self)
        layout.addWidget(self.widget1)
        CLoadingBar.start(self.widget1, color='#19be6b', failedColor='#ff9900')

        widget = QWidget(self)
        layoutc = QHBoxLayout(widget)
        layoutc.addWidget(QPushButton('开始', self, clicked=self.doStart))
        layoutc.addWidget(QPushButton('结束', self, clicked=self.doFinish))
        layoutc.addWidget(QPushButton('错误', self, clicked=self.doError))
        layout.addWidget(widget)

        # 子控件底部进度
        self.widget2 = QWidget(self)
        layout.addWidget(self.widget2)
        CLoadingBar.start(self.widget2, direction=CLoadingBar.BOTTOM, height=6)

        # 模拟进度
        self.updateTimer = QTimeLine(
            10000, self, frameChanged=self.doUpdateProgress)
        self.updateTimer.setFrameRange(0, 100)
        # 设置数字变化曲线模拟进度的不规则变化
        self.updateTimer.setCurveShape(QTimeLine.EaseInOutCurve)

    def doStart(self):
        """模拟开始
        """
        self.updateTimer.stop()
        self.updateTimer.start()

    def doFinish(self):
        """模拟结束
        """
        self.updateTimer.stop()
        CLoadingBar.finish(self.widget1)
        CLoadingBar.finish(self.widget2)

    def doError(self):
        """模拟出错
        """
        self.updateTimer.stop()
        CLoadingBar.error(self.widget1)
        CLoadingBar.error(self.widget2)

    def doUpdateProgress(self, value):
        """模拟进度值变化
        :param value:
        """
        CLoadingBar.update(self.widget1, value)
        CLoadingBar.update(self.widget2, value)
        if value == 100:
            self.updateTimer.stop()
            self.doFinish()


if __name__ == '__main__':
    import sys
    import cgitb
    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
