#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年4月20日
@author: Irony
@site: https://pyqt5.com https://github.com/PyQt5
@email: 892768447@qq.com
@file: CustomWidgets.CColorPicker.CColorPanel
@description: 饱和度面板
"""
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QPainter, QLinearGradient, QColor, QImage, QPen,\
    QPainterPath
from PyQt5.QtWidgets import QWidget


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019 "
__Version__ = "Version 1.0"


class CColorPanel(QWidget):

    colorChanged = pyqtSignal(QColor)

    def __init__(self, *args, color=Qt.red, **kwargs):
        super(CColorPanel, self).__init__(*args, **kwargs)
        self._color = QColor(color)
        self._image = None
        self._imagePointer = None       # 小圆环
        self._pointerPos = None         # 小圆环位置
        self._createPointer()

    def reset(self):
        self.blockSignals(True)
        self._color = QColor(Qt.red)
        self._pointerPos = self.rect().topRight() - QPoint(6, 6)
        self.update()
        self.blockSignals(False)

    def _createPointer(self):
        # 绘制一个小圆环
        self._imagePointer = QImage(12, 12, QImage.Format_ARGB32)
        self._imagePointer.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(self._imagePointer)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.addRoundedRect(0, 0, 12, 12, 6.0, 6.0)
        painter.setClipPath(path)
        painter.drawRoundedRect(0, 0, 12, 12, 6.0, 6.0)
        painter.end()

    def mousePressEvent(self, event):
        # 鼠标按下更新小圆环位置
        super(CColorPanel, self).mousePressEvent(event)
        self._pointerPos = event.pos()
        if self._image:
            self.colorChanged.emit(self._image.pixelColor(
                max(min(self._pointerPos.x(), self.width() - 1), 0),
                max(min(self._pointerPos.y(), self.height() - 1), 0)
            ))
        self._pointerPos -= QPoint(6, 6)
        self.update()

    def mouseMoveEvent(self, event):
        # 小圆环随鼠标移动
        super(CColorPanel, self).mouseMoveEvent(event)
        self._pointerPos = event.pos()
        self._pointerPos.setX(max(min(self._pointerPos.x(), self.width()), 0))
        self._pointerPos.setY(max(min(self._pointerPos.y(), self.height()), 0))
        if self._image:
            self.colorChanged.emit(self._image.pixelColor(
                max(min(self._pointerPos.x(), self.width() - 1), 0),
                max(min(self._pointerPos.y(), self.height() - 1), 0)
            ))
        self._pointerPos -= QPoint(6, 6)
        self.update()

    def paintEvent(self, event):
        super(CColorPanel, self).paintEvent(event)
        if self._image:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
            painter.drawImage(self.rect(), self._image)
            painter.setPen(QColor(240, 240, 240))
            painter.drawRect(self.rect())
            if self._pointerPos:
                painter.setPen(Qt.NoPen)
                painter.drawImage(self._pointerPos, self._imagePointer)

    def showEvent(self, event):
        super(CColorPanel, self).showEvent(event)
        # 右上角
        if not self._pointerPos:
            self._pointerPos = self.rect().topRight() - QPoint(6, 6)

    def resizeEvent(self, event):
        super(CColorPanel, self).resizeEvent(event)
        self.createImage(self._color)

    def createImage(self, color, alpha=255):
        self._color = QColor(color)
        self._color.setAlpha(255)
        self._image = QImage(self.size(), QImage.Format_ARGB32)

        painter = QPainter()
        painter.begin(self._image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        # 背景色
        painter.fillRect(self.rect(), color)
        # 白色渐变
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, Qt.white)
        gradient.setColorAt(1, QColor.fromHslF(0.055, 0.42, 0.65, 0))
        painter.fillRect(self.rect(), gradient)
        # 黑色渐变
        gradient = QLinearGradient(0, self.height(), 0, 0)
        gradient.setColorAt(1, QColor.fromHslF(0.055, 0.42, 0.65, 0))
        gradient.setColorAt(0, Qt.black)
        painter.fillRect(self.rect(), gradient)
        painter.end()

        self.update()

        if self._image and self._pointerPos:
            self.colorChanged.emit(self._image.pixelColor(
                max(min(self._pointerPos.x(), self.width() - 1), 0),
                max(min(self._pointerPos.y(), self.height() - 1), 0)
            ))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = CColorPanel(color=Qt.blue)
    w.resize(224, 120)
    w.colorChanged.connect(lambda c: print('color:', c.name()))
    w.show()
    sys.exit(app.exec_())
