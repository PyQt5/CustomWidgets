#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年4月21日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: CustomWidgets.CColorPicker.CColorPalettes
@description: 
"""
from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTabWidget

from CustomWidgets.CColorPicker.CColorItems import CColorItems


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'

MaterialColors = [
    '#F44336', '#E91E63', '#9C27B0', '#673AB7',
    '#3F51B5', '#2196F3', '#03A9F4', '#00BCD4',
    '#009688', '#4CAF50', '#8BC34A', '#CDDC39',
    '#FFEB3B', '#FFC107', '#FF9800', '#FF5722',
    '#795548', '#9E9E9E', '#607D8B',
]

FlatColors = [
    '#1ABC9C', '#2ECC71', '#3498DB', '#9B59B6',
    '#34495E', '#16A085', '#27AE60', '#2980B9',
    '#8E44AD', '#2C3E50', '#F1C40F', '#E67E22',
    '#E74C3C', '#ECF0F1', '#95A5A6', '#F39C12',
    '#D35400', '#C0392B', '#BDC3C7', '#7F8C8D',
]

FluentColors = [
    '#FFB900', '#E74856', '#0078D7', '#0099BC',
    '#7A7574', '#767676', '#FF8C00', '#E81123',
    '#0063B1', '#2D7D9A', '#5D5A58', '#4C4A48',
    '#F7630C', '#EA005E', '#8E8CD8', '#00B7C3',
    '#68768A', '#69797E', '#CA5010', '#C30052',
    '#6B69D6', '#038387', '#515C6B', '#4A5459',
    '#DA3B01', '#E3008C', '#8764B8', '#00B294',
    '#567C73', '#647C64', '#EF6950', '#BF0077',
    '#744DA9', '#018574', '#486860', '#525E54',
    '#D13438', '#C239B3', '#B146C2', '#00CC6A',
    '#498205', '#847545', '#FF4343', '#9A0089',
    '#881798', '#10893E', '#107C10', '#7E735F',
]

SocialColors = [
    '#3B5999', '#0084FF', '#55ACEE', '#0077B5',
    '#00AFF0', '#007EE5', '#21759B', '#1AB7EA',
    '#0077B5', '#4C75A3', '#34465D', '#410093',
    '#DD4B39', '#BD081C', '#CD201F', '#EB4924',
    '#FF5700', '#B92B27', '#AF0606', '#DF2029',
    '#DA552F', '#FF6600', '#FF3300', '#F57D00',
    '#25D366', '#09B83E', '#00C300', '#02B875',
    '#00B489', '#3AAF85', '#E4405F', '#EA4C89',
    '#FF0084', '#F94877', '#131418', '#FFFC00',
]

MetroColors = [
    '#A4C400', '#60A917', '#008A00', '#00ABA9',
    '#1BA1E2', '#0050EF', '#6A00FF', '#AA00FF',
    '#F472D0', '#D80073', '#A20025', '#E51400',
    '#FA6800', '#F0A30A', '#E3C800', '#825A2C',
    '#6D8764', '#647687', '#76608A', '#A0522D',
]


class CColorPalettes(QTabWidget):

    colorChanged = pyqtSignal(QColor)

    def __init__(self, *args, **kwargs):
        super(CColorPalettes, self).__init__(*args, **kwargs)

        self._setting = QSettings('CColorPicker', QSettings.NativeFormat, self)
        self.addTab(CColorItems(MaterialColors, self,
                                clicked=self.onColorChanged), 'Material')
        self.addTab(CColorItems(FlatColors, self,
                                clicked=self.onColorChanged), 'Flat')
        self.addTab(CColorItems(FluentColors, self,
                                clicked=self.onColorChanged), 'Fluent')
        self.addTab(CColorItems(SocialColors, self,
                                clicked=self.onColorChanged), 'Social')
        self.addTab(CColorItems(MetroColors, self,
                                clicked=self.onColorChanged), 'Metro')

        self.customColors = self._setting.value('colors', [])
        self.customItems = CColorItems(
            self.customColors, self, clicked=self.onColorChanged)
        self.addTab(self.customItems, 'Custom')

    def reset(self):
        self.setCurrentIndex(0)

    def onColorChanged(self, index):
        self.colorChanged.emit(
            self.sender().model().itemFromIndex(index).data())

    def addColor(self, color):
        name = color.name().upper()
        if not name in self.customColors:
            self.customColors.append(name)
            self.customItems.addColor(name)
            self.setCurrentWidget(self.customItems)
            self._setting.setValue('colors', self.customColors)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = CColorPalettes()
    w.show()
    w.colorChanged.connect(lambda c: print(c.name()))
    sys.exit(app.exec_())
