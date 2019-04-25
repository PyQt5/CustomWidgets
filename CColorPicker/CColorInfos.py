#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年4月21日
@author: Irony
@site: https://pyqt5.com https://github.com/PyQt5
@email: 892768447@qq.com
@file: CColorPicker.CColorInfos
@description: 
"""
from PyQt5.QtCore import QSize, Qt, QRegExp, pyqtSignal
from PyQt5.QtGui import QRegExpValidator, QColor
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, QSpinBox,\
    QSpacerItem, QSizePolicy, QPushButton


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019 "
__Version__ = "Version 1.0"


class CColorInfos(QWidget):

    colorChanged = pyqtSignal(QColor, int)
    colorAdded = pyqtSignal(QColor)

    def __init__(self, *args, **kwargs):
        super(CColorInfos, self).__init__(*args, **kwargs)
        layout = QGridLayout(self)
        layout.setContentsMargins(11, 2, 11, 2)
        layout.setSpacing(8)

        self.editHex = QLineEdit(
            '#FF0000', self, alignment=Qt.AlignCenter,
            objectName='editHex',
            textChanged=self.onHexChanged)
        self.editHex.setValidator(
            QRegExpValidator(QRegExp('#[0-9a-fA-F]{6}$'), self.editHex))
        self.labelHex = QLabel('HEX', self, alignment=Qt.AlignCenter)
        layout.addWidget(self.editHex, 0, 0)
        layout.addWidget(self.labelHex, 1, 0)

        layout.addItem(QSpacerItem(
            10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum), 0, 1)

        self.editRed = QSpinBox(
            self, buttonSymbols=QSpinBox.NoButtons,
            alignment=Qt.AlignCenter, valueChanged=self.onRgbaChanged)
        self.editRed.setRange(0, 255)
        self.labelRed = QLabel('R', self, alignment=Qt.AlignCenter)
        layout.addWidget(self.editRed, 0, 2)
        layout.addWidget(self.labelRed, 1, 2)

        self.editGreen = QSpinBox(
            self, buttonSymbols=QSpinBox.NoButtons,
            alignment=Qt.AlignCenter, valueChanged=self.onRgbaChanged)
        self.editGreen.setRange(0, 255)
        self.labelGreen = QLabel('G', self, alignment=Qt.AlignCenter)
        layout.addWidget(self.editGreen, 0, 3)
        layout.addWidget(self.labelGreen, 1, 3)

        self.editBlue = QSpinBox(
            self, buttonSymbols=QSpinBox.NoButtons,
            alignment=Qt.AlignCenter, valueChanged=self.onRgbaChanged)
        self.editBlue.setRange(0, 255)
        self.labelBlue = QLabel('B', self, alignment=Qt.AlignCenter)
        layout.addWidget(self.editBlue, 0, 4)
        layout.addWidget(self.labelBlue, 1, 4)

        self.editAlpha = QSpinBox(
            self, buttonSymbols=QSpinBox.NoButtons,
            alignment=Qt.AlignCenter, valueChanged=self.onRgbaChanged)
        self.editAlpha.setRange(0, 255)
        self.labelAlpha = QLabel('A', self, alignment=Qt.AlignCenter)
        layout.addWidget(self.editAlpha, 0, 5)
        layout.addWidget(self.labelAlpha, 1, 5)

        layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 6)
        layout.addWidget(QPushButton(
            '+', self, cursor=Qt.PointingHandCursor,
            toolTip='添加自定义颜色',
            clicked=self.onColorAdd), 0, 7)

        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 1)
        layout.setColumnStretch(5, 1)
        layout.setColumnStretch(6, 2)
        layout.setColumnStretch(7, 1)
        self.setFocus()
        self.editRed.setValue(255)
        self.editAlpha.setValue(255)

    def reset(self):
        pass

    def onColorAdd(self):
        self.colorAdded.emit(QColor(
            self.editRed.value(),
            self.editGreen.value(),
            self.editBlue.value()
        ))

    def setHex(self, code):
        self.editHex.setText(str(code))

    def updateColor(self, color):
        self.editRed.setValue(color.red())
        self.editGreen.setValue(color.green())
        self.editBlue.setValue(color.blue())

    def updateAlpha(self, _, alpha):
        self.editAlpha.setValue(alpha)

    def onHexChanged(self, code):
        if len(code) != 7:
            return
        color = QColor(code)
        if color.isValid():
            self.blockRgbaSignals(True)
            self.editHex.blockSignals(True)
            self.editRed.setValue(color.red())
            self.editGreen.setValue(color.green())
            self.editBlue.setValue(color.blue())
            self.editAlpha.setValue(color.alpha())
            self.colorChanged.emit(color, color.alpha())
            self.editHex.blockSignals(False)
            self.blockRgbaSignals(False)

    def onRgbaChanged(self, _):
        self.editHex.blockSignals(True)
        self.blockRgbaSignals(True)
        color = QColor(
            self.editRed.value(),
            self.editGreen.value(),
            self.editBlue.value(),
            self.editAlpha.value()
        )
        self.editHex.setText(color.name())
        self.colorChanged.emit(color, self.editAlpha.value())
        self.blockRgbaSignals(False)
        self.editHex.blockSignals(False)

    def blockRgbaSignals(self, block=True):
        self.editRed.blockSignals(block)
        self.editGreen.blockSignals(block)
        self.editBlue.blockSignals(block)
        self.editAlpha.blockSignals(block)

    def sizeHint(self):
        return QSize(280, 48)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = CColorInfos()
    w.show()
    sys.exit(app.exec_())
