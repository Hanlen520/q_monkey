#! /usr/bin/python
# @Time    : 6/4/18 2:02 AM
# @Author  : Xiangwei Sun
# @FileName: file.py
# @Software: PyCharm
import os
import logging


class FileUtil(object):
    def __init__(self, file, method='w+'):
        self.file = file
        self.method = method
        self.file_handler = None
