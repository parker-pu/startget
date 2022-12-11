# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedLayout, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QToolBar, QToolButton, QColorDialog, QFontDialog, QFileDialog, QMessageBox, QStyle
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class MyStackedLayout(QMainWindow):
    def __init__(self, parent=None):
        super(MyStackedLayout, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.resize(800, 480)
        self.move(300, 300)
        self.setWindowTitle("StackedLayout堆栈布局")

        toolBar = QToolBar(self)  # 创建ToolBar
        # self.addToolBar(Qt.LeftToolBarArea, toolBar)  # 添加ToolBar到主界面
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, toolBar)  # 添加ToolBar到主界面

        # 创建一个ToolButton
        btnColor = QToolButton(self)
        btnColor.setText("颜色对话框")
        btnColor.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        btnColor.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        btnColor.clicked.connect(lambda: self.onButtonClicked(0))
        toolBar.addWidget(btnColor)  # ToolBar添加ToolButton按钮

        btnFont = QToolButton(self)
        btnFont.setText("字体对话框")
        btnFont.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DesktopIcon))
        btnFont.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        btnFont.clicked.connect(lambda: self.onButtonClicked(1))
        toolBar.addWidget(btnFont)

        btnFile = QToolButton(self)
        btnFile.setText("文件对话框")
        btnFile.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton))
        btnFile.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        btnFile.clicked.connect(lambda: self.onButtonClicked(2))
        toolBar.addWidget(btnFile)

        self.mainlayout = QStackedLayout()
        self.mainlayout.addWidget(QColorDialog(self))  # StackedLayout添加一个Widget,  index为0
        self.mainlayout.addWidget(QFontDialog(self))  # StackedLayout添加一个Widget,  index为1
        self.mainlayout.addWidget(QFileDialog(self))  # StackedLayout添加一个Widget,  index为2

        self.mainwidget = QWidget()
        self.mainwidget.setLayout(self.mainlayout)
        self.setCentralWidget(self.mainwidget)

    def onButtonClicked(self, index):
        if index < self.mainlayout.count():
            self.mainlayout.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyStackedLayout()
    win.show()
    sys.exit(app.exec())
