#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年4月21日
@author: Irony
@site: https://pyqt5.com https://github.com/PyQt5
@email: 892768447@qq.com
@file: CustomWidgets.CColorPicker.CColorControl
@description: 
"""
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtWidgets import QWidget


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019 "
__Version__ = "Version 1.0"


class CColorControl(QWidget):

    colorChanged = pyqtSignal(QColor)

    def __init__(self, *args, color=Qt.red, **kwargs):
        super(CColorControl, self).__init__(*args, **kwargs)
        self._alpha = 255
        self._color = QColor(color)
        self.colorChanged.emit(self._color)

    def updateColor(self, color, alpha=255):
        self._color = QColor(color)
        self.colorChanged.emit(self._color)
        self._color.setAlpha(alpha)
        self.update()

    def reset(self):
        self.updateColor(Qt.red)

    def paintEvent(self, event):
        super(CColorControl, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setPen(Qt.NoPen)

        # 变换圆心
        painter.translate(self.rect().center())

        # 画背景方格图
        painter.save()
        # 保证方格在前景圆内部
        diameter = min(self.width(), self.height()) - 8
        radius = diameter / 2
        path = QPainterPath()
        path.addRoundedRect(-radius, -radius, diameter,
                            diameter, radius, radius)
        painter.setClipPath(path)

        pixSize = 5
        for x in range(int(self.width() / pixSize)):
            for y in range(int(self.height() / pixSize)):
                _x, _y = x * pixSize, y * pixSize
                painter.fillRect(_x - radius, _y - radius, pixSize, pixSize,
                                 Qt.white if x % 2 != y % 2 else Qt.darkGray)
        painter.restore()

        # 画前景颜色
        diameter = min(self.width(), self.height()) - 4
        radius = diameter / 2
        path = QPainterPath()
        path.addRoundedRect(-radius, -radius, diameter,
                            diameter, radius, radius)
        painter.setClipPath(path)

        painter.setBrush(self._color)
        painter.drawRoundedRect(-radius, -radius,
                                diameter, diameter, radius, radius)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = CColorControl()
    w.resize(200, 200)
    w.show()
    sys.exit(app.exec_())
