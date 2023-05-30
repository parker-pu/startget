# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025
"""

from PySide6.QtCore import QObject, Slot, QThreadPool


class Manage(QObject):
    run_pool = QThreadPool()

    def __init__(self):
        super().__init__()

    @Slot()
    def run(self):
        self.run_pool.setMaxThreadCount(5)
