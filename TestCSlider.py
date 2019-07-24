#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月24日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: TestCSlider
@description: 
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from CustomWidgets.CSlider import CSlider


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('Window{background:gray;}')
        layout = QVBoxLayout(self)
        self.labelValue = QLabel(self)
        layout.addWidget(CSlider(
            Qt.Vertical, self, valueChanged=lambda v: self.labelValue.setText(str(v))))
        layout.addWidget(CSlider(
            Qt.Horizontal, self, valueChanged=lambda v: self.labelValue.setText(str(v))))
        layout.addWidget(self.labelValue)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
