#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月16日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: TestCFramelessWidget
@description: 
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLineEdit

from CFramelessWidget.CFramelessWidget import CFramelessWidget
from CTitleBar.CTitleBar import CTitleBar


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class TestCFramelessWidget(CFramelessWidget):

    def __init__(self, *args, **kwargs):
        super(TestCFramelessWidget, self).__init__(*args, **kwargs)
        self.resize(500, 400)
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        # 添加自定义标题栏
        layout.addWidget(CTitleBar(self, title='CTitleBar'))
        layout.addWidget(QLineEdit(self))
        # 底部空白占位
        layout.addWidget(
            QWidget(self, objectName='bottomWidget', cursor=Qt.PointingHandCursor))


# 标题栏样式
Style = """
/*标题栏颜色*/
CTitleBar {
    background: rgb(65, 148, 216);
}

/*标题栏圆角*/
CTitleBar {
    border-top-right-radius: 5px;
    border-top-left-radius: 5px;
}

#CTitleBar_buttonClose {
    /*需要把右侧的关闭按钮考虑进去*/
    border-top-right-radius: 5px;
}

/*底部圆角和背景*/
#bottomWidget {
    background: white;
    border-bottom-right-radius: 5px;
    border-bottom-left-radius: 5px;
}

/*最小化、最大化、还原按钮*/
CTitleBar > QPushButton {
    background: transparent;
}
CTitleBar > QPushButton:hover {
    background: rgba(0, 0, 0, 30);
}
CTitleBar > QPushButton:pressed {
    background: rgba(0, 0, 0, 60);
}

/*关闭按钮*/
#CTitleBar_buttonClose:hover {
    color: white;
    background: rgb(232, 17, 35);
}
#CTitleBar_buttonClose:pressed {
    color: white;
    background: rgb(165, 69, 106);
}
"""

if __name__ == '__main__':
    import sys
    import cgitb
    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(Style)
    w = TestCFramelessWidget()
    w.show()
    sys.exit(app.exec_())
