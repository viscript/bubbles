#!/bin/env python2.7
#-*- coding=utf-8 -*_

#debug 调试信息
#info 基本信息
#warning 警告信息
#error 错误信息
#critical 严重错误信息

import logging, sys, os

class Loger:

    """

    """

    #Loger Initialization
    def __init__(self, FILE_PATH,
                       LOG_LOWEST_RANK = logging.DEBUG,
                       LOG_PATH = "log",
                       LOG_FILE_NAME = "bubbles.log",
                       CONSOLE_RANK = logging.DEBUG,
                       LOG_FILE_RANK = logging.DEBUG
                       ):
        # private args
        self.FILE_PATH = FILE_PATH
        self.LOG_LOWEST_RANK = LOG_LOWEST_RANK
        self.LOG_PATH = LOG_PATH
        self.LOG_FILE_NAME = LOG_FILE_NAME
        self.CONSOLE_RANK = CONSOLE_RANK
        self.LOG_FILE_RANK = LOG_FILE_RANK

        # Create a logger
        self.logger = logging.getLogger('mylogger')
        self.logger.setLevel(self.LOG_LOWEST_RANK)


        
        # Create a logger hanlde，put the logs to the log file
        fh = logging.FileHandler(FILE_PATH + '/' + LOG_PATH + '/' + LOG_FILE_NAME)
        fh.setLevel(self.LOG_FILE_RANK)

        # Create another logger hanlde，Put the logs on the console
        ch = logging.StreamHandler()
        ch.setLevel(self.CONSOLE_RANK)


        # define the format handler of output 
        formatter_log = logging.Formatter(fmt='[%(asctime)s] - %(levelname)s - %(message)s') #, datefmt='%Y-%m-%d %H:%M:%S.%F')
        formatter_con = logging.Formatter(fmt='[%(asctime)s %(levelname)s] > %(message)s', datefmt='%H:%M:%S')

        fh.setFormatter(formatter_log)
        ch.setFormatter(formatter_con)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def D(self, DEBUG):
        self.logger.debug(DEBUG)

    def I(self, INFO):
        self.logger.info(INFO)

    def W(self, WARNING):
        self.logger.warning(WARNING)

    def E(self, ERROR):
        self.logger.error(ERROR)

    def C(self, CRITICAL):
        self.logger.critical(CRITICAL)
