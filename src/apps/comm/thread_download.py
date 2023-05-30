# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025
下载线程
"""
from pathlib import Path

import requests
from PySide6.QtCore import QRunnable, Signal

from src.utils.file.load import Load
from src.utils.file.save import Save


class ThreadDownload(QRunnable):
    download_progress = Signal(int)
    uuid = None
    url = None
    file_name = None
    file_path = None
    kwargs = None
    paused = False
    cancelled = False

    def __init__(self, uuid, url, file_name, file_path, *args, **kwargs):
        super().__init__()
        self.uuid = uuid
        self.url = url
        self.file_name = file_name
        self.file_path = file_path
        self.kwargs = kwargs

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def cancel(self):
        self.cancelled = True

    def save_progress(self, finish_rate):
        """
        保存进度
        :param finish_rate:
        :return:
        """
        fl, sv, new_data, f_exists = Load(), Save(), [], False
        for row in fl.load_history_config():
            if not isinstance(row, dict):
                continue
            if row.get("uuid") == self.uuid:
                row["progress"] = finish_rate
                row["Status"] = "Finish" if int(finish_rate) == 1 else "Download"
                f_exists = True
            new_data.append(row)
        if not f_exists:
            row = self.kwargs
            row["uuid"] = self.uuid
            row["progress"] = finish_rate
            new_data.append(row)
        sv.save_history_config(config=new_data)

    def run(self):
        """
        开始下载
        :return:
        """
        with requests.get(self.url, stream=True) as r:
            r.raise_for_status()  # 检测下载是否成功
            total_size, finish_size = int(r.headers.get("Content-Length", 0)), 0
            Path(self.file_path).mkdir(parents=True, exist_ok=True)  # 如果不存在就创建目录
            with open(str(Path(self.file_path).joinpath(self.file_name)), "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if self.paused or self.cancelled:
                        return
                    if chunk:
                        f.write(chunk)
                        finish_size += 8192
                        # 存入进度
                        self.save_progress(finish_rate=round(finish_size / total_size, 2))
