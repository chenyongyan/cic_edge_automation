#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import requests,json
from loguru import logger
from public.deviceName import deviceName
from public.readConfig import readConfig


class deviceContrl:

    def __init__(self):
        self.readConfig = readConfig()
        self.deviceName = deviceName()
        ConfPath = self.readConfig.readConfig("Path","conf_dir")
        File = open(file=ConfPath + "config.json", mode='r', encoding='UTF-8')
        self.file = json.load(File)


    def deviceStop(self,mid):
        """
        单设备关机
        :param mid:
        :return:
        """
        name = self.deviceName.deviceMid(mid=str(mid))
        urlGateWay = self.file['url'] + self.file['gatewayPort'] + self.file['gateway']['controlDeviceByGeteway']
        urlByDevice = self.file['url'] + self.file['devicePort'] + self.file['device']['controlByDevice']
        body = {"mid":str(mid), "type":2}
        response = requests.post(url=urlByDevice,json=body,headers=None)
        try:
            text = str(response.text).replace("false", "False").replace("true", "True").replace("null", "None")
            jsonData = json.loads(str(text))
            assert jsonData['ret'] == 1
            logger.info('模拟器停机{}成功！'.format(name))
        except AssertionError:
            logger.error('模拟器停机{}失败！'.format(name))
            logger.warning('请求报文：{}'.format(body))
            logger.warning('返回信息：{}'.format(response.text))
            logger.warning('尝试网关停机设备...')
            responseGateway = requests.post(url=urlGateWay, json=body, headers=None)
            textGateway = str(responseGateway.text).replace("false", "False").replace("true", "True").replace("null", "None")
            GatewayjsonData = eval(str(textGateway))
            try:
                assert GatewayjsonData['ret'] == 1
                logger.info('网关停机{}成功！'.format(name))
            except AssertionError:
                logger.error('网关停机{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(responseGateway.text))


    def deviceRun(self,mid):
        """
        单设备开机
        :param mid:
        :return:
        """
        name = self.deviceName.deviceMid(mid=str(mid))
        urlGateWay = self.file['url'] + self.file['gatewayPort'] + self.file['gateway']['controlDeviceByGeteway']
        urlByDevice = self.file['url'] + self.file['devicePort'] + self.file['device']['controlByDevice']
        body = {"mid":str(mid), "type":1}
        response = requests.post(url=urlByDevice,json=body,headers=None)
        try:
            text = str(response.text).replace("false", "False").replace("true", "True").replace("null", "None")
            jsonData = json.loads(str(text))
            assert jsonData['ret'] == 1
            logger.info('模拟器启动{}成功！'.format(name))
        except AssertionError:
            logger.error('模拟器启动{}失败！'.format(name))
            logger.warning('请求报文：{}'.format(body))
            logger.warning('返回信息：{}'.format(response.text))
            logger.warning('尝试网关启动设备...')
            responseGateway = requests.post(url=urlGateWay, json=body, headers=None)
            textGateway = str(responseGateway.text).replace("false", "False").replace("true", "True").replace("null", "None")
            gatwayJsonData = eval(str(textGateway))
            try:
                assert gatwayJsonData['ret'] == 1
                logger.info('网关启动{}成功！'.format(name))
            except AssertionError:
                logger.info('网关启动{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(responseGateway.text))