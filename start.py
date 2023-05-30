# -*- encoding: utf-8 -*-
import sys

from PySide6 import QtWidgets

from src.apps.main.views import MainWindow
from src.utils.sys_tray_widget import MySysTrayWidget

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()

    # 创建系统托盘项目
    tray = MySysTrayWidget(app=app, window=window)

    window.show()
    sys.exit(app.exec())
