# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025

视频测试地址
https://sf1-hscdn-tos.pstatp.com/obj/media-fe/xgplayer_doc_video/flv/xgplayer-demo-720p.flv
"""
import requests
from PyQt6 import uic
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QPlainTextEdit, QTableView, QHeaderView

from src.apps.comm.msg import Msg


class DownLoadWidget(QWidget, Msg):
    input_url: QPlainTextEdit

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("src/apps/download/ui/download.ui", self)

        self.ok_button.clicked.connect(self.parse_download_url)  # 确认下载
        self.ds = DownLoadSaveWidget()

    def parse_download_url(self):
        text = self.input_url.toPlainText()
        if text:
            resp = requests.get(text, stream=True)
            headers_data = dict(resp.headers)
            try:
                # 4行3列
                model = QStandardItemModel(len(headers_data.keys()), 2)

                # 关联QTableView控件和Model
                self.ds.url_info.setModel(model)

                i = 0
                for k, v in headers_data.items():
                    # 添加数据
                    model.setItem(i, 0, QStandardItem(k))  # 第一行第一列
                    model.setItem(i, 1, QStandardItem(v))  # 第一行第二列
                    i += 1

                self.ds.show()

            except Exception as e:
                print(e)
        else:
            self.warning("没有输入数据")


class DownLoadSaveWidget(QWidget, Msg):
    input_url: QPlainTextEdit

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("src/apps/download/ui/download_save.ui", self)

    #     self.ok_button.clicked.connect(self.parse_download_url)  # 确认下载
    #
    # def parse_download_url(self):
    #     text = self.input_url.toPlainText()
    #     if text:
    #         resp = requests.get(text, stream=True)
    #         print(resp.headers)
    #         # with requests.get(text, stream=True) as r:
    #         #     print('开始下载。。。')
    #         #     content_size = int(r.headers['content-length'])
    #         #     with open('v.mp4', 'wb') as f:
    #         #         n = 1
    #         #         for i in r.iter_content(chunk_size=1024):
    #         #             loaded = n * 1024.0 / content_size
    #         #             print(loaded)
    #         #             f.write(i)
    #         #             print('已下载{0:%}'.format(loaded))
    #         #             n += 1
    #     else:
    #         self.warning("没有输入数据")
