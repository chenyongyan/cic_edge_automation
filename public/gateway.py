#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import requests,json,time
from loguru import logger
from public.deviceName import deviceName
from public.readConfig import readConfig


class gateway:

    def __init__(self):
        self.deviceName = deviceName()
        self.readConfig = readConfig()
        ConfPath = self.readConfig.readConfig("Path","conf_dir")
        File = open(file=ConfPath + "config.json", mode='r', encoding='UTF-8')
        self.jsondata = json.load(File)


    def controlDeviceByGeteway(self,mid,type):
        """
        设备控制
        :param mid:
        :param type: 控制类型 1：启动，2：停机，3：加载，4：加载
        :return:
        """
        name = self.deviceName.deviceMid(mid=str(mid))
        url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['controlDeviceByGeteway']
        body = {"mid":str(mid),"type":type}
        response = requests.post(url=url,json=body,headers=None)
        try:
            text = str(response.text).replace("false", "False").replace("true", "True").replace("null", "None")
            jsonData = json.loads(str(text))
            assert jsonData['ret'] == 1
            if type == 1:
                device_run_time = int(time.time())
                gm = time.gmtime(device_run_time)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", gm)
                logger.warning('设备{}启动时间：{}'.format(name,dt))
                logger.info('网关启动设备{}成功！'.format(name))
            elif type == 2:
                logger.info('网关停机设备{}成功！'.format(name))
            elif type == 3:
                logger.info('网关加载设备{}成功！'.format(name))
            elif type == 4:
                logger.info('网关卸载设备{}成功！'.format(name))
            elif type == 5:
                logger.info('网关锁定设备{}成功！'.format(name))
            elif type == 6:
                logger.info('网关解锁设备{}成功！'.format(name))
            elif type == 7:
                logger.info('网关离线设备{}成功！'.format(name))
            elif type == 8:
                logger.info('网关在线设备{}成功！'.format(name))
            return jsonData
        except AssertionError:
            if type == 1:
                logger.error('网关启动设备{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))
            elif type == 2:
                logger.error('网关停机设备{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))
            elif type == 3:
                logger.error('网关加载设备{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))
            elif type == 4:
                logger.error('网关卸载设备{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))
            elif type == 5:
                logger.error('网关锁定设备{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))
            elif type == 6:
                logger.error('网关解锁设备{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))
            elif type == 7:
                logger.error('网关离线设备{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))
            elif type == 8:
                logger.error('网关在线设备{}失败！'.format(name))
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))


    def getDeviceDataByGeteway(self,mid):
        """
        设备数据查询(对应的数据查看设备对应协议)
        :param mid:
        :return:
        """
        url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['getDeviceDataByGeteway']
        body = {"mid":str(mid),"code":""}
        response = requests.post(url=url,json=body,headers=None,verify=False)
        try:
            text = str(response.text).replace("false", "False").replace("true", "True").replace("null", "None")
            jsonData = json.loads(str(text))
            assert jsonData['ret'] == 1
            return jsonData
        except AssertionError:
            logger.error('获取网关设备数据详情失败！')
            logger.warning('请求报文：{}'.format(body))
            logger.warning('返回信息：{}'.format(response.text))


    def getGateWayData(self):
        """
        网关系统数据查询,参数设置页面所有参数
        :return:
        """
        url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['gatewayData']
        body = {"groupId":self.jsondata['groupID']}
        response = requests.post(url=url,json=body,headers=None,verify=False)
        try:
            text = str(response.text).replace("false", "False").replace("true", "True").replace("null", "None")
            jsonData = eval(text)
            assert jsonData['ret'] == 1
            if jsonData['jointEnable'] == True:
                logger.info('总智控开关状态：开启')
            if jsonData['jointEnable'] == False:
                logger.info('总智控开关状态：关闭')
            logger.info('上限压力：{}'.format(jsonData['upLimitPress']))
            logger.info('下限压力：{}'.format(jsonData['endPress']))
            logger.info('设备启动间隔：{}s'.format(jsonData['startInterval']))
            logger.info('设备停机间隔：{}s'.format(jsonData['stopInterval']))
            return jsonData
        except AssertionError:
            logger.error('获取网关参数设置页面数据详情失败！')
            logger.warning('请求报文：{}'.format(body))
            logger.warning('返回信息：{}'.format(response.text))


    def getQueue(self,device_type):
        """
        智控队列详情
        :param device_type: 队列类型，1：空压机算法，2：干燥机算法
        :return:
        """
        url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['joinQueue']
        body = {"groupId":self.jsondata['groupID'],"type":device_type}
        response = requests.post(url=url,json=body,headers=None,verify=False)
        try:
            text = str(response.text).replace("false", "False").replace("true", "True").replace("null", "None")
            jsonData = json.loads(str(text))
            assert jsonData['ret'] == 1
            if device_type == 1:
                logger.info('获取空压机智控队列信息成功！')
            elif device_type == 2:
                logger.info('获取干燥机智控队列信息成功！')
            return jsonData
        except AssertionError:
            if device_type == 1:
                logger.error('获取空压机智控队列信息失败！')
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))
            elif device_type == 2:
                logger.error('获取干燥机智控队列信息失败！')
                logger.warning('请求报文：{}'.format(body))
                logger.warning('返回信息：{}'.format(response.text))


    def sendProtocol(self,version):
        """
        更新配置文件
        :param version: 版本号,version不传时,默认更到当前同步版本, 更新成功后网关程序自动重启
        :return:
        """
        url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['protocolAndGatewayRestart']
        body = {"groupId":self.jsondata['groupID'],"version":version}
        response = requests.post(url=url,json=body,headers=None,verify=False)
        try:
            text = str(response.text).replace("false", "False").replace("true", "True").replace("null", "None")
            jsonData = json.loads(str(text))
            assert jsonData['ret'] == 1
            logger.info('网关更新配置文件成功！')
            logger.info('当前配置文件版本号：{}'.format(version))
            return jsonData
        except AssertionError:
            logger.error('网关更新配置文件失败！')
            logger.warning('请求报文：{}'.format(body))
            logger.warning('返回信息：{}'.format(response.text))


    def modifyGeteway(self,jointEnable,upLimitPress,endPress,startInterval,stopInterval,enableArray):
        """
        网关系统参数修改
        :param jointEnable: 系统智控状态
        :param upLimitPress: 上限压力
        :param endPress: 末端压力
        :param startInterval: 启动间隔
        :param stopInterval: 停机间隔
        :param enableArray: [{"enable":False,"mid":"1020070085"},{"enable":False,"mid":"1020070084"},{"enable":False,"mid":"1020070083"},{"enable":False,"mid":"1020070082"}]
        :return:
        """
        url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['modifyByGeteway']
        body = {"groupId":self.jsondata['groupID'],
                "jointEnable":jointEnable,
                "upLimitPress":upLimitPress,
                "endPress":endPress,
                "pressDrop":"",
                "safePress":"",
                "startInterval":startInterval,
                "stopInterval":stopInterval,
                "enableArray": enableArray,
                }
        response = requests.post(url=url,json=body,headers=None,verify=False)
        try:
            text = str(response.text).replace("false", "False").replace("true", "True").replace("null", "None")
            jsonData = json.loads(str(text))
            assert jsonData['ret'] == 1
            logger.info('修改网关参数设置页面参数数据成功！')
            return jsonData
        except AssertionError:
            logger.error('修改网关参数设置页面参数数据失败！')
            logger.warning('请求报文：{}'.format(body))
            logger.warning('返回信息：{}'.format(response.text))


