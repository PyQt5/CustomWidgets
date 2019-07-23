#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年4月19日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: CustomWidgets.CColorPicker.CColorPicker
@description: 
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget,\
    QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy,\
    QHBoxLayout, QPushButton

from CustomWidgets.CColorPicker.CColorControl import CColorControl
from CustomWidgets.CColorPicker.CColorInfos import CColorInfos
from CustomWidgets.CColorPicker.CColorPalettes import CColorPalettes
from CustomWidgets.CColorPicker.CColorPanel import CColorPanel
from CustomWidgets.CColorPicker.CColorSlider import CColorSlider
from CustomWidgets.CColorPicker.CColorStraw import CColorStraw


__Author__ = "Irony"
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

Stylesheet = """
QLineEdit, QLabel, QTabWidget {
    font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Oxygen,Ubuntu,Cantarell,Fira Sans,Droid Sans,Helvetica Neue,sans-serif;
}
#Custom_Color_View {
    background: white;
    border-radius: 3px;
}
CColorPalettes {
    min-width: 322px;
    max-width: 322px;
    max-height: 120px;
}
CColorPanel {
    min-height: 160px;
    max-height: 160px;
}
CColorControl {
    min-width: 50px;
    max-width: 50px;
    min-height: 50px;
    max-height: 50px;
}

#editHex {
    min-width: 75px;
}

#splitLine {
    min-height: 1px;
    max-height: 1px;
    background: #e2e2e2;
}

QLineEdit, QSpinBox {
    border: 1px solid #cbcbcb;
    border-radius: 2px;
    background: white;
    min-width: 31px;
    min-height: 21px;
}
QLineEdit:focus, QSpinBox:focus {
    border-color: rgb(139, 173, 228);
}
QLabel {
    color: #a9a9a9;
}
QPushButton {
    border: 1px solid #cbcbcb;
    border-radius: 2px;
    min-width: 21px;
    max-width: 21px;
    min-height: 21px;
    max-height: 21px;
    font-size: 14px;
    background: white;
}
QPushButton:hover {
    border-color: rgb(139, 173, 228);
}
QPushButton:pressed {
    border-color: #cbcbcb;
}

CColorStraw {
    border: none;
    font-size: 18px;
    border-radius: 0px;
}
QPushButton:hover {
    color: rgb(139, 173, 228);
}
QPushButton:pressed {
    color: #cbcbcb;
}

#confirmButton, #cancelButton {
    min-width: 70px;
    min-height: 30px;
}
#cancelButton:hover {
    border-color: rgb(255, 133, 0);
}

QTabWidget::pane {
    border: none;
}
QTabBar::tab {
    padding: 3px 6px;
    color: rgb(100, 100, 100);
    background: transparent;
}
QTabBar::tab:hover {
    color: black;
}
QTabBar::tab:selected {
    color: rgb(139, 173, 228);
    border-bottom: 2px solid rgb(139, 173, 228);
}

QTabBar::tab:!selected {
    border-bottom: 2px solid transparent;
}

QScrollBar:vertical {
    max-width: 10px;
    border: none;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:vertical {
    background: rgb(220, 220, 220);
    border: 1px solid rgb(207, 207, 207);
    border-radius: 5px;
}
"""


