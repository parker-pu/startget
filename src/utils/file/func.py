# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025
"""


def tail(filepath, n, reverse=False, block=-1024):
    """
    实现 tail 的功能
    :param filepath:
    :param n:
    :param reverse:
    :param block:
    :return:
    """
    with open(filepath, "rb") as f:
        f.seek(0, 2)
        file_size, all_block = f.tell(), False
        while True:
            if file_size >= abs(block):
                f.seek(block, 2)
                s = f.readlines()
                # 判断是否满足所需行数
                if all_block or len(s) > n:
                    r = s[-n:]
                    if reverse:
                        r.reverse()
                    return r
                else:
                    block *= 2
            else:
                block, all_block = -file_size, True


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
