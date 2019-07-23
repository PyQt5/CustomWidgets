#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年4月21日
@author: Irony
@site: https://pyqt5.com https://github.com/PyQt5
@email: 892768447@qq.com
@file: CustomWidgets.CColorPicker.CColorItems
@description: 小方块列表
"""
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QListView, QStyledItemDelegate, QStyle


__Author__ = "Irony"
__Copyright__ = "Copyright (c) 2019 "
__Version__ = "Version 1.0"


class StyledItemDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        if option.state & QStyle.State_HasFocus:
            # 取消虚线框
            option.state = option.state ^ QStyle.State_HasFocus

        # 取出颜色
        item = index.model().itemFromIndex(index)
        color = item.data()

        # 绘制矩形区域
        rect = option.rect
        # 是否鼠标悬停
        _in = option.state & QStyle.State_MouseOver

        painter.save()
        painter.setPen(color.darker(150) if _in else Qt.NoPen)
        painter.setBrush(color)
        rect = rect if _in else rect.adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(rect, 2, 2)
        painter.restore()


class CColorItems(QListView):

    def __init__(self, colors, *args, **kwargs):
        super(CColorItems, self).__init__(*args, **kwargs)
        self.setItemDelegate(StyledItemDelegate(self))
        self.setEditTriggers(self.NoEditTriggers)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.setSpacing(6)
        self.setCursor(Qt.PointingHandCursor)
        self.setFrameShape(self.NoFrame)
        self._model = QStandardItemModel(self)
        self.setModel(self._model)

        for color in colors:
            self.addColor(color)
    
    def addColor(self, color):
        item = QStandardItem('')
        item.setData(QColor(color))
        item.setSizeHint(QSize(20, 20))
        item.setToolTip(color)
        self._model.appendRow(item)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = CColorItems(['#A4C400', '#60A917', '#008A00', '#00ABA9', ])
    w.colorChanged.connect(lambda c: print('color: ', c.name()))
    w.show()
    sys.exit(app.exec_())