class CColorPicker(QDialog):

    selectedColor = QColor()

    def __init__(self, *args, **kwargs):
        super(CColorPicker, self).__init__(*args, **kwargs)
        self.setObjectName('Custom_Color_Dialog')
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet(Stylesheet)
        self.mPos = None
        self.initUi()
        self.initSignals()
        # 添加阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(10)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)

    def initUi(self):
        layout = QVBoxLayout(self)
        self.colorView = QWidget(self)
        self.colorView.setObjectName('Custom_Color_View')
        layout.addWidget(self.colorView)

        # 内部布局
        layout = QVBoxLayout(self.colorView)
        layout.setContentsMargins(1, 1, 1, 1)

        # 面板
        self.colorPanel = CColorPanel(self.colorView)
        layout.addWidget(self.colorPanel)

        self.controlWidget = QWidget(self.colorView)
        layout.addWidget(self.controlWidget)
        clayout = QHBoxLayout(self.controlWidget)

        # 取色器
        self.colorStraw = CColorStraw(self.colorView)
        clayout.addWidget(self.colorStraw)
        # 小圆
        self.colorControl = CColorControl(self.colorView)
        clayout.addWidget(self.colorControl)

        self.sliderWidget = QWidget(self.colorView)
        clayout.addWidget(self.sliderWidget)
        slayout = QVBoxLayout(self.sliderWidget)
        slayout.setContentsMargins(0, 0, 0, 0)
        # 滑动条
        self.rainbowSlider = CColorSlider(
            CColorSlider.TypeRainbow, self.colorView)
        slayout.addWidget(self.rainbowSlider)
        self.alphaSlider = CColorSlider(CColorSlider.TypeAlpha, self.colorView)
        slayout.addWidget(self.alphaSlider)

        # 信息
        self.colorInfos = CColorInfos(self.colorView)
        layout.addWidget(self.colorInfos)

        # 分割线
        layout.addWidget(QWidget(self.colorView, objectName='splitLine'))

        # 底部色板
        self.colorPalettes = CColorPalettes(self.colorView)
        layout.addWidget(self.colorPalettes)

        # 确定取消按钮
        self.confirmWidget = QWidget(self.colorView)
        clayout = QHBoxLayout(self.confirmWidget)
        clayout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        clayout.addWidget(QPushButton(
            '确定', self, clicked=self.accept, objectName='confirmButton'))
        clayout.addWidget(QPushButton(
            '取消', self, clicked=self.reject, objectName='cancelButton'))
        layout.addWidget(self.confirmWidget)

    def initSignals(self):
        # 彩虹slider->面板->rgb文字->小圆
        self.rainbowSlider.colorChanged.connect(self.colorPanel.createImage)
        self.colorPanel.colorChanged.connect(self.colorInfos.updateColor)
        self.colorInfos.colorChanged.connect(self.colorControl.updateColor)

        # 透明slider->alpha文字->小圆
        self.alphaSlider.colorChanged.connect(self.colorInfos.updateAlpha)

        # alpha文字->透明slider
#         self.colorInfos.colorChanged.connect(self.alphaSlider.updateAlpha)

        # 底部多颜色卡
        self.colorPalettes.colorChanged.connect(self.colorInfos.updateColor)
        self.colorPalettes.colorChanged.connect(self.colorPanel.createImage)
        self.colorInfos.colorAdded.connect(self.colorPalettes.addColor)

        # 取色器
        self.colorStraw.colorChanged.connect(self.colorInfos.updateColor)

        # 颜色结果
        self.colorInfos.colorChanged.connect(self.setColor)

    def setColor(self, color, alpha):
        color = QColor(color)
        color.setAlpha(alpha)
        CColorPicker.selectedColor = color

#     def reset(self):
#         CColorPicker.selectedColor = QColor()
#         self.colorPalettes.reset()
#         self.colorPanel.reset()
#         self.colorControl.reset()
#         self.rainbowSlider.reset()
#         self.alphaSlider.reset()
#         self.colorInfos.reset()

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        '''鼠标弹起事件'''
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mPos:
            if not self.colorPanel.geometry().contains(self.mPos):
                self.move(self.mapToGlobal(event.pos() - self.mPos))
        event.accept()

    @classmethod
    def getColor(cls, parent=None):
        """获取选择的颜色
        :param cls:
        :param parent:
        """
        if not hasattr(cls, '_colorPicker'):
            cls._colorPicker = CColorPicker(parent)
        ret = cls._colorPicker.exec_()
        if ret != QDialog.Accepted:
            return ret, QColor()
        return ret, CColorPicker.selectedColor


def test():
    import sys
    import cgitb
    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication, QLabel
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


if __name__ == '__main__':
    test()
