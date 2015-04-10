#!/bin/env python2.7
#-*- coding=utf-8 -*_

"""
Author: 周宸翰 Hank
Date: 2015-01-03 11:00:43
Bubbles config
"""

import ConfigParser, os, sys


CNF_FILE = ''

################
#读取配置文件
################

class config():

    @staticmethod
    def _CNF(cnf_file):
        cf = ConfigParser.ConfigParser()
        cf.read(cnf_file)
        sec = cf.sections()
        dic = {}
        for i in sec:
            opt = cf.options(i)
            dic[i] = {}
            for m in opt:
                dic[i][m] = cf.get(i,m)
        return dic 
