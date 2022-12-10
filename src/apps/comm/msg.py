# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025
"""
from PyQt6 import QtWidgets


class Msg:
    """
    消息
    """

    def info(self, msg):
        QtWidgets.QMessageBox.information(self, "通知", msg)

    def warning(self, msg):
        QtWidgets.QMessageBox.warning(self, "警告", msg)
