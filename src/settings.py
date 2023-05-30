# -*- encoding: utf-8 -*-
"""
@License :   (C)Copyright 2022-2025
"""
import pathlib
import sys

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = "."

if getattr(sys, 'frozen', False):
    # BASE_DIR = os.path.dirname(sys.executable)  # 打包EXE后的运行路径
    BASE_DIR = pathlib.Path(sys.executable).parent.absolute()  # 打包EXE后的运行路径
elif __file__:
    BASE_DIR = pathlib.Path(__file__).parent.parent.absolute()  # 未打包时的运行路径

