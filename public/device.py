#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import requests,json
import time
from loguru import logger
from public.deviceName import deviceName
from public.readConfig import readConfig

class device:

    def __init__(self):
        self.readConfig = readConfig()
        self.deviceName = deviceName()
        ConfPath = self.readConfig.readConfi("Path","conf_dir")
        File = open(file=ConfPath + "config.json", mode='r', encoding='UTF-8')
        self.file = json.load(File)


    def controlByDevice(self,mid,type):
        """
        设备控制
        :param mid:
        :param type: 1：启动，2：停机，3：加载，4：卸载，5：锁定，6：解锁，7：离线，8：在线
        :return:
        """
        name = self.deviceName.deviceMid(mid=str(mid))
        url = self.file['url'] + self.file['devicePort'] + self.file['device']['controlByDevice']
        body = {"mid":str(mid),"type":type}
        response = requests.post(url=url,json=body,headers=None,verify=False)
        try:
            text = eval(str(response.text).replace("false", "False").replace("true", "True").replace("null", "None"))
            assert text['ret'] == 1
            if type == 1:
                device_run_time = int(time.time())
                gm = time.gmtime(device_run_time)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", gm)
                logger.warning('设备{}启动时间：{}'.format(name,dt))
                logger.info('模拟器启动{}成功！'.format(name))
            elif type == 2:
                logger.info('模拟器停机{}成功！'.format(name))
            elif type == 3:
                logger.info('模拟器加载{}成功！'.format(name))
            elif type == 4:
                logger.info('模拟器卸载{}成功！'.format(name))
            elif type == 5:
                logger.info('模拟器锁定{}成功！'.format(name))
            elif type == 6:
                logger.info('模拟器解锁{}成功！'.format(name))
            elif type == 7:
                logger.info('模拟器离线{}成功！'.format(name))
            elif type == 8:
                logger.info('模拟器在线{}成功！'.format(name))
        except AssertionError:
            if type == 1:
                logger.error('模拟器启动{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))
            elif type == 2:
                logger.error('模拟器停机{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))
            elif type == 3:
                logger.error('模拟器加载{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))
            elif type == 4:
                logger.error('模拟器卸载{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))
            elif type == 5:
                logger.error('模拟器锁定{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))
            elif type == 6:
                logger.error('模拟器解锁{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))
            elif type == 7:
                logger.error('模拟器离线{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))
            elif type == 8:
                logger.error('模拟器在线{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))


    def modify(self,mid,code,value):
        """
        修改设备临时参数
        busPressureBar: 母管压力
        Instantaneous_flow: 工况瞬时流量
        TOTAL: 累计流量
        :param mid:
        :param code: code码
        :param value:
        :return:
        """
        name = self.deviceName.deviceMid(mid=str(mid))
        pressure = self.deviceName.protocolCode(code=str(code))
        url = self.file['url'] + self.file['devicePort'] + self.file['device']['modify']
        body = {"mid":str(mid),"code":str(code),"value":value}
        response = requests.post(url=url,json=body,headers=None,verify=False)
        try:
            text = str(response.text).replace("false", "False").replace("true", "True").replace("null", "None")
            jsonData = eval(str(text))
            assert jsonData['ret'] == 1
            logger.info('{}修改{}成功！'.format(name,pressure))
            logger.info('当前{}值为：{}'.format(pressure,value))
            return jsonData
        except AssertionError:
            logger.error('{}修改{}失败！'.format(name,pressure))
            logger.warning('请求报文：{}'.format(body))
            logger.warning('返回信息：{}'.format(response.text))


    def getDeviceDataByDevice(self,mid,code):
        """
        设备信息查询
        :param mid:
        :param code: 协议参数码
        :return:
        """
        name = self.deviceName.deviceMid(mid=str(mid))
        pressure = self.deviceName.protocolCode(code=str(code))
        url = self.file['url'] + self.file['devicePort'] + self.file['device']['getDeviceDataByDevice']
        body = {"mid":str(mid),"code":str(code)}
        response = requests.post(url=url,json=body,headers=None,verify=False)
        try:
            text = str(response.text).replace("false", "False").replace("true", "True").replace("null", "None")
            jsonData = json.loads(str(text))
            assert jsonData['ret'] == 1
            logger.info('当前{}值为：{}'.format(pressure,jsonData['data'][code]))
            return jsonData
        except AssertionError:
            logger.error('获取{}{}失败！'.format(name,pressure))
            logger.warning('请求报文：{}'.format(body))
            logger.warning('返回信息：{}'.format(response.text))


    def deviceRestart(self,status):
        """
        重启边缘模拟器
        :param type_restart: 0:关闭,1:重启
        :return:
        """
        url = self.file['url'] + self.file['devicePort'] + self.file['device']['deviceRestart']
        body = {"type":status}
        response = requests.post(url=url,json=body,headers=None,verify=False)
        try:
            text = str(response.text).replace("false", "False").replace("true", "True").replace("null", "None")
            jsonData = json.loads(str(text))
            assert jsonData['ret'] == 1
            if type == 0:
                logger.info('关闭模拟器成功！')
            elif type == 1:
                logger.info('重启模拟器成功！')
            return jsonData
        except AssertionError:
            if type == 0:
                logger.error('关闭模拟器失败！')
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))
            elif type == 1:
                logger.error('重启模拟器失败！')
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))


    def unlockedDevice(self,mid):
        """
        解锁设备
        :param mid:
        :return:
        """
        equepment = self.deviceName.deviceMid(mid=str(mid))
        device.controlByDevice(mid=str(mid),type=6)
        enableArray = [{"enable":False,"mid":str(mid)}]
        url = self.file['url'] + self.file['gatewayPort'] + self.file['gateway']['modifyByGeteway']
        body = {"groupId":self.file['groupID'],"enableArray": enableArray}
        response = requests.post(url=url,json=body,headers=None,verify=False)
        try:
            text = str(response.text).replace("false", "False").replace("true", "True").replace("null", "None")
            jsonData = json.loads(str(text))
            assert jsonData['ret'] == 1
            logger.info('{}退出智控成功！'.format(equepment))
        except Exception:
            logger.info('{}退出智控失败！'.format(equepment))
            logger.warning('请求报文：{}'.format(body))
            logger.warning('返回信息：{}'.format(response.text))
        enable = [{"enable":True,"mid": str(mid)}]
        urlJoin = self.file['url'] + self.file['gatewayPort'] + self.file['gateway']['modifyByGeteway']
        bodyJoin = {"groupId":self.file['groupID'],"enableArray": enable}
        responseJoin = requests.post(url=urlJoin, json=bodyJoin, headers=None, verify=False)
        try:
            textJoin = str(responseJoin.text).replace("false", "False").replace("true", "True").replace("null", "None")
            joinjsonData = json.loads(str(textJoin))
            assert joinjsonData['ret'] == 1
            logger.info('{}加入智控成功！'.format(equepment))
        except Exception:
            logger.error('{}加入智控失败！'.format(equepment))
            logger.warning('请求报文：{}'.format(body))
            logger.warning('返回信息：{}'.format(response.text))


