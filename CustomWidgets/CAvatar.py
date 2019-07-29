#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月26日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: CustomWidgets.CAvatar
@description: 头像
"""
import os

from PyQt5.QtCore import QUrl, QRectF, Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QColor, QPainter, QPainterPath
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkDiskCache,\
    QNetworkRequest
from PyQt5.QtWidgets import QWidget, qApp


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019 Irony'
__Version__ = 1.0


class CAvatar(QWidget):

    Circle = 0              # 圆圈
    Rectangle = 1           # 圆角矩形
    SizeLarge = QSize(128, 128)
    SizeMedium = QSize(64, 64)
    SizeSmall = QSize(32, 32)

    def __init__(self, *args, shape=0, url='', cacheDir=False, size=QSize(64, 64), **kwargs):
        super(CAvatar, self).__init__(*args, **kwargs)
        self.url = ''
        self.pradius = 0            # 加载进度条半径
        self._pixmap = QPixmap()    # 图片对象
        self.pixmap = QPixmap()     # 被绘制的对象
        # 进度动画定时器
        self.loadingTimer = QTimer(self, timeout=self.onLoading)
        self.setShape(shape)
        self.setCacheDir(cacheDir)
        self.setSize(size)
        self.setUrl(url)

    def paintEvent(self, event):
        super(CAvatar, self).paintEvent(event)
        # 画笔
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        # 绘制
        path = QPainterPath()
        diameter = min(self.width(), self.height())
        if self.shape == self.Circle:
            radius = int(diameter / 2)
        elif self.shape == self.Rectangle:
            radius = 4
        halfW = self.width() / 2
        halfH = self.height() / 2
        painter.translate(halfW, halfH)
        path.addRoundedRect(
            QRectF(-halfW, -halfH, diameter, diameter), radius, radius)
        painter.setClipPath(path)
        painter.drawPixmap(-int(halfW), -int(halfH), self.pixmap)
        # 如果在加载
        if self.loadingTimer.isActive():
            diameter = 2 * self.pradius
            painter.setBrush(
                QColor(45, 140, 240, (1 - self.pradius / 10) * 255))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(
                QRectF(-self.pradius, -self.pradius, diameter, diameter), self.pradius, self.pradius)

    def onLoading(self):
        """更新进度动画
        """
        if self.loadingTimer.isActive():
            if self.pradius > 9:
                self.pradius = 0
            self.pradius += 1
        else:
            self.pradius = 0
        self.update()

    def onFinished(self):
        """图片下载完成
        """
        self.loadingTimer.stop()
        self.pradius = 0
        reply = self.sender()
        data = reply.readAll().data()
        reply.deleteLater()
        del reply
        self._pixmap.loadFromData(data)
        if self._pixmap.isNull():
            self._pixmap = QPixmap(self.size())
            self._pixmap.fill(QColor(204, 204, 204))
        self._resizePixmap()

    def onError(self, code):
        """下载出错了
        :param code:
        """
        self._pixmap = QPixmap(self.size())
        self._pixmap.fill(QColor(204, 204, 204))
        self._resizePixmap()

    def refresh(self):
        """强制刷新
        """
        self._get(self.url)

    def isLoading(self):
        """判断是否正在加载
        """
        return self.loadingTimer.isActive()

    def setShape(self, shape):
        """设置形状
        :param shape:        0=圆形, 1=圆角矩形
        """
        self.shape = shape

    def setUrl(self, url):
        """设置url,可以是本地路径,也可以是网络地址
        :param url:
        """
        self.url = url
        self._get(url)

    def setCacheDir(self, cacheDir=''):
        """设置本地缓存路径
        :param cacheDir:
        """
        self.cacheDir = cacheDir
        self._initNetWork()

    def setSize(self, size):
        """设置固定尺寸
        :param size:
        """
        if not isinstance(size, QSize):
            size = self.SizeMedium
        self.setMinimumSize(size)
        self.setMaximumSize(size)
        self._resizePixmap()

    def _resizePixmap(self):
        """缩放图片
        """
        if not self._pixmap.isNull():
            self.pixmap = self._pixmap.scaled(
                self.width(), self.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.update()

    def _initNetWork(self):
        """初始化异步网络库
        """
        if not hasattr(qApp, '_network'):
            network = QNetworkAccessManager(self.window())
            setattr(qApp, '_network', network)
        # 是否需要设置缓存
        if self.cacheDir and not qApp._network.cache():
            cache = QNetworkDiskCache(self.window())
            cache.setCacheDirectory(self.cacheDir)
            qApp._network.setCache(cache)

    def _get(self, url):
        """设置图片或者请求网络图片
        :param url:
        """
        if not url:
            self.onError('')
            return
        if url.startswith('http') and not self.loadingTimer.isActive():
            url = QUrl(url)
            request = QNetworkRequest(url)
            request.setHeader(QNetworkRequest.UserAgentHeader, b'CAvatar')
            request.setRawHeader(b'Author', b'Irony')
            request.setAttribute(
                QNetworkRequest.FollowRedirectsAttribute, True)
            if qApp._network.cache():
                request.setAttribute(
                    QNetworkRequest.CacheLoadControlAttribute, QNetworkRequest.PreferNetwork)
                request.setAttribute(
                    QNetworkRequest.CacheSaveControlAttribute, True)
            reply = qApp._network.get(request)
            self.pradius = 0
            self.loadingTimer.start(50)  # 显示进度动画
            reply.finished.connect(self.onFinished)
            reply.error.connect(self.onError)
            return
        self.pradius = 0
        if os.path.exists(url) and os.path.isfile(url):
            self._pixmap = QPixmap(url)
            self._resizePixmap()
        else:
            self.onError('')


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = CAvatar()
    w.show()
    sys.exit(app.exec_())
