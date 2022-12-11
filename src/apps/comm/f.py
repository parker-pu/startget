# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025
"""


def convert_size(text: int) -> str:
    """
    文件大小单位换算
    :text: 文件字节
    :return: 返回字节大小对应单位的数值
    """
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = 1024
    for i in range(len(units)):
        if (text / size) < 1:
            return "%.2f%s" % (text, units[i])  # 返回值保留小数点后两位
        text = text / size
