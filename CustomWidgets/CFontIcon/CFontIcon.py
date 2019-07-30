#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月28日
@author: Irony
@site: https://pyqt5.com https://github.com/PyQt5
@email: 892768447@qq.com
@file: CustomWidgets.CFontIcon
@description: 字体图标
"""
import json
import os

from PyQt5.QtCore import Qt, QPoint, QRect, QTimer
from PyQt5.QtGui import QFontDatabase, QIcon, QIconEngine, QPixmap, QPainter,\
    QFont


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'
__Version__ = 'Version 1.0'


class CIconEngine(QIconEngine):
    """图标绘制引擎
    """

    def __init__(self, font, *args, **kwargs):
        super(CIconEngine, self).__init__(*args, **kwargs)
        self.font = font
        self.icon = None

    def setIcon(self, icon):
        self.icon = icon

    def paint(self, painter, rect, mode, state):
        painter.save()
        self.font.setPixelSize(round(0.875 * min(rect.width(), rect.height())))
        painter.setFont(self.font)
        if self.icon:
            if self.icon.animation:
                self.icon.animation.paint(painter, rect)
            ms = self.icon._getMode(mode) * self.icon._getState(state)
            text, color = self.icon.icons.get(ms, (None, None))
            if text == None and color == None:
                return
            painter.setPen(color)
            self.text = text if text else self.text
            painter.drawText(
                rect, int(Qt.AlignCenter | Qt.AlignVCenter), self.text)
        painter.restore()

    def pixmap(self, size, mode, state):
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)
        self.paint(QPainter(pixmap), QRect(QPoint(0, 0), size), mode, state)
        return pixmap


class CIconAnimationSpin:

    def __init__(self, parent, interval=10, step=4):
        self.parent = parent
        self.angle = 0
        self.timer = None
        self.interval = interval
        self.step = step

    def update(self):
        if self.angle >= 360:
            self.angle = 0
        self.angle += self.step
        self.parent.update()

    def paint(self, painter, rect):
        if not self.timer:
            self.timer = QTimer(self.parent, timeout=self.update)
            self.timer.start(self.interval)
        else:
            x_center = rect.width() * 0.5
            y_center = rect.height() * 0.5
            painter.translate(x_center, y_center)
            painter.rotate(self.angle)
            painter.translate(-x_center, -y_center)


class CIcon(QIcon):

    # New Mode
    Normal = int(QIcon.Normal) + 2
    Disabled = int(QIcon.Disabled) + 2
    Active = int(QIcon.Active) + 2
    Selected = int(QIcon.Selected) + 2

    # New State
    Off = int(QIcon.Off) + 6
    On = int(QIcon.On) + 6

    def __init__(self, engine, fontMap, animation=None):
        super(CIcon, self).__init__(engine)
        engine.setIcon(self)
        self.animation = animation
        self.fontMap = fontMap
        self.icons = {}
        self.modestate = [m * s for m in [
            self.Normal, self.Disabled, self.Active, self.Selected] for s in [self.Off, self.On]]

    def setAnimation(self, animation):
        self.animation = animation

    def add(self, name, color=Qt.black, mode=QIcon.Normal, state=QIcon.Off):
        """添加或者更新一个指定mode和state的字体和颜色
        :param name:
        :param color:
        :param mode:
        :param state:
        """
        ms = self._getMode(mode) * self._getState(state)
        self.icons[ms] = [self.fontMap.get(name, ''), color]
        return self

    def _getMode(self, mode):
        """修改QIcon::Mode值+2，比如
        QIcon::Normal    0          ->        2
        QIcon::Disabled    1        ->        3
        QIcon::Active    2          ->        4
        QIcon::Selected    3        ->        5
        :param mode:
        """
        return int(mode) + 2

    def _getState(self, state):
        """修改QIcon::State值+6，比如
        QIcon::Off    1             ->        7
        QIcon::On    0              ->        6
        :param state:
        """
        return int(state) + 6


class CIconLoader:
    """字体图标加载器
    """

    def __init__(self, ttfFile, mapFile):
        """
        :param ttfFile:            ttf字体文件路径
        :param mapFile:            ttf字体文件对应的字符映射 json格式
        """
        fontId = QFontDatabase.addApplicationFont(ttfFile)
        fontFamilies = QFontDatabase.applicationFontFamilies(fontId)
        if fontFamilies:
            self._font = QFont(fontFamilies[0])
            self.fontMap = json.loads(open(mapFile, 'rb').read().decode(
                encoding='utf_8', errors='ignore'), encoding='utf_8', object_hook=self.object_hook)
        else:
            self._font = QFont()
            self.fontMap = {}

    @classmethod
    def fontAwesome(cls):
        """FontAwesome字体
        :param cls:
        """
        dirPath = os.path.dirname(__file__)
        return cls(
            os.path.join(dirPath, 'Fonts', 'fontawesome-webfont.ttf'),
            os.path.join(dirPath, 'Fonts', 'fontawesome-webfont.json'),
        )

    @classmethod
    def fontMaterial(cls):
        """material字体
        :param cls:
        """
        dirPath = os.path.dirname(__file__)
        return cls(
            os.path.join(dirPath, 'Fonts', 'materialdesignicons-webfont.ttf'),
            os.path.join(dirPath, 'Fonts', 'materialdesignicons-webfont.json'),
        )

    def icon(self, name, animation=None):
        """根据键值返回一个字体图标
        :param name:
        """
        return CIcon(CIconEngine(self._font), self.fontMap, animation).add(name)

    @property
    def font(self):
        return self._font

    def value(self, name):
        """返回对应的字符
        :param name:
        """
        return self.fontMap.get(name, '')

    def object_hook(self, obj):
        result = {}
        for key in obj:
            result[key] = chr(int(obj[key], 16))
        return result
