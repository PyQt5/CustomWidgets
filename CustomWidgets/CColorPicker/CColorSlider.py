#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年4月19日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: CustomWidgets.CColorPicker.CColorSlider
@description: 颜色滑动条
"""
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QLinearGradient, QColor, QImage, QPainter,\
    QRadialGradient
from PyQt5.QtWidgets import QSlider, QStyleOptionSlider, QStyle


__Author__ = "Irony"
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class CColorSlider(QSlider):

    TypeAlpha = 0                   # 透明颜色类型
    TypeRainbow = 1                 # 彩虹色

    colorChanged = pyqtSignal(QColor, int)          # 颜色, 透明度

    def __init__(self, types, parent=None, color=Qt.black):
        """
        :param types:                    渐变类型（0-透明，1-彩虹）
        :param parent:
        """
        super(CColorSlider, self).__init__(Qt.Horizontal, parent)
        self.setObjectName('Custom_Color_Slider')
        self.setCursor(Qt.PointingHandCursor)
        self.valueChanged.connect(self.onValueChanged)
        self._types = types
        self._color = color
        self._isFirstShow = True
        self._imageRainbow = None                       # 彩虹背景图
        self._imageAlphaColor = None                    # 带颜色透明图
        self._imageAlphaTmp = None                      # 透明方格
        self._imageAlpha = None                         # 带颜色透明背景和方格合成图
        self._imageCircle = None                        # 圆形滑块图
        self._imageCircleHover = None                   # 圆形滑块悬停图
        self.setToolTip('彩虹色' if self._types == self.TypeRainbow else '透明度')

    def reset(self):
        self.setValue(0 if self._types == self.TypeRainbow else self.maximum())

    def updateAlpha(self, color, alpha):
        self.blockSignals(True)
        self.setValue(alpha)
        self.blockSignals(False)

    def showEvent(self, event):
        super(CColorSlider, self).showEvent(event)
        if self._isFirstShow:
            self._isFirstShow = False
            self.setRange(0, max(1, self.width() - 1))
            if self._types == self.TypeAlpha:
                self.blockSignals(True)
                self.setValue(self.maximum())
                self.blockSignals(False)
            self.gradientCirclePixmap()
            self.gradientPixmap(self._types, self._color)

    def pick(self, pt):
        return pt.x() if self.orientation() == Qt.Horizontal else pt.y()

    def pixelPosToRangeValue(self, pos):
        option = QStyleOptionSlider()
        self.initStyleOption(option)
        gr = self.style().subControlRect(QStyle.CC_Slider,
                                         option, QStyle.SC_SliderGroove, self)
        sr = self.style().subControlRect(QStyle.CC_Slider,
                                         option, QStyle.SC_SliderHandle, self)
        if self.orientation() == Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1
        return QStyle.sliderValueFromPosition(
            self.minimum(), self.maximum(), pos - sliderMin,
            sliderMax - sliderMin, option.upsideDown)

    def mousePressEvent(self, event):
        # 获取上面的拉动块位置
        event.accept()
        option = QStyleOptionSlider()
        self.initStyleOption(option)
        rect = self.style().subControlRect(
            QStyle.CC_Slider, option, QStyle.SC_SliderHandle, self)
        rect.setX(max(min(rect.x(), self.width() - self.height()), 0))
        rect.setWidth(self.height())
        rect.setHeight(self.height())
        center = rect.center() - rect.topLeft()
        self.setSliderPosition(self.pixelPosToRangeValue(
            self.pick(event.pos() - center)))
        self.setSliderDown(True)

    def mouseMoveEvent(self, event):
        event.accept()
        self.setSliderPosition(
            self.pixelPosToRangeValue(self.pick(event.pos())))

    def paintEvent(self, event):
        if not (self._imageRainbow or self._imageAlpha):
            return super(CColorSlider, self).paintEvent(event)

        option = QStyleOptionSlider()
        self.initStyleOption(option)
        # 背景Rect
        groove = self.style().subControlRect(
            QStyle.CC_Slider, option, QStyle.SC_SliderGroove, self)
        groove.adjust(3, 5, -3, -5)
        # 滑块Rect
        handle = self.style().subControlRect(
            QStyle.CC_Slider, option, QStyle.SC_SliderHandle, self)
        handle.setX(max(min(handle.x(), self.width() - self.height()), 0))
        handle.setWidth(self.height())
        handle.setHeight(self.height())
        radius = self.height() / 2
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.drawImage(
            groove, self._imageRainbow if self._imageRainbow else self._imageAlpha)

        if not self._imageCircle or not self._imageCircleHover:
            painter.setBrush(QColor(245, 245, 245) if option.state &
                             QStyle.State_MouseOver else QColor(254, 254, 254))
            painter.drawRoundedRect(handle, radius, radius)
        else:
            painter.drawImage(handle, self._imageCircleHover if option.state &
                              QStyle.State_MouseOver else self._imageCircle)

    def gradientCirclePixmap(self):
        """白色带阴影
        """
        xy = self.height() / 2
        radius = self.height() * 0.8

        # 绘制普通状态下圆形的滑块
        circleColor = QRadialGradient(xy, xy, radius, xy, xy)
        circleColor.setColorAt(0.5, QColor(254, 254, 254))
        circleColor.setColorAt(0.7, QColor(0, 0, 0, 60))
        circleColor.setColorAt(0.7, QColor(0, 0, 0, 30))
        circleColor.setColorAt(0.9, QColor(0, 0, 0, 0))
        self._imageCircle = QImage(
            self.height(), self.height(), QImage.Format_ARGB32)
        self._imageCircle.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(self._imageCircle)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setPen(Qt.NoPen)
        painter.setBrush(circleColor)
        painter.drawRoundedRect(0, 0, self.height(), self.height(), xy, xy)
        painter.end()

        # 绘制悬停状态下圆形的滑块
        circleColorHover = QRadialGradient(xy, xy, radius, xy, xy)
        circleColorHover.setColorAt(0.5, QColor(245, 245, 245))
        circleColorHover.setColorAt(0.7, QColor(0, 0, 0, 30))
        circleColorHover.setColorAt(0.9, QColor(0, 0, 0, 0))
        self._imageCircleHover = QImage(
            self.height(), self.height(), QImage.Format_ARGB32)
        self._imageCircleHover.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(self._imageCircleHover)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setPen(Qt.NoPen)
        painter.setBrush(circleColorHover)
        painter.drawRoundedRect(0, 0, self.height(), self.height(), xy, xy)
        painter.end()

    def gradientPixmap(self, types, color):
        """生成渐变图片
        """
        pixSize = 5
        if types == self.TypeAlpha:
            # 生成黑边相间的模拟透明背景
            if not self._imageAlphaTmp:
                self._imageAlphaTmp = QImage(
                    self.width(), self.height(), QImage.Format_ARGB32)
                painter = QPainter()
                painter.begin(self._imageAlphaTmp)
                painter.setRenderHint(QPainter.Antialiasing, True)
                painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
                for x in range(int(self.width() / pixSize)):
                    for y in range(int(self.height() / pixSize)):
                        _x, _y = x * pixSize, y * pixSize
                        painter.fillRect(_x, _y, pixSize, pixSize,
                                         Qt.white if x % 2 != y % 2 else Qt.darkGray)
                painter.end()
            # 绘制透明渐变
            gradient = QLinearGradient(0, 0, self.width(), 0)
            gradient.setColorAt(0, QColor(0, 0, 0, 0))
            gradient.setColorAt(1, color)
            # 只画渐变颜色
            self._imageAlphaColor = QImage(
                self.width(), self.height(), QImage.Format_ARGB32)
            self._imageAlphaColor.fill(Qt.transparent)
            painter = QPainter()
            painter.begin(self._imageAlphaColor)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
            painter.fillRect(0, 0, self.width(), self.height(), gradient)
            painter.end()
            # 合并方格图
            self._imageAlpha = self._imageAlphaColor.copy()
            painter = QPainter()
            painter.begin(self._imageAlpha)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
            painter.drawImage(0, 0, self._imageAlphaTmp)
            painter.fillRect(0, 0, self.width(), self.height(), gradient)
            painter.end()
        else:
            gradient = QLinearGradient(0, 0, self.width(), 0)
            gradient.setColorAt(0, QColor('#ff0000'))
            gradient.setColorAt(0.17, QColor('#ffff00'))
            gradient.setColorAt(0.33, QColor('#00ff00'))
            gradient.setColorAt(0.5, QColor('#00ffff'))
            gradient.setColorAt(0.67, QColor('#0000ff'))
            gradient.setColorAt(0.83, QColor('#ff00ff'))
            gradient.setColorAt(1, QColor('#ff0000'))
            self._imageRainbow = QImage(
                self.width(), self.height(), QImage.Format_ARGB32)
            painter = QPainter()
            painter.begin(self._imageRainbow)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
            painter.fillRect(0, 0, self.width(), self.height(), gradient)
            painter.end()

    def onValueChanged(self, value):
        hh = int(self.height() / 2)
        color = self.colorFromPoint(value, hh)
        alpha = self.alphaFromPoint(value, hh)
        self.colorChanged.emit(color, alpha)

    def colorFromPoint(self, x, y):
        if not self._imageRainbow:
            return QColor(Qt.red)
        return self._imageRainbow.pixelColor(x, y)

    def alphaFromPoint(self, x, y):
        if not self._imageAlphaColor:
            return 255
        return self._imageAlphaColor.pixelColor(x, y).alpha()


if __name__ == '__main__':
    import sys
    import cgitb
    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
    app = QApplication(sys.argv)
    app.setStyleSheet('Window{background:white;}')
    w = QWidget()
    w.resize(250, 150)
    w.show()

    layout = QVBoxLayout(w)

    slider1 = CColorSlider(CColorSlider.TypeRainbow, w)
    slider1.colorChanged.connect(
        lambda c, a: print('TypeRainbow:', c.name(), a))
    layout.addWidget(slider1)

    slider2 = CColorSlider(CColorSlider.TypeAlpha, w, Qt.black)
    slider2.colorChanged.connect(lambda c, a: print('TypeAlpha:', c.name(), a))
    layout.addWidget(slider2)

    sys.exit(app.exec_())
