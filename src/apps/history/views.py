# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025
历史
"""

from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy
)
from src.apps.history.ui.table_history import TableHistory


class TabHistoryUI(QVBoxLayout):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.start()

    def start(self):
        table_widget = TableHistory(parent=self.parent)

        # -------------------------------------------- 顶部功能区 ----------------------------------------
        top_frame = QWidget()
        horizontal_layout = QHBoxLayout(top_frame)  # 水平布局
        horizontal_layout.setContentsMargins(0, 0, 0, 0)

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
