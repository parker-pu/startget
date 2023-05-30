# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025
"""
import json

from src.settings import BASE_DIR
from src.utils.logger import logger


class Save:

    @staticmethod
    def __save_file(filename, config):
        """
        保存文件
        :param filename: 文件名称
        :param config:
        :return:
        """
        cfp = f"{BASE_DIR}/{filename}.json"
        try:
            with open(cfp, "w") as f:
                f.write(json.dumps(config))
        except Exception as e:
            logger.error(e)

    def save_software_config(self, config):
        """
        保存软件的一些配置信息
        :param config:
        :return:
        """
        self.__save_file("software_config", config)

    def save_history_config(self, config):
        """
        保存下载记录及历史
        :param config:
        :return:
        """
        self.__save_file("history_file", config)
