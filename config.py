#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
全局配置
'''

'''
日志配置
'''
LOG_LEVEL = 'INFO'  # 日志级别 ['DEBUG','WARNING','INFO','ERROR']
LOG_FILE_USE = True  # 日志是否存储到文件
LOG_FILE = 'app'  # 日志存储文件名
LOG_STREAM_USE = True  # 日志是否打印到控制台

'''
MySQL数据库连接配置
'''
DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, TABLE_NAME = (
    '192.168.1.101', 3306, 'paper', 'root', '123456', 'paper')  # MySQL配置

