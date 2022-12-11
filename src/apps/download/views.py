# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025

视频测试地址
https://sf1-hscdn-tos.pstatp.com/obj/media-fe/xgplayer_doc_video/flv/xgplayer-demo-720p.flv
"""
from pathlib import Path

import requests
from PyQt6 import uic
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import (
    QStandardItemModel,
    QStandardItem
)
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import (
    QWidget,
    QPlainTextEdit,
    QFileDialog,
    QLineEdit,
    QTableView,
    QLabel,
    QTableWidget,
    QTableWidgetItem, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea
)

from src.apps.comm.db import DB
from src.apps.comm.f import convert_size
from src.apps.comm.msg import Msg


class DownLoadWidget(QWidget, Msg):
    input_url: QPlainTextEdit

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("src/apps/download/ui/download.ui", self)

        # TODO:测试
        self.input_url.setPlainText(
            "https://sf1-hscdn-tos.pstatp.com/obj/media-fe/xgplayer_doc_video/flv/xgplayer-demo-720p.flv")

        self.ok_button.clicked.connect(self.parse_download_url)  # 确认下载
        self.ds = DownLoadSaveWidget()

    def parse_download_url(self):
        _url = self.input_url.toPlainText()
        if _url:
            self.close()  # 关闭下载的页面
            resp = requests.get(_url, stream=True)
            headers_data, url_info_dict = dict(resp.headers), {}
            headers_data["req_url"] = _url

            # 给子组件赋予数据
            self.ds.headers_data = headers_data

            # URL 的信息
            url_info_dict["类型"] = headers_data.get("Content-Type", "")
            url_info_dict["大小"] = convert_size(int(headers_data.get("Content-Length", 0)))
            url_info_dict["时间"] = headers_data.get("Date", "")
            url_info_dict["最后修改时间"] = headers_data.get("Last-Modified", "")

            # 列表数据
            url_list_model = QStandardItemModel(1, 1)
            self.ds.url_data_list.setModel(url_list_model)  # 关联 QTableView 控件和Model
            # ResizeToContents
            self.ds.url_data_list.horizontalHeader().setStretchLastSection(True)
            self.ds.url_data_list.resizeRowsToContents()
            url_list_model.setItem(0, 0, QStandardItem(_url))  # 第一行第一列

            # 信息数据
            model = QStandardItemModel(len(url_info_dict.keys()), 2)  # 关联 QTableView 控件和Model
            self.ds.url_info.setModel(model)
            # ResizeToContents
            self.ds.url_info.horizontalHeader().setStretchLastSection(True)
            self.ds.url_info.resizeRowsToContents()

            i = 0
            for k, v in url_info_dict.items():
                # 添加数据
                model.setItem(i, 0, QStandardItem(k))  # 第一行第一列
                model.setItem(i, 1, QStandardItem(v))  # 第一行第二列
                i += 1

            self.ds.show()
        else:
            self.warning("没有输入数据")


class DownLoadSaveWidget(QWidget, DB, Msg):
    input_url: QPlainTextEdit
    file_path: QLineEdit
    url_info: QTableView
    headers_data: dict

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("src/apps/download/ui/download_save.ui", self)

        self.default_save_folder()
        self.open_save_folder.clicked.connect(self.open_local_folder)  # 保存文件
        self.down_ok_button.clicked.connect(self.down_ok_save)  # 保存下载信息

    def default_save_folder(self):
        """
        获取默认文件夹
        :return:
        """
        q = self.exec("SELECT * FROM constance_config WHERE key = 'DEFAULT_SAVE_FOLDER' LIMIT 1")
        q.next()
        self.file_path.setText(q.value("value"))

    def open_local_folder(self):
        """
        打开本地文件夹
        :return:
        """
        directory_path = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")  # 起始路径
        self.file_path.setText(directory_path)

    def down_ok_save(self):
        """
        保存下载信息
        :return:
        """
        query = QSqlQuery(self.db)
        query.prepare("INSERT INTO downloads(name,url,data_size,data_md5,file_path) "
                      "VALUES(:name,:url,:data_size,:data_md5,:file_path)")

        query.bindValue(":name", Path(self.headers_data.get("req_url")).name)
        query.bindValue(":url", str(self.headers_data.get("req_url")))
        query.bindValue(":data_size", convert_size(int(self.headers_data.get("Content-Length", 0))))
        query.bindValue(":data_md5", self.headers_data.get("Content-MD5", ""))
        query.bindValue(":file_path", self.file_path.text())
        query.exec()

        # 更新列表
        self.close()

        # self.exec("SELECT * FROM constance_config WHERE key = 'DEFAULT_SAVE_FOLDER' LIMIT 1")

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


class DownLoadBlockWidget(QWidget, DB):
    row_task_layout_dict: dict = {}
    task_list_layout: QVBoxLayout

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        uic.loadUi("src/apps/download/ui/download_run2.ui", self)

        self.setup_ui()

    def setup_ui(self):
        # self.task_list_layout.addStretch(2)
        # self.task_list_layout.setSpacing(5)

        q: QSqlQuery = self.exec("SELECT * FROM downloads WHERE status IN('WAIT') ORDER BY id")
        # q: QSqlQuery = self.exec("SELECT * FROM downloads WHERE status IN('WAIT') ORDER BY id DESC LIMIT 10")
        i = 0

        while q.next():
            row_task_layout = QHBoxLayout()

            for qe in ("name", "data_size", "status", "loaded"):
                _task = QLineEdit()
                _task.setText(str(q.value(qe)))
                _task.setReadOnly(True)
                row_task_layout.addWidget(_task)

            self.row_task_layout_dict[str(q.value("id"))] = row_task_layout
            self.task_list_layout.insertLayout(i, row_task_layout)

    def update_data(self):
        pass


class RowTaskWidget(QWidget, DB):
    row_task_layout_dict: {}

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        uic.loadUi("src/apps/download/ui/row_task.ui", self)


class DownLoadRunWidget(QWidget, DB):
    download_run_table_widget: QTableWidget

    def __init__(self):
        super().__init__()
        uic.loadUi("src/apps/download/ui/download_run.ui", self)

        self.download_run_table_widget.horizontalHeader().setStretchLastSection(True)
        # self.download_run_table_widget.isFullScreen()
        # self.download_run_table_widget.resizeRowsToContents()
        self.download_run_table_widget.horizontalHeader().setStyleSheet("QHeaderView::section{background:grey;}")

        self.download_run_table_widget.setRowCount(100)

        self.load_data()

        # 定时
        self.crontab_time = QTimer(self)
        self.crontab_time.start(1000)
        # 给QTimer设定一个时间，每到达这个时间一次就会调用一次该方法
        self.crontab_time.timeout.connect(self.load_data)

    def load_data(self):
        """
        加载数据
        :return:
        """
        q: QSqlQuery = self.exec("SELECT * FROM downloads WHERE status IN('WAIT') ORDER BY id DESC")
        i = 0

        while q.next():
            # self.download_run_table_widget.setRowCount(i + 1)  # 动态设置列
            self.download_run_table_widget.setItem(i, 0, QTableWidgetItem(q.value("name")))
            self.download_run_table_widget.setItem(i, 1, QTableWidgetItem(q.value("data_size")))
            self.download_run_table_widget.setItem(i, 2, QTableWidgetItem(q.value("status")))
            self.download_run_table_widget.setItem(i, 3, QTableWidgetItem(str(q.value("loaded"))))
            i += 1
        self.download_run_table_widget.setRowCount(i)
        # self.download_run_table_widget.update()


class DownLoadComplete(QWidget, DB):
    download_complete_table_widget: QTableWidget

    def __init__(self):
        super().__init__()
        uic.loadUi("src/apps/download/ui/download_complete.ui", self)

        self.load_data()

        # 定时
        self.crontab_time = QTimer(self)
        self.crontab_time.start(1000)
        # 给QTimer设定一个时间，每到达这个时间一次就会调用一次该方法
        self.crontab_time.timeout.connect(self.load_data)

    def load_data(self):
        """
        加载数据
        :return:
        """
        q: QSqlQuery = self.exec("SELECT * FROM downloads WHERE status IN('COMPLETE') ORDER BY id DESC")
        i = 0
        self.download_complete_table_widget.horizontalHeader().setStretchLastSection(True)
        # self.download_complete_table_widget.isFullScreen()
        self.download_complete_table_widget.horizontalHeader().setStyleSheet("QHeaderView::section{background:grey;}")

        while q.next():
            self.download_complete_table_widget.setRowCount(i + 1)  # 动态设置列
            self.download_complete_table_widget.setItem(i, 0, QTableWidgetItem(q.value("name")))
            self.download_complete_table_widget.setItem(i, 1, QTableWidgetItem(q.value("data_size")))
            self.download_complete_table_widget.setItem(i, 2, QTableWidgetItem(q.value("status")))
            self.download_complete_table_widget.setItem(i, 3, QTableWidgetItem(str(q.value("loaded"))))
            i += 1
            self.download_complete_table_widget.update()
