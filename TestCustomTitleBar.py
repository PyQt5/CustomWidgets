#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月15日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: TestCustomTitleBar
@description: 
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from CustomTitleBar.CustomTitleBar import CustomTitleBar


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class TestWidgetTitle(QWidget):

    def __init__(self, *args, **kwargs):
        super(TestWidgetTitle, self).__init__(*args, **kwargs)
        self.resize(500, 400)
        # 设置背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 设置无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        # 添加自定义标题栏
        layout.addWidget(CustomTitleBar(self, title='CustomTitleBar'))
        # 底部空白占位
        layout.addWidget(QWidget(self, objectName='bottomWidget'))


# 标题栏样式
Style = """
/*标题栏颜色*/
CustomTitleBar {
    background: rgb(65, 148, 216);
}

/*标题栏圆角*/
CustomTitleBar {
    border-top-right-radius: 10px;
    border-top-left-radius: 10px;
}

#CustomTitleBar_buttonClose {
    /*需要把右侧的关闭按钮考虑进去*/
    border-top-right-radius: 10px;
}

/*底部圆角和背景*/
#bottomWidget {
    background: white;
    border-bottom-right-radius: 10px;
    border-bottom-left-radius: 10px;
}

/*最小化、最大化、还原按钮*/
CustomTitleBar > QPushButton {
    background: transparent;
}
CustomTitleBar > QPushButton:hover {
    background: rgba(0, 0, 0, 30);
}
CustomTitleBar > QPushButton:pressed {
    background: rgba(0, 0, 0, 60);
}

/*关闭按钮*/
#CustomTitleBar_buttonClose:hover {
    color: white;
    background: rgb(232, 17, 35);
}
#CustomTitleBar_buttonClose:pressed {
    color: white;
    background: rgb(165, 69, 106);
}
"""

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(Style)
    w = TestWidgetTitle()
    w.show()
    sys.exit(app.exec_())
