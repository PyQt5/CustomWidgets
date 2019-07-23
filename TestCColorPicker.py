#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年4月25日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: TestCColorPicker
@description: 
"""
__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'

import cgitb
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QWidget, QVBoxLayout,\
    QPushButton

from CustomWidgets.CColorPicker.CColorPicker import CColorPicker


sys.excepthook = cgitb.enable(1, None, 5, '')
app = QApplication(sys.argv)


def getColor():
    ret, color = CColorPicker.getColor()
    if ret == QDialog.Accepted:
        r, g, b, a = color.red(), color.green(), color.blue(), color.alpha()
        label.setText('color: rgba(%d, %d, %d, %d)' % (r, g, b, a))
        label.setStyleSheet(
            'background: rgba(%d, %d, %d, %d);' % (r, g, b, a))


window = QWidget()
window.resize(200, 200)
layout = QVBoxLayout(window)
label = QLabel('', window, alignment=Qt.AlignCenter)
button = QPushButton('点击选择颜色', window, clicked=getColor)
layout.addWidget(label)
layout.addWidget(button)
window.show()

sys.exit(app.exec_())
