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
        layout.addWidget(CAvatar(shape=CAvatar.Circle,
                                 url='TestData/example-1.jpg'))
        layout.addWidget(CAvatar(shape=CAvatar.Rectangle,
                                 url='TestData/example-2.jpg'))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
