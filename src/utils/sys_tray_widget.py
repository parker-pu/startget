# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025

系统托盘
"""
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QWidget, QSystemTrayIcon, QMenu
from src.utils import images


class MySysTrayWidget(QWidget):
    def __init__(self, app=None, window=None):
        QWidget.__init__(self)  # 必须调用，否则信号系统无法启用

        #  私有变量
        self.__app = app
        self.__window = window

        # 配置系统托盘
        self.__tray_icon = QSystemTrayIcon(self)
        self.__tray_icon.setIcon(QIcon(":/static/download_inbox_icon.ico"))
        self.__tray_icon.setToolTip('D22Maid\n热键Ctrl+Alt+M')

        # 创建托盘的右键菜单
        self.__tray_menu = QMenu()
        self.__tray_action = []
        # self.add_tray_menu_action("MainWindow", self.show_main_interface)
        self.add_tray_menu_action("Quit", self.quit)

        # 配置菜单并显示托盘
        self.__tray_icon.setContextMenu(self.__tray_menu)  # 把tpMenu设定为托盘的右键菜单
        self.__tray_icon.show()  # 显示托盘

        # 隐藏连接信号
        # self.__ui.pushButton.clicked.connect(self.hide_userinterface)

        # 默认隐藏界面
        self.hide_main_interface()

    def __del__(self):
        pass

    def add_tray_menu_action(self, text='empty', callback=None):
        a = QAction(text, self)
        a.triggered.connect(callback)
        self.__tray_menu.addAction(a)
        self.__tray_action.append(a)

    def quit(self):
        # 真正的退出
        self.__app.exit()

    def show_main_interface(self):
        self.__window.show()

    def hide_main_interface(self):
        self.__window.hide()
