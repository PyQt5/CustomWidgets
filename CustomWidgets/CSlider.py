#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月24日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: CustomWidgets.CSlider
@description: 滑块
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QStyleOptionSlider, QStyle


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0

# 普通样式
Style = """
/*横向*/
QSlider:horizontal {
    min-height: 60px;
}
QSlider::groove:horizontal {
    height: 2px;
    background: white;
}
QSlider::handle:horizontal {
    width: 30px;
    margin: 0 -6px;
    margin-top: -15px;
    margin-bottom: -15px;
    border-radius: 15px;
    background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.5 rgba(255, 255, 255, 255), stop:0.6 rgba(255, 255, 255, 100), stop:0.61 rgba(255, 255, 255, 0));
}
QSlider::handle:horizontal:hover {
    background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.40113 rgba(255, 255, 255, 255), stop:0.502825 rgba(44, 167, 248, 255), stop:0.59887 rgba(44, 167, 248, 100), stop:0.61 rgba(44, 167, 248, 0));
}
QSlider::add-page:horizontal {
    background: white;
}

QSlider::sub-page:horizontal {
    background: rgb(44, 167, 248);
}
/*竖向*/
QSlider:vertical {
    min-width: 60px;
}
QSlider::groove:vertical {
    width: 2px;
    background: white; 
}
QSlider::handle:vertical {
    height: 30px;
    margin: -6px 0;
    margin-left: -15px;
    margin-right: -15px;
    border-radius: 15px;
    background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.5 rgba(255, 255, 255, 255), stop:0.6 rgba(255, 255, 255, 100), stop:0.61 rgba(255, 255, 255, 0));
}
QSlider::handle:vertical:hover {
    background: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.40113 rgba(255, 255, 255, 255), stop:0.502825 rgba(44, 167, 248, 255), stop:0.59887 rgba(44, 167, 248, 100), stop:0.61 rgba(44, 167, 248, 0));
}
QSlider::add-page:vertical {
    background: white;
}

QSlider::sub-page:vertical {
    background: rgb(44, 167, 248);
}
"""


class CSlider(QSlider):

    def __init__(self, *args, **kwargs):
        super(CSlider, self).__init__(*args, **kwargs)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(Style)

    def mousePressEvent(self, event):
        # 获取上面的拉动块位置
        option = QStyleOptionSlider()
        self.initStyleOption(option)
        rect = self.style().subControlRect(
            QStyle.CC_Slider, option, QStyle.SC_SliderHandle, self)
        if rect.contains(event.pos()):
            # 如果鼠标点击的位置在滑块上则交给Qt自行处理
            super(CSlider, self).mousePressEvent(event)
            return
        if self.orientation() == Qt.Horizontal:
            # 横向，要考虑invertedAppearance是否反向显示的问题
            self.setValue(self.style().sliderValueFromPosition(
                self.minimum(), self.maximum(),
                event.x() if not self.invertedAppearance() else (self.width(
                ) - event.x()), self.width()))
        else:
            # 纵向
            self.setValue(self.style().sliderValueFromPosition(
                self.minimum(), self.maximum(),
                (self.height() - event.y()) if not self.invertedAppearance(
                ) else event.y(), self.height()))
