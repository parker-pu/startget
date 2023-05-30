# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025
"""
from PySide6.QtWidgets import QTableWidget, QAbstractItemView, QTableWidgetItem, QSizePolicy


class TableTaskConf(QTableWidget):
    parent = None
    task_conf = None

    def __init__(self, parent, task_conf, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.task_conf = task_conf
        self.table_style()  # 绘制样式
        self.load_table()  # 加载数据

    def table_style(self):
        """
        表格样式
        :return:
        """
        self.setStyleSheet("QHeaderView::section {background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,"
                           "stop:0 #00007f, stop: 0.5 #00007f,stop: 0.6 #00007f, stop:1 #00007f);color: white;}")

        # 设置表头是否显示
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(True)

        self.setRowCount(0)  # 设置行数
        self.setColumnCount(5)  # 设置列数
        self.setShowGrid(True)  # 设置是否显示网格线
        self.horizontalHeader().setStretchLastSection(True)  # 设置最后一列宽度自动填充

        # 设置水平表头标签
        self.setHorizontalHeaderLabels(["Name", "Type", "Size", "Date", "Last Modified"])

        # 设置宽度
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 150)
        self.setColumnWidth(4, 150)

        # table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)  # 设置垂直表头内容居中显示
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # 将表格变为禁止编辑
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)  # 选择单个行
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)  # 按行而不是单元格选中

        # 用于控制当选择了 tableView 视图中数据项时，对应的表头区域是否高亮，默认高亮显示
        self.verticalHeader().setHighlightSections(False)
        self.horizontalHeader().setHighlightSections(False)

        # 设置高度
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMaximumHeight(400)

    def load_table(self):
        """
        加载数据
        :return:
        """
        self.clearContents()
        self.setRowCount(len(self.task_conf))

        index = 0
        for row in self.task_conf:
            if not isinstance(row, (dict,)):
                continue

            # 处理表格数据
            self.setItem(index, 0, QTableWidgetItem(row.get("Name")))
            self.setItem(index, 1, QTableWidgetItem(row.get("Type")))
            self.setItem(index, 2, QTableWidgetItem(row.get("Size")))
            self.setItem(index, 3, QTableWidgetItem(row.get("Date")))
            self.setItem(index, 4, QTableWidgetItem(row.get("Last Modified")))

            index += 1

    def refresh_table(self):
        """
        刷新表格
        :return:
        """
        pass

    def delete_row(self):
        """
        刷新表格
        :return:
        """
        pass
