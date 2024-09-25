#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import configparser


class readConfig(object):


    def __init__(self):
        pass

    def readConfi(self,item,key):
        """
        读取配置文件中的conf路径
        :param item:
        :param key:
        :return:
        """
        self.cf = configparser.ConfigParser()
        self.cf.read("././conf/conf.ini")
        value = self.cf.get(item, key)
        return str(value)
