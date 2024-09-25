#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import time
from public.readConfig import readConfig
from loguru import logger


class logger_:

    def __init__(self):
        self.readConfig = readConfig()
        self.logPath = self.readConfig.readConfi("Path","log_dir")



    def info_PRINT(self,messges):
        timestap = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        day = time.strftime("%Y-%m-%d", time.localtime())
        logger.info(messges)
        with open(name=str(self.logPath) + str(day) + ".log", mode="a+", encoding="utf-8") as f:
            f.write(str(timestap) + "   | INFO |    " + str(messges) + "\n")
            f.close()


    def warning_PRINT(self,messges):
        timestap = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        day = time.strftime("%Y-%m-%d", time.localtime())
        logger.warning(messges)
        with open(name=str(self.logPath) + str(day) + ".log", mode="a+", encoding="utf-8") as f:
            f.write(str(timestap) + "   | WARNING |    " + str(messges) + "\n")
            f.close()


    def error_PRINT(self,messges):
        timestap = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        day = time.strftime("%Y-%m-%d", time.localtime())
        logger.error(messges)
        with open(name=str(self.logPath) + str(day) + ".log", mode="a+", encoding="utf-8") as f:
            f.write(str(timestap) + "   | ERROR |  " + str(messges) + "\n")
            f.close()





