#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月24日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: TestCDrawer
@description: 
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout,\
    QLineEdit

from CustomWidgets.CDrawer import CDrawer


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class DrawerWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(DrawerWidget, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('DrawerWidget{background:white;}')
        layout = QVBoxLayout(self)
        layout.addWidget(QLineEdit(self))
        layout.addWidget(QPushButton('button', self))


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(400, 300)
        layout = QGridLayout(self)
        layout.addWidget(QPushButton('上', self, clicked=self.doOpenTop), 0, 1)
        layout.addWidget(QPushButton('左', self, clicked=self.doOpenLeft), 1, 0)
        layout.addWidget(QPushButton(
            '右', self, clicked=self.doOpenRight), 1, 2)
        layout.addWidget(QPushButton(
            '下', self, clicked=self.doOpenBottom), 2, 1)

    def doOpenTop(self):
        if not hasattr(self, 'topDrawer'):
            self.topDrawer = CDrawer(self, stretch=0.5, direction=CDrawer.TOP)
            self.topDrawer.setWidget(DrawerWidget(self.topDrawer))
        self.topDrawer.show()

    def doOpenLeft(self):
        if not hasattr(self, 'leftDrawer'):
            self.leftDrawer = CDrawer(self, direction=CDrawer.LEFT)
            self.leftDrawer.setWidget(DrawerWidget(self.leftDrawer))
        self.leftDrawer.show()

    def doOpenRight(self):
        if not hasattr(self, 'rightDrawer'):
            self.rightDrawer = CDrawer(self, widget=DrawerWidget())
            self.rightDrawer.setDirection(CDrawer.RIGHT)
        self.rightDrawer.show()

    def doOpenBottom(self):
        if not hasattr(self, 'bottomDrawer'):
            self.bottomDrawer = CDrawer(
                self, direction=CDrawer.BOTTOM, widget=DrawerWidget())
            self.bottomDrawer.setStretch(0.5)
        self.bottomDrawer.show()


if __name__ == '__main__':
    import sys
    import cgitb
    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
