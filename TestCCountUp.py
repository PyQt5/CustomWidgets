#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月31日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: TestCCountUp
@description: 
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout,\
    QPushButton

from CustomWidgets.CCountUp import CCountUp


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

Style = """
QLabel, QPushButton {
    font-family: Helvetica Neue,Helvetica,PingFang SC,Hiragino Sans GB,Microsoft YaHei,"\5FAE\8F6F\96C5\9ED1",Arial,sans-serif;
    font-size: 14px;
}
QPushButton {
    font-size: 12px;
}
CCountUp {
    font-size: 24px;
}
"""


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setStyleSheet(Style)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('目标值：1234，持续时间：6秒', self))
        self.countLabel = CCountUp(self)
        self.countLabel.setAlignment(Qt.AlignCenter)
        self.countLabel.setMinimumSize(100, 100)
        self.countLabel.setDuration(6000)  # 动画时间 6 秒
        layout.addWidget(self.countLabel)

        cw = QWidget(self)
        layout.addWidget(cw)
        layoutc = QHBoxLayout(cw)
        layoutc.addWidget(QPushButton(
            '开始', cw, clicked=lambda: self.countLabel.setNum(1234)))
        layoutc.addWidget(QPushButton('重置', cw, clicked=self.countLabel.reset))
        layoutc.addWidget(QPushButton('暂停/继续', cw, clicked=self.doContinue))

        layoutc.addWidget(QPushButton(
            '开始负小数-1234.00', cw, clicked=lambda: self.countLabel.setNum(-1234.00)))

    def doContinue(self):
        if self.countLabel.isPaused():
            self.countLabel.resume()
        else:
            self.countLabel.pause()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
