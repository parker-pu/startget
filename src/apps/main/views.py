# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2021-2025
"""
import PySide6
from PySide6 import QtWidgets
from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QTabWidget, QMessageBox
)
from apscheduler.schedulers.qt import QtScheduler

from src.apps.download.views import TabDownLoadUI
from src.apps.history.views import TabHistoryUI
from src.utils.file.load import Load
from src.utils.file.save import Save
from src.utils.logger import logger
from src.utils import images


class MainWindow(QMainWindow):
    """
    主页面
    """

    tabs: QTabWidget = None

    # 创建3个选项卡小控件窗口
    tab_download: QWidget = None
    tab_history: QWidget = None
    tab_sys_setting: QWidget = None
    tab_help: QWidget = None

    # 调度
    scheduler = None
    transfer_work = None

    # 文件
    load_file = None
    save_file = None
    logger = None

    # 线程
    thread_pool = None

    def __init__(self):
        super().__init__()

        self.setWindowTitle("startGet")
        self.setWindowIcon(QIcon(":/static/download_inbox_icon.ico"))
        self.resize(900, 500)

        self.scheduler = QtScheduler()

        self.load_file = Load()
        self.save_file = Save()
        self.logger = logger

        # 初始化加载控件
        self.tabs = QTabWidget()
        self.tab_download = QWidget()
        self.tab_history = QWidget()
        self.tab_sys_setting = QWidget()
        self.tab_help = QWidget()

        # 设置线程
        self.thread_pool = QThreadPool()

        self.start()

    def start(self):
        self.thread_pool.setMaxThreadCount(5)  # 设置线程池
        self.q_tab()

    def q_tab(self):
        # 设置按钮的方向，默认为上方
        self.tabs.setTabPosition(QTabWidget.TabPosition.West)
        # self.tabs.setTabShape(QTabWidget.TabShape.Triangular)
        self.tabs.setMovable(True)  # 设置按钮是否可以移动

        # 将三个选项卡添加到顶层窗口中
        self.tabs.addTab(self.tab_download, "Download")
        self.tabs.addTab(self.tab_history, "History")
        self.tabs.addTab(self.tab_sys_setting, "Setting")
        self.tabs.addTab(self.tab_help, "Help")

        self.setCentralWidget(self.tabs)

        # 每个选项卡页面绑定
        self.tab_download.setLayout(TabDownLoadUI(parent=self))
        self.tab_history.setLayout(TabHistoryUI(parent=self))
        # self.tab_sys_setting.setLayout(TabLogUI(parent=self))
        # self.tab_help.setLayout(TabHelpUI(parent=self))

    def notice_msg(self, msg_type="error", msg=None):
        """
        通知消息
        :param msg_type:
        :param msg:
        :return:
        """
        if msg_type == "error":
            QMessageBox.critical(self, "ERROR", msg)
        elif msg_type == "warning":
            QtWidgets.QMessageBox.warning(self, "WARN", msg)
        else:
            QtWidgets.QMessageBox.information(self, "MSG", msg)

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        """
        退出的时候关闭线程
        :param event:
        :return:
        """
        # stop background tasks before exiting
        self.thread_pool.clear()
        # wait for all tasks to complete before exiting
        self.thread_pool.waitForDone()
        # stop all threads
        self.thread_pool.setMaxThreadCount(0)
        event.accept()
