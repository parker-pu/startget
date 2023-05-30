# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025
"""
import requests
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
)

from src.apps.download.ui.dialog_task_conf import TaskConfDialog
from src.utils import images
from src.utils.file.func import convert_size
from src.utils.spinner import WaitingSpinner


class AddTaskDialog(QDialog):
    """
    添加下载任务
    """
    parent = None

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.setWindowTitle("Add Task")
        self.spinner = WaitingSpinner(
            self,
            roundness=100.0,
            # opacity=3.141592653589793,
            fade=80.0,
            radius=10,
            lines=20,
            line_length=10,
            line_width=2,
            speed=1.5707963267948966,
            # color=(0, 0, 0)
        )
        self.setWindowIcon(QIcon(":/static/link_broken_link_url_hyperlink_icon.ico"))
        self.resize(500, 200)
        self.start()

    def start(self):
        """
        编辑表单布局
        :return:
        """
        # 外层容器
        container = QVBoxLayout()

        # 表单容器
        form_layout_url = QFormLayout()
        url_edit = QTextEdit(
            "https://sf1-hscdn-tos.pstatp.com/obj/media-fe/xgplayer_doc_video/flv/xgplayer-demo-720p.flv")
        # url_edit.setLineWrapMode(QTextEdit.WidgetWidth)  # 添加换行
        form_layout_url.setWidget(0, QFormLayout.FieldRole, url_edit)

        container.addLayout(form_layout_url)

        def ok_button_func():
            d_url = url_edit.toPlainText()
            self.spinner.start()
            url_items = self.get_download_info(d_url)
            self.close()  # 关闭
            self.spinner.stop()
            if url_items:
                # 把数据传递给子组件
                TaskConfDialog(self.parent, task_conf=url_items).exec()

        # ------------------------------- 功能按钮 -------------------------------
        horizontal_layout = QHBoxLayout()
        horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        horizontal_layout.addItem(horizontal_spacer)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(ok_button_func)
        horizontal_layout.addWidget(ok_button)

        container.addLayout(horizontal_layout)
        self.setLayout(container)

    def get_download_info(self, url):
        """
        获取下载文件信息
        :param url:
        :return:
        """
        rd = []
        try:
            # 如果是一个链接包含多个的时候需要依次获取各个资源
            resp = requests.get(url, stream=True)
            headers_data, url_info_dict = dict(resp.headers), {}
            headers_data["req_url"] = url

            # URL 的信息
            url_info_dict["URL"] = url
            url_info_dict["Name"] = url.split("/")[-1]
            url_info_dict["Type"] = headers_data.get("Content-Type", "")
            url_info_dict["Size"] = convert_size(int(headers_data.get("Content-Length", 0)))
            url_info_dict["Date"] = headers_data.get("Date", "")
            url_info_dict["Status"] = "Download"
            url_info_dict["Last Modified"] = headers_data.get("Last-Modified", "")
            rd.append(url_info_dict)
        except Exception as e:
            self.parent.logger.error(e)
            self.parent.notice_msg(msg=str(e))
        finally:
            return rd
