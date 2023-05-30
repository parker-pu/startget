# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025
"""
import json
from pathlib import Path

from src.settings import BASE_DIR
from src.utils.logger import logger


class Load:

    @staticmethod
    def __load_file(filename) -> dict:
        """
        加载文件
        :param filename:
        :return:
        """
        cfp = f"{BASE_DIR}/{filename}.json"
        if Path(cfp).exists():
            try:
                return json.load(open(cfp, "r"))
            except Exception as e:
                logger.error(e)
                return {}
        return {}

    def load_software_config(self) -> dict:
        """
        加载软件保存的信息
        :return:
        """
        return self.__load_file("software_config")

    def load_history_config(self) -> dict:
        """
        加载下载记录
        :return:
        """
        return self.__load_file("history_file")
