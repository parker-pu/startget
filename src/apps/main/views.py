# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2021-2025
"""
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QStackedLayout,
    QWidget,
    QToolBar
)

from src.apps.download.views import (
    DownLoadWidget,
    DownLoadRunWidget,
    DownLoadComplete
)


class MainWindow(QMainWindow):
    """
    main ui
    """
    top_tool_bar: QToolBar
    left_tool_bar: QToolBar
    main_layout: QStackedLayout
    main_widget: QWidget
    new_add_download_widget: QWidget

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("src/apps/main/ui/main.ui", self)

        # 创建ToolBar
        self.top_tool_bar = QToolBar(self)
        self.left_tool_bar = QToolBar(self)

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.top_tool_bar)  # 添加 ToolBar 到主界面
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.left_tool_bar)  # 添加 ToolBar 到主界面

        self.main_layout = QStackedLayout()  # 创建抽屉布局
        self.main_widget = QWidget()  # 注册一个 QWidget

        self.new_add_download_widget = DownLoadWidget()  # 注册新下载页面

        self.setup_main_layout()
        self.setup_top_tool_bar()
        self.setup_left_tool_bar()

    def setup_top_tool_bar(self):
        """
        设置上部按钮
        :return:
        """
        self.new_download_button.clicked.connect(self.click_download_button)  # 新增下载按钮
        self.top_tool_bar.addWidget(self.new_download_button)  # ToolBar添加ToolButton按钮

    def setup_left_tool_bar(self):
        """
        设置左侧按钮
        :return:
        """
        self.download_run_button.clicked.connect(lambda: self.on_button_clicked(0))
        self.left_tool_bar.addWidget(self.download_run_button)  # ToolBar添加ToolButton按钮

        self.download_complete_button.clicked.connect(lambda: self.on_button_clicked(1))
        self.left_tool_bar.addWidget(self.download_complete_button)  # ToolBar添加ToolButton按钮

    def setup_main_layout(self):
        """
        设置主布局
        :return:
        """
        self.main_layout.addWidget(DownLoadRunWidget())
        self.main_layout.addWidget(DownLoadComplete())
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def on_button_clicked(self, index):
        """
        点击鼠标切换
        :param index:
        :return:
        """
        if index < self.main_layout.count():
            self.main_layout.setCurrentIndex(index)

    def click_download_button(self):
        """
        点击下载按钮
        :return:
        """
        self.new_add_download_widget.show()
