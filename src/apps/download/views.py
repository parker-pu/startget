# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025

视频测试地址
https://sf1-hscdn-tos.pstatp.com/obj/media-fe/xgplayer_doc_video/flv/xgplayer-demo-720p.flv
"""

from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy
)

from src.apps.download.ui.dialog_add_task import AddTaskDialog
from src.apps.download.ui.table_download import TableDownload


class TabDownLoadUI(QVBoxLayout):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.start()

    def start(self):
        table_widget = TableDownload(parent=self.parent)

        # -------------------------------------------- 顶部功能区 ----------------------------------------
        top_frame = QWidget()
        horizontal_layout = QHBoxLayout(top_frame)  # 水平布局
        horizontal_layout.setContentsMargins(0, 0, 0, 0)

        # ============================================ 添加任务 ==========================================
        def add_task():
            """
            添加任务
            :return:
            """
            AddTaskDialog(self.parent).exec()

        create_button = QPushButton("Add", top_frame)
        create_button.setStyleSheet("QPushButton{background:#54FF9F}QPushButton:hover{background:LawnGreen;}")
        create_button.clicked.connect(add_task)
        horizontal_layout.addWidget(create_button)

        # ============================================ 删除任务 ==========================================
        def delete_task():
            """
            删除任务
            :return:
            """
            pass

        # 删除按钮
        delete_button = QPushButton("Delete", top_frame)
        delete_button.setStyleSheet("QPushButton{background:#FFC0CB}QPushButton:hover{background:HotPink;}")
        delete_button.clicked.connect(delete_task)
        horizontal_layout.addWidget(delete_button)

        # 空格占位
        horizontal_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # ============================================ 刷新任务 ==========================================
        def refresh_task():
            """
            刷新任务
            :return:
            """
            table_widget.refresh_table()

        refresh_button = QPushButton("Refresh", top_frame)
        refresh_button.clicked.connect(refresh_task)
        horizontal_layout.addWidget(refresh_button)

        table_widget.refresh_table()  # 加载数据
        # 操作布局
        # load_host_config()  # 加载数据
        self.addWidget(top_frame)  # 增加功能区
        self.addWidget(table_widget)  # 增加表格
