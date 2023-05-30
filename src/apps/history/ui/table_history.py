# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025
"""
from PySide6.QtWidgets import QTableWidget, QAbstractItemView, QTableWidgetItem

from src.utils.file.load import Load


class TableHistory(QTableWidget):
    parent = None

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.table_style()  # 绘制样式

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
        self.setColumnCount(3)  # 设置列数
        self.setShowGrid(True)  # 设置是否显示网格线
        self.horizontalHeader().setStretchLastSection(True)  # 设置最后一列宽度自动填充

        # 设置水平表头标签
        self.setHorizontalHeaderLabels(["File Name", "Status", "Other"])

        # 设置宽度
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 150)
        self.setColumnWidth(2, 150)

        # table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)  # 设置垂直表头内容居中显示
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # 将表格变为禁止编辑
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)  # 选择单个行
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)  # 按行而不是单元格选中

        # 用于控制当选择了 tableView 视图中数据项时，对应的表头区域是否高亮，默认高亮显示
        self.verticalHeader().setHighlightSections(False)
        self.horizontalHeader().setHighlightSections(False)

    def load_table(self):
        """
        加载数据
        :return:
        """
        self.clearContents()
        # 加载文件
        fd = Load()
        hd = [item for item in fd.load_history_config() if item.get("Status") == "Finish"]
        self.setRowCount(len(hd))

        index = 0
        for row in hd:
            if not isinstance(row, (dict,)):
                continue

            # 处理表格数据
            self.setItem(index, 0, QTableWidgetItem(row.get("Name")))
            self.setItem(index, 1, QTableWidgetItem(str(row.get("Status"))))
            self.setItem(index, 2, QTableWidgetItem(row.get("Last Modified")))

            index += 1

    def refresh_table(self):
        """
        刷新表格
        :return:
        """
        self.load_table()

    def delete_row(self):
        """
        刷新表格
        :return:
        """
        pass
