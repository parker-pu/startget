# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025
"""
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import sys
import time


class my_thread(QThread):
    send_signal = pyqtSignal(str)

    def run(self):
        while True:
            date = QDateTime.currentDateTime()
            current_time = date.toString("yyyy-MM-dd hh:mm:ss")
            self.send_signal.emit(current_time)
            time.sleep(1)

            print("更新thread! ", current_time)


class NewTableWidget(QWidget):
    sum = 0

    def __init__(self):
        super(NewTableWidget, self).__init__()
        self.resize(800, 300)
        self.setWindowTitle('例子')

        # 表头标签
        heaerlabels = ['标题1', '标题2']
        # 行数和列数
        self.rowsnum, self.columnsnum = 20, len(heaerlabels)  # 默认2行2列

        self.TableWidget = QTableWidget(self.rowsnum, self.columnsnum)

        # todo 优化 2 设置水平方向表格为自适应的伸缩模式
        # self.TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.TableWidget.horizontalHeader().setStretchLastSection(True)
        # self.TableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Todo 优化 5 将行与列的高度设置为所显示的内容的宽度高度匹配
        QTableWidget.resizeColumnsToContents(self.TableWidget)
        QTableWidget.resizeRowsToContents(self.TableWidget)

        # 设置水平方向的表头标签与垂直方向上的表头标签，注意必须在初始化行列之后进行，否则，没有效果
        self.TableWidget.setHorizontalHeaderLabels(heaerlabels)
        # Todo 优化1 设置垂直方向的表头标签
        # TableWidget.setVerticalHeaderLabels(['行1', '行2', '行3', '行4'])

        # 添加单元格初始化内容
        for i in range(self.rowsnum):
            for j in range(self.columnsnum):
                newItem = QTableWidgetItem('数据' + str(i) + ',' + str(j))
                newItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.TableWidget.setItem(i, j, newItem)

        # 表格中不显示分割线
        # TableWidget.setShowGrid(False)

        # 隐藏垂直头标签
        # TableWidget.verticalHeader().setVisible(False)

        # 创建更新按钮
        self.switch_btn = QPushButton()
        self.switch_btn.setText("启动更新")

        # 实例化线程类
        self.myThread = my_thread()

        # 单击按钮, 以单击为发送信号
        self.switch_btn.clicked.connect(self.on_clicked)

        # 整体布局
        layout = QVBoxLayout()
        layout.addWidget(self.TableWidget)
        layout.addWidget(self.switch_btn)
        self.setLayout(layout)

        # 单击按钮的槽

    def on_clicked(self):
        try:
            self.sum += 1
            if self.sum % 2 == 0:
                self.myThread.send_signal.disconnect(self.switch_slot)
                self.switch_btn.setText("重新更新")
                self.myThread.terminate()
            else:
                self.myThread.send_signal.connect(self.switch_slot)
                self.switch_btn.setText("终止更新")
                self.myThread.start()
        except Exception as e:
            print(e)

    # 连接信号的槽
    def switch_slot(self, text):
        # 更新表格内容
        for i in range(self.rowsnum):
            for j in range(self.columnsnum):
                newItem = QTableWidgetItem('数据: ' + text)
                newItem.setTextAlignment(Qt.AlignCenter)
                self.TableWidget.setItem(i, j, newItem)
        self.TableWidget.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = NewTableWidget()
    win.show()
    sys.exit(app.exec())
