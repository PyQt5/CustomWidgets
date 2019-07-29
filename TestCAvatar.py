#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月26日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: TestCAvatar
@description: 
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from CustomWidgets.CAvatar import CAvatar


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        # 没有头像
        layout.addWidget(CAvatar(self))
        # 路径错误
        layout.addWidget(CAvatar(self, url='test.jpg'))
        # 本地三种尺寸头像
        layout.addWidget(CAvatar(
            self, shape=CAvatar.Circle, url='TestData/example-1.jpg', size=CAvatar.SizeSmall))
        layout.addWidget(CAvatar(
            self, shape=CAvatar.Circle, url='TestData/example-2.jpg'))
        layout.addWidget(CAvatar(
            self, shape=CAvatar.Rectangle, url='TestData/example-3.jpg', size=CAvatar.SizeLarge))

        # 网络头像
        layout.addWidget(CAvatar(
            self, shape=CAvatar.Rectangle, url='https://www.thiswaifudoesnotexist.net/example-1000.jpg', size=CAvatar.SizeSmall))
        layout.addWidget(CAvatar(
            self, shape=CAvatar.Circle, url='https://www.thiswaifudoesnotexist.net/example-1001.jpg'))
        # 假装路径错误
        layout.addWidget(CAvatar(
            self, shape=CAvatar.Rectangle, url='https://www.thiswaifudoesnotexist.net/example.jpg', size=CAvatar.SizeLarge))


if __name__ == '__main__':
    import sys
    import cgitb
    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
