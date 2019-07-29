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

from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QFontDatabase, QIcon, QIconEngine, QPixmap, QPainter,\
    QFont


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'
__Version__ = 'Version 1.0'

FontCache = {}


class CFontIcon:

    def __init__(self, ttfFile, mapFile):
        """
        :param ttfFile:            ttf字体文件路径
        :param mapFile:            ttf字体文件对应的字符映射 json格式
        """
        if ttfFile in FontCache:
            return FontCache[ttfFile]
        fontId = QFontDatabase.addApplicationFont(ttfFile)
        fontFamilies = QFontDatabase.applicationFontFamilies(fontId)
        if fontFamilies:
            self.font = QFont(fontFamilies[0])
            self.fontMap = json.loads(open(mapFile, 'rb').read().decode(
                encoding='utf_8', errors='ignore'), encoding='utf_8', object_hook=self.object_hook)
            FontCache[ttfFile] = self
        else:
            self.font = QFont()
            self.fontMap = {}

    @classmethod
    def fontAwesome(cls):
        """FontAwesome字体
        :param cls:
        """
        dirPath = os.path.dirname(__file__)
        return CFontIcon(
            os.path.join(dirPath, 'Fonts', 'fontawesome-webfont.ttf'),
            os.path.join(dirPath, 'Fonts', 'fontawesome-webfont.json'),
        )

    @classmethod
    def fontMaterial(cls):
        """material字体
        :param cls:
        """
        dirPath = os.path.dirname(__file__)
        return CFontIcon(
            os.path.join(dirPath, 'Fonts', 'materialdesignicons-webfont.ttf'),
            os.path.join(dirPath, 'Fonts', 'materialdesignicons-webfont.json'),
        )

    def icon(self, name, color=Qt.black):
        if name not in self.fontMap:
            return QIcon()
        return QIcon(CIconEngine(self.font, self.fontMap[name], color))

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


class CIconEngine(QIconEngine):

    def __init__(self, font, text, color, *args, **kwargs):
        super(CIconEngine, self).__init__(*args, **kwargs)
        self.font = font
        self.text = text
        self.color = color

    def paint(self, painter, rect, mode, state):
        painter.save()
        painter.setPen(self.color)
        self.font.setPixelSize(round(0.875 * min(rect.width(), rect.height())))
        painter.setFont(self.font)
        painter.drawText(
            rect, int(Qt.AlignCenter | Qt.AlignVCenter), self.text)
        painter.restore()

    def pixmap(self, size, mode, state):
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)
        self.paint(QPainter(pixmap), QRect(QPoint(0, 0), size), mode, state)
        return pixmap
