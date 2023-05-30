# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025
"""
import uuid

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
    QLabel,
    QFileDialog
)

from src.apps.comm.thread_download import ThreadDownload
from src.apps.download.ui.table_task_conf import TableTaskConf
from src.settings import BASE_DIR
from src.utils import images


class TaskConfDialog(QDialog):
    """
    添加下载任务
    """
    parent = None
    spinner = None
    task_conf = None

    def __init__(self, parent=None, task_conf: list | tuple = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.task_conf = task_conf  # 配置信息
        self.setWindowTitle("Task Conf")
        self.setWindowIcon(QIcon(":/static/link_broken_link_url_hyperlink_icon.ico"))
        self.resize(800, 400)
        self.start()

    def start(self):
        """
        编辑表单布局
        :return:
        """
        # 外层容器
        container = QVBoxLayout()

        # 下载内容的表格
        tf = TableTaskConf(parent=self.parent, task_conf=self.task_conf)

        # 文件输入
        file_input_layout = QHBoxLayout()
        file_save_path = QLineEdit(str(BASE_DIR.joinpath("download")))
        file_select_button = QPushButton()
        file_select_button.setIcon(QIcon(":/static/folder.ico"))

        def open_directory():
            dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
            file_save_path.setText(dir_path)

        file_select_button.clicked.connect(open_directory)
        file_input_layout.addWidget(file_save_path)
        file_input_layout.addWidget(file_select_button)

        # ------------------------------- 功能按钮 -------------------------------
        horizontal_layout = QHBoxLayout()
        horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        horizontal_layout.addItem(horizontal_spacer)

        def ok_button_func():
            # 添加下载
            for row in self.task_conf:
                td = ThreadDownload(
                    uuid=str(uuid.uuid4()),
                    url=row.get("URL"),
                    file_name=row.get("Name"),
                    file_path=file_save_path.text(),
                    **row
                )
                self.parent.thread_pool.start(td)  # 加入线程池
            self.close()  # 关闭

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(ok_button_func)
        horizontal_layout.addWidget(ok_button)

        container.addWidget(tf)  # 表格
        container.addLayout(file_input_layout)  # 文件选择
        container.addLayout(horizontal_layout)  # 功能按钮
        self.setLayout(container)
