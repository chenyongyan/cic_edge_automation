#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import unittest,time,smtplib,os
from BeautifulReport import BeautifulReport
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from loguru import logger
from public.readConfig import readConfig


class runTest:

    def __init__(self):
        self.readConfig = readConfig()
        self.logPath = self.readConfig.readConfi(item="Path",key="log_dir")
        self.testReportPath = self.readConfig.readConfi(item="Path",key="report_dir")
        self.testCasePath = self.readConfig.readConfi(item="Path",key="testcase_dir")

    def delete(self):
        """删除工程中的垃圾日志和垃圾报告"""
        for logFile in os.listdir(self.logPath):
            os.remove(self.logPath + logFile)
        for self.reportFile in os.listdir(self.testReportPath):
            os.remove(self.testReportPath + self.reportFile)

    def newReport(self,report_dir):
        """"获取工程最新生成的报告"""
        self.lists = os.listdir(report_dir)
        self.lists.sort(key=lambda fn: os.path.getatime(report_dir + "/" + fn))
        self.file_new = os.path.join(report_dir, self.lists[-1])
        return self.file_new

    def sendMail(self,file,STMPServer,From,Password):
        """"将新报告以邮件附件形式发送指定邮箱"""
        self.f = open(file,'rb')
        self.mailbody = self.f.read()
        self.f.close()
        self.stmpserver = STMPServer
        self.user = From
        self.password = Password
        self.subject = '自动化测试报告'
        self.msgRoot = MIMEMultipart()
        self.text_msg = MIMEText(self.mailbody,'html','utf-8')
        self.msgRoot.attach(self.text_msg)
        self.file_msg = MIMEText(self.mailbody,'base64','utf-8')
        self.file_msg["Content-Type"] = 'application/octet-stream'
        self.basename = os.path.basename(file)
        self.file_msg["Content-Disposition"] = 'attachment; filename=''' + self.basename + ''
        self.msgRoot.attach(self.file_msg)
        self.msgRoot['Subject'] = Header(self.subject,'utf-8')
        self.msgRoot['From'] = From
        self.msg_to = ['abc@163.com', 'abc@qq.com', 'abc@qq.com']
        self.msgRoot['To'] = ','.join(self.msg_to)
        self.smtp = smtplib.SMTP()
        self.smtp.connect(self.stmpserver)
        self.smtp.login(self.user, self.password)
        self.smtp.sendmail(self.msgRoot['From'], self.msgRoot['To'], self.msgRoot.as_string())
        self.smtp.quit()

    def main(self):
        """主程序入口"""
        runTest.delete(self)
        self.test_suite = unittest.defaultTestLoader.discover(self.testCasePath, pattern='test*.py')
        self.result = BeautifulReport(self.test_suite)
        self.now = time.strftime("%Y%m%d_%H%M%S")
        self.logName = 'log' + self.now + '.log'
        logger.add(sink=self.logPath + self.logName, format=("{time} {level} {message}"), encoding="UTF-8")
        self.result.report(filename=self.now, description='接口测试用例', report_dir=self.testReportPath,theme='theme_memories')
        self.report = runTest.newReport(self,self.testReportPath)
        #runTest.sendMail(self,file=self.report,STMPServer="",From="",Password="")

if __name__ == '__main__':
    run = runTest()
    run.main()




