# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2021-2025
"""
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from src.apps.download.views import DownLoadWidget


class MainWindow(QMainWindow):
    """
    main ui
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("src/apps/main/ui/main.ui", self)

        # 注册按钮
        self.download_button.clicked.connect(self.click_download_button)  # 下载按钮
        self.dw = DownLoadWidget()

    def click_download_button(self):
        """
        点击下载按钮
        :return:
        """
        self.dw.show()
