#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月23日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: TestCPaginationBar
@description: 
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from CustomWidgets.CPaginationBar import CPaginationBar


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.pageLabel = QLabel('当前页: 1', self, alignment=Qt.AlignCenter)
        self.paginationBar = CPaginationBar(self)
        layout.addWidget(self.pageLabel)
        layout.addWidget(self.paginationBar)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
