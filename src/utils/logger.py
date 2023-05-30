# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025
"""
import logging

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s "  # 配置输出日志格式
DATE_FORMAT = "%Y-%m-%d  %H:%M:%S %a"  # 配置输出时间的格式，注意月份和天数不要搞乱了
logging.basicConfig(level=logging.INFO,
                    format=LOG_FORMAT,
                    datefmt=DATE_FORMAT,
                    filename="start_get.log",  # 有了filename参数就不会直接输出显示到控制台，而是直接写入文件
                    encoding="utf-8",
                    )
logger = logging.getLogger(__name__)
