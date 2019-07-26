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

from PyQt5.QtCore import QUrl
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

    def __init__(self, *args, shape=0, url='', cacheDir=False, **kwargs):
        super(CAvatar, self).__init__(*args, **kwargs)
        self.loading = False        # 是否正在加载
        self.progress = 0           # 加载进度
        self.url = ''
        self._pixmap = QPixmap()    # 图片对象
        self.setShape(shape)
        self.setCacheDir(cacheDir)
        self.setUrl(url)

    def paintEvent(self, event):
        super(CAvatar, self).paintEvent(event)
        # 画笔
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        # 绘制路径
        path = QPainterPath()
        diameter = min(self.width(), self.height())
        if self.shape == self.Circle:
            radius = int(diameter / 2)
        elif self.shape == self.Rectangle:
            radius = 4
        path.addRoundedRect(0, 0, diameter, diameter, radius, radius)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, self._pixmap)

    def _get(self, url):
        """设置图片或者请求网络图片
        :param url:
        """
        if not url:
            return
        if os.path.exists(url) and os.path.isfile(url):
            self._pixmap = QPixmap(url)
            self.update()
            self.progress = 0
            self.loading = False
            return
        if url.startswith('http') and not self.loading:
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
            self.loading = True
            self.progress = 0
            reply.downloadProgress.connect(self.onDownloadProgress)
            reply.finished.connect(self.onFinished)
            reply.error.connect(self.onError)

    def onDownloadProgress(self, bytesReceived, bytesTotal):
        """下载进度
        :param bytesReceived:         接收量
        :param bytesTotal:            总量
        """
        self.progress = abs(int(bytesReceived / bytesTotal * 100))
        self.update()

    def onFinished(self):
        """图片下载完成
        """
        self.loading = False
        self.progress = 0
        reply = self.sender()
        data = reply.readAll().data()
        reply.deleteLater()
        del reply
        self._pixmap.loadFromData(data)
        if self._pixmap.isNull():
            self._pixmap.fill(QColor(204, 204, 204))
        self.update()

    def onError(self, code):
        """下载出错了
        :param code:
        """
        self._pixmap.fill(QColor(204, 204, 204))
        self.update()

    def refresh(self):
        """强制刷新
        """
        self._get(self.url)

    def isLoading(self):
        """判断是否正在加载
        """
        return self.loading

    def setShape(self, shape):
        """设置形状
        :param shape:        0=圆形, 1=圆角矩形
        """
        self.shape = shape

    def setUrl(self, url):
        """设置url,可以是本地路径,也可以是网络地址
        :param url:
        """
        if self.url == url:
            return
        self.url = url
        self._get(url)

    def setCacheDir(self, cacheDir=''):
        """设置本地缓存路径
        :param cacheDir:
        """
        self.cacheDir = cacheDir
        self._initNetWork()

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


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = CAvatar()
    w.show()
    sys.exit(app.exec_())
