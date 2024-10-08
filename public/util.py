#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pandas,json,os,openpyxl,requests,time
from loguru import logger
from public.device import device
from public.deviceName import deviceName
from public.gatewayContrler import gatewayContrler
from public.deviceContrler import deviceContrler
from public.readConfig import readConfig


class util:

    def __init__(self):
        self.device = device()
        self.deviceName = deviceName()
        self.gatewayContrler = gatewayContrler()
        self.deviceContrler = deviceContrler()
        self.readConfig = readConfig()
        ConfPath = self.readConfig.readConfig("Path","conf_dir")
        File = open(file=ConfPath + "config.json", mode='r', encoding='UTF-8')
        self.jsondata = json.load(File)
        self.time_list = []


    def get_key(self,d,value):
        """
        通过字典中的value获取key返回list
        :param d:
        :param value:
        :return:
        """
        key = [k for k, v in d.items() if v == value]
        return key


    def get_device_mid(self):
        """
        获取数据表格测试设备mid
        :param :
        :return:
        """
        for root , dirs, files in os.walk(self.readConfig.readConfi("Path","file_dir")):
            for name in files:
                if name.endswith(".xlsx"):
                    pass
                elif name.endswith(".xls"):
                    pass
                elif name.endswith(".csv"):
                    pass
                else:
                    os.remove(os.path.join(root, name))
        test_file_list =  os.listdir(self.readConfig.readConfi("Path","file_dir"))
        for fileName in test_file_list:
            os.path.join('{}{}'.format(test_file_list, fileName))
            wb = openpyxl.load_workbook(self.readConfig.readConfi("Path","file_dir") + fileName)
            sheet_names_list = wb.sheetnames
            for sheet_name in sheet_names_list:
                if sheet_name != "配置文件":
                    pd = pandas.read_excel(io=self.readConfig.readConfi("Path","file_dir") + fileName, sheet_name=sheet_name,keep_default_na=False)
                    for rows in pd.index.values:
                        d = dict()
                        list_mid = []
                        d['key5'] = pd.iloc[rows, 4]
                        textTestDevice = str(d['key5']).replace("\n", "").replace(" ","").replace("，",",")
                        list_mid.append(textTestDevice)
                        str_mid = str(list_mid).replace("['","{").replace("']","}")
                        TestDevice = eval(str(str_mid))
                        return TestDevice


    def test_setup(self, case_title):
        """
        测试初始化
        :param test_title:
        :return:
        """
        if str(case_title) == "初始队列":
            self.device.modify_device(mid=self.jsondata['母管压力变送器'], code=self.jsondata['母管压力参数码'], value='7')
            enableArray = self.jsondata['enableArray']
            enableArrayText = str(enableArray).replace('false', "False")
            enableArrayData = eval(str(enableArrayText))
            url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['modifyByGeteway']
            body = {"groupId": self.jsondata['groupID'], "jointEnable": False, "enableArray": enableArrayData}
            response = requests.post(url=url, json=body, headers=None, verify=False)
            try:
                text = str(response.text).replace("false", "False").replace("true", "True").replace("null", "None")
                jsonData = eval(str(text))
                assert jsonData['ret'] == 1
                logger.info('所有设备退出智控成功！')
            except AssertionError:
                logger.error('所有设备退出智控失败！')
                logger.warning('返回信息：{}'.format(response.text))
            logger.info('停机所有设备...')
            devicemid = self.jsondata['devicemid']
            for mid in devicemid:
                self.device.controler_device(mid=str(mid),type=6)
                self.device.controler_device(mid=str(mid),type=8)
                self.deviceContrler.device_stop(mid=str(mid))
            time.sleep(5)

    def device_setup(self, device_status):
        """
        设备条件
        :param deviceStatus:
        :return:
        """
        device_mid = self.get_device_mid()
        if deviceStatus != {}:
            jsonData = eval(str(device_status))
            for state in jsonData.keys():
                if state == '停机':
                    get_device_type = jsonData.get('停机')
                    jointEnable_device_list = []
                    for device_type in get_device_type:
                        mid = device_mid.get(device_type)
                        self.device.controler_device(mid=str(mid), type=2)
                        jointEnable_device_list.append({"enable": True, "mid": str(mid)})
                    gatway_url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['modifyByGeteway']
                    gatwaybodyTrue = {"groupId": self.jsondata['groupID'],"enableArray": jointEnable_device_list}
                    r = requests.post(url=gatway_url, json=gatwaybodyTrue, headers=None, verify=False)
                    text = str(r.text).replace("false", "False").replace("true", "True").replace("null", "None")
                    gatway_data = eval(str(text))
                    assert gatway_data['ret'] == 1

                if state == '运行':
                    get_device_type = jsonData.get('运行')
                    jointEnable_device_list = []
                    for device_type in get_device_type:
                        mid = device_mid.get(device_type)
                        self.device.controler_device(mid=str(mid), type=1)
                        jointEnable_device_list.append({"enable": True, "mid": str(mid)})
                    gatway_url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['modifyByGeteway']
                    gatwaybodyTrue = {"groupId": self.jsondata['groupID'], "enableArray": jointEnable_device_list}
                    r = requests.post(url=gatway_url, json=gatwaybodyTrue, headers=None, verify=False)
                    text = str(r.text).replace("false", "False").replace("true", "True").replace("null", "None")
                    gatway_data = eval(str(text))
                    assert gatway_data['ret'] == 1

                if state == '卸载':
                    get_device_type = jsonData.get('卸载')
                    jointEnable_device_list = []
                    for device_type in get_device_type:
                        mid = device_mid.get(device_type)
                        self.device.controler_device(mid=str(mid), type=4)
                        jointEnable_device_list.append({"enable": True, "mid": str(mid)})
                    gatway_url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['modifyByGeteway']
                    gatwaybodyTrue = {"groupId": self.jsondata['groupID'], "enableArray": jointEnable_device_list}
                    r = requests.post(url=gatway_url, json=gatwaybodyTrue, headers=None, verify=False)
                    text = str(r.text).replace("false", "False").replace("true", "True").replace("null", "None")
                    gatway_data = eval(str(text))
                    assert gatway_data['ret'] == 1

                if state == '加载':
                    get_device_type = jsonData.get('加载')
                    jointEnable_device_list = []
                    for device_type in get_device_type:
                        mid = device_mid.get(device_type)
                        self.device.controler_device(mid=str(mid),type=3)
                        jointEnable_device_list.append({"enable": True, "mid": str(mid)})
                    gatway_url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['modifyByGeteway']
                    gatwaybodyTrue = {"groupId": self.jsondata['groupID'], "enableArray": jointEnable_device_list}
                    r = requests.post(url=gatway_url, json=gatwaybodyTrue, headers=None, verify=False)
                    text = str(r.text).replace("false", "False").replace("true", "True").replace("null", "None")
                    gatway_data = eval(str(text))
                    assert gatway_data['ret'] == 1

                if state == '非智控停机':
                    get_device_type = jsonData.get('非智控停机')
                    jointEnable_device_list = []
                    for device_type in get_device_type:
                        mid = device_mid.get(device_type)
                        self.device.controler_device(mid=str(mid), type=2)
                        jointEnable_device_list.append({"enable": False, "mid":mid})
                    gatway_url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['modifyByGeteway']
                    gatwaybodyTrue = {"groupId": self.jsondata['groupID'],"enableArray": jointEnable_device_list}
                    r = requests.post(url=gatway_url, json=gatwaybodyTrue, headers=None, verify=False)
                    text = str(r.text).replace("false", "False").replace("true", "True").replace("null", "None")
                    gatway_data = eval(str(text))
                    assert gatway_data['ret'] == 1

                if state == '非智控运行':
                    get_device_type = jsonData.get('非智控运行')
                    jointEnable_device_list = []
                    for device_type in get_device_type:
                        mid = device_mid.get(device_type)
                        self.device.controler_device(mid=str(mid), type=1)
                        jointEnable_device_list.append({"enable": False, "mid":mid})
                    gatway_url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['modifyByGeteway']
                    gatwaybodyTrue = {"groupId": self.jsondata['groupID'],"enableArray": jointEnable_device_list}
                    r = requests.post(url=gatway_url, json=gatwaybodyTrue, headers=None, verify=False)
                    text = str(r.text).replace("false", "False").replace("true", "True").replace("null", "None")
                    gatway_data = eval(str(text))
                    assert gatway_data['ret'] == 1


    def gatway_setup(self, gatway_status):
        """
        网关初始化
        :param gatway_status:
        :return:
        """
        if gatway_status != {}:
            gatway_info = eval(str(gatway_status))
            gatway_url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['modifyByGeteway']
            jointEnable = gatway_info.get('智控状态')
            if str(jointEnable) == "开启":
                gatwaybodyTrue = {
                    "groupId": self.jsondata['groupID'],
                    "jointEnable": True,
                    "upLimitPress": gatway_info.get('母管上限压力'),
                    "endPress": gatway_info.get('母管下限压力'),
                    "pressDrop": "",
                    "safePress": "",
                    "startInterval": gatway_info.get('启动时间间隔'),
                    "stopInterval": gatway_info.get('停机时间间隔')
                }
                r = requests.post(url=gatway_url, json=gatwaybodyTrue, headers=None, verify=False)
                try:
                    text = str(r.text).replace("false", "False").replace("true", "True").replace("null", "None")
                    gatway_data = eval(str(text))
                    assert gatway_data['ret'] == 1
                    logger.info('网关条件初始化成功！')
                except AssertionError:
                    logger.error('网关条件初始化失败！')
                    logger.error('请求报文：{}'.format(gatwaybodyTrue))
                    logger.warning('返回信息：{}'.format(r.text))
            elif str(jointEnable) == "关闭":
                gatwaybodyFalse = {
                    "groupId": self.jsondata['groupID'],
                    "jointEnable": False,
                    "upLimitPress": gatway_info.get('母管上限压力'),
                    "endPress": gatway_info.get('母管下限压力'),
                    "pressDrop": "",
                    "safePress": "",
                    "startInterval": gatway_info.get('启动时间间隔'),
                    "stopInterval": gatway_info.get('停机时间间隔')
                }
                r = requests.post(url=gatway_url, json=gatwaybodyFalse, headers=None, verify=False)
                try:
                    text = str(r.text).replace("false", "False").replace("true", "True").replace("null", "None")
                    gatway_data = eval(str(text))
                    assert gatway_data['ret'] == 1
                    logger.info('网关条件初始化成功！')
                except AssertionError:
                    logger.error('网关条件初始化失败！')
                    logger.error('请求报文：{}'.format(gatwaybodyFalse))
                    logger.warning('返回信息：{}'.format(r.text))

            for val in gatway_info.keys():
                if val == str('瞬时流量'):
                    Instantaneous_flow = gatway_info.get(str(val))
                    self.device.modify_device(mid='1020070060', code='Instantaneous_flow', value=str(Instantaneous_flow))

                if val == str('累计流量'):
                    TOTAL = gatway_info.get(str(val))
                    self.device.modify_device(mid='1020070060', code='TOTAL', value=str(TOTAL))


    def test_setpe(self, test_setpe, test_title):
        """
        操作步骤
        :param Setpe:
        :param Title:
        :return:
        """
        device_mid = util.get_device_mid(self)
        if test_setpe != {}:
            setpes = eval(str(test_setpe))
            for setpe in setpes.keys():
                if setpe == "智控状态":
                    join_state = setpes.get(setpe)
                    if str(join_state) == "开启":
                        gatway_url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['modifyByGeteway']
                        gatwaybody = {"groupId": self.jsondata['groupID'], "jointEnable": True}
                        r = requests.post(url=gatway_url, json=gatwaybody, headers=None, verify=False)
                        text = str(r.text).replace("false", "False").replace("true", "True").replace("null", "None")
                        gatway_data = eval(str(text))
                        try:
                            assert gatway_data['ret'] == 1
                            logger.info('智控总开关开启成功！')
                        except AssertionError:
                            logger.error('智控总开关开启失败！')
                            logger.warning('请求报文：{}'.format(gatwaybody))
                            logger.warning('返回信息：{}'.format(r.text))
                            break

                    if str(join_state) == "关闭":
                        gatway_url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['modifyByGeteway']
                        gatwaybody = {"groupId": self.jsondata['groupID'], "jointEnable": False}
                        r = requests.post(url=gatway_url, json=gatwaybody, headers=None, verify=False)
                        text = str(r.text).replace("false", "False").replace("true", "True").replace("null", "None")
                        gatway_data = json.loads(str(text))
                        try:
                            assert gatway_data['ret'] == 1
                            logger.info('智控总开关关闭成功！')
                        except AssertionError:
                            logger.error('智控总开关关闭失败！')
                            logger.warning('请求报文：{}'.format(gatwaybody))
                            logger.warning('返回信息：{}'.format(r.text))
                            break

                if setpe == "母管压力":
                    self.device.modify_device(mid=self.jsondata["母管压力变送器"],code=self.jsondata["母管压力参数码"],value=str(setpes.get(setpe)))

                if setpe == "等待时间":
                    excel_wait_time = setpes.get(str(setpe))
                    if Title == "初始队列":
                        self.time_list.clear()
                    else:
                        pass

                    if self.time_list == []:
                        logger.warning("当前需要等待：{}s".format(excel_wait_time))
                        count = 0
                        while True:
                            count += 1
                            time.sleep(1)
                            logger.info("已经等待{}s".format(count))
                            if count == excel_wait_time:
                                self.time_list.clear()
                                self.time_list.append(excel_wait_time)
                                break
                    else:
                        wait = int(excel_wait_time) - int(self.time_list[0])
                        logger.warning("当前需要等待：{}s".format(wait))
                        count = 0
                        while True:
                            count += 1
                            time.sleep(1)
                            logger.info("已经等待{}s".format(count))
                            if count == wait:
                                self.time_list.append(excel_wait_time)
                                self.time_list.remove(self.time_list[0])
                                break

                if setpe == "在线设备":
                    online_device_list = setpes.get(setpe)
                    for online_device in online_device_list:
                        for device_name in device_mid.keys():
                            if str(online_device) == str(device_name):
                                mid = device_mid.get(str(device_name))
                                self.device.controler_device(mid=str(mid), type=8)

                if setpe == "模拟器停机":
                    stop_device_list = setpes.get(setpe)
                    for stop_device in stop_device_list:
                        for device_name in device_mid.keys():
                            if str(stop_device) == str(device_name):
                                mid = device_mid.get(str(device_name))
                                self.device.controler_device(mid=str(mid), type=2)

                if setpe == "模拟器运行":
                    run_device_list = setpes.get(setpe)
                    for run_device in run_device_list:
                        for device_name in device_mid.keys():
                            if str(run_device) == str(device_name):
                                mid = device_mid.get(str(device_name))
                                self.device.controler_device(mid=str(mid), type=1)

                if setpe == "网关运行":
                    run_device_list = setpes.get(setpe)
                    for run_device in run_device_list:
                        for device_name in device_mid.keys():
                            if str(run_device) == str(device_name):
                                mid = device_mid.get(str(device_name))
                                self.gatewayContrler.controlDeviceByGeteway(mid=str(mid),type=1)

                if setpe == "网关停机":
                    run_device_list = setpes.get(setpe)
                    for run_device in run_device_list:
                        for device_name in device_mid.keys():
                            if str(run_device) == str(device_name):
                                mid = device_mid.get(str(device_name))
                                self.gatewayContrler.controlDeviceByGeteway(mid=str(mid), type=2)

                if setpe == "离线设备":
                    offline_device_list = setpes.get(setpe)
                    for offline_device in offline_device_list:
                        for device_name in device_mid.keys():
                            if str(offline_device) == str(device_name):
                                mid = device_mid.get(str(device_name))
                                self.device.controler_device(mid=str(mid), type=7)

                if setpe == "锁定设备":
                    lock_device_list = setpes.get(setpe)
                    for lock_device in lock_device_list:
                        for device_name in device_mid.keys():
                            if str(device_name) == str(lock_device):
                                mid = device_mid.get(str(device_name))
                                self.device.controler_device(mid=str(mid), type=5)

                if setpe == "解锁设备":
                    unlock_device_list = setpes.get(setpe)
                    for unlock_device in unlock_device_list:
                        for device_name in device_mid.keys():
                            if str(device_name) == str(unlock_device):
                                mid = device_mid.get(str(unlock_device))
                                self.device.controler_device(mid=str(mid), type=6)

                if setpe == "退出智控":
                    unJoin_device_list = setpes.get(setpe)
                    for unJoin_device in unJoin_device_list:
                        for device_name in device_mid.keys():
                            if str(unJoin_device) == str(device_name):
                                mid = device_mid.get(str(device_name))
                                enableArray = []
                                enableArray.append({"enable": False, "mid": str(mid)})
                                gatway_url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['modifyByGeteway']
                                gatway_body = {"groupId": self.jsondata['groupID'],"enableArray": enableArray}
                                r = requests.post(url=gatway_url, json=gatway_body, headers=None, verify=False)
                                name = self.deviceName.get_device_name(mid=str(mid))
                                try:
                                    text = str(r.text).replace("false","False").replace("true","True").replace("null","None")
                                    gatway_data = json.loads(str(text))
                                    assert gatway_data['ret'] == 1
                                    logger.info('{}退出智控成功！'.format(name))
                                except AssertionError:
                                    logger.error('{}退出智控失败！'.format(name))
                                    logger.warning('返回信息：{}'.format(r.text))
                                    break

                if setpe == "加入智控":
                    join_device_list = setpes.get(setpe)
                    for join_device in join_device_list:
                        for device_name in device_mid.keys():
                            if str(join_device) == str(device_name):
                                mid = device_mid.get(str(device_name))
                                enableArray = []
                                enableArray.append({"enable": True, "mid": str(mid)})
                                gatway_url = self.jsondata['url'] + self.jsondata['gatewayPort'] + self.jsondata['gateway']['modifyByGeteway']
                                gatway_body = {"groupId": self.jsondata['groupID'],"enableArray": enableArray}
                                r = requests.post(url=gatway_url, json=gatway_body, headers=None, verify=False)
                                name = self.deviceName.get_device_name(mid=str(mid))
                                try:
                                    text = str(r.text).replace("false","False").replace("true","True").replace("null","None")
                                    gatway_data = json.loads(str(text))
                                    assert gatway_data['ret'] == 1
                                    logger.info('{}加入智控成功！'.format(name))
                                except AssertionError:
                                    logger.error('{}加入智控失败！'.format(name))
                                    logger.warning("请求报文：{}".format(gatway_body))
                                    logger.warning('返回信息：{}'.format(r.text))
                                    break

                if setpe == "累计流量":
                    TOTAL = setpes.get(str(setpe))
                    self.device.modify_device(mid='1020070060',code='TOTAL',value=str(TOTAL))

                if setpe == "瞬时流量":
                    Instantaneous_flow = setpes.get(str(setpe))
                    self.device.modify_device(mid='1020070060',code='Instantaneous_flow',value=str(Instantaneous_flow))

                if setpe == "运行时间":
                    run_time_list = setpes.get(setpe)[0]
                    for run_device in run_time_list:
                        runtime = run_time_list.get(str(run_device))
                        for device_name in device_mid.keys():
                            if str(device_name) == str(run_device):
                                mid = device_mid.get(str(device_name))
                                self.device.modify_device(mid=str(mid),code="runTime",value=str(runtime))

                if setpe == "重故障":
                    device_list = setpes.get(setpe)
                    for device_ in device_list:
                        for device_name in device_mid.keys():
                            if str(device_name) == str(device_):
                                mid = device_mid.get(str(device_name))
                                self.device.modify_device(mid=str(mid),code="errorStatus",value=str('1'))

                                # import socket
                                # client = socket.socket()
                                # client.connect(('127.0.0.1',8081))
                                # cmd = '{"cmd":5,"mid":"' + str(mid) + '","x0":["03_1_0_3_4_5_6_7_8_9_10_11_12_13_14_1_16"]}'
                                # client.send(cmd.encode("utf-8"))
                                # client.close()


    def get_gatway_queue_assert(self, test_id, queue_info):
        """
        获取实时队列信息断言
        :param test_id:
        :param queue_info:
        :return:
        """
        if queue_info != {}:
            queue = self.gatewayContrler.get_queue(device_type=1)
            readyqueueList = []
            runqueueList = []
            readyqueuelist_1 = []
            readyqueuelist_2 = []
            readyqueuelist_3 = []
            readyqueuelist_4 = []
            runqueue_1 = []
            runqueue_2 = []
            runqueue_3 = []
            runqueue_4 = []
            Queue = {
                "待机队列":{"1":readyqueuelist_1,"2":readyqueuelist_2,"3":readyqueuelist_3,"4":readyqueuelist_4},
                "运行队列":{"1":runqueue_1,"2":runqueue_2,"3":runqueue_3,"4":runqueue_4}
            }
            try:
                ready__Queue = queue['readyQueue']
                excel_device_mid = util.get_device_mid(self)
                lst = []
                for level_mid in ready__Queue:
                    get_mid_interface = level_mid['mid']
                    for deviceName_mid in excel_device_mid:
                        get_mid_excel = excel_device_mid[deviceName_mid]
                        if str(get_mid_interface) == str(get_mid_excel):
                            n = str(level_mid).replace(str(get_mid_interface), str(deviceName_mid), 10)
                            lst.append(n)
                for alldevice in lst:
                    alldeviceData = eval(alldevice)
                    del alldeviceData['time']
                    readyqueueList.append(alldeviceData)
                    global text
                    for readyQueueDevice in readyqueueList:
                        text = eval(str(readyQueueDevice))
                    if text['level'] == 1:
                        readyqueuelist_1.append(text['mid'])
                    elif text['level'] == 2:
                        readyqueuelist_2.append(text['mid'])
                    elif text['level'] == 3:
                        readyqueuelist_3.append(text['mid'])
                    elif text['level'] == 4:
                        readyqueuelist_4.append(text['mid'])
            except Exception:
                pass
            l3 = []
            l4 = []
            for device in Queue['待机队列'].values():
                if device != []:
                    key = util.get_key(self,d=Queue['待机队列'], value=device)
                    l3.append(key[0])
                    l4.append(device)
            d_readyqueue = dict(zip(l3, l4))
            try:
                run__Queue = queue['runQueue']
                device_mid_text = util.get_device_mid(self)
                lst_run = []
                for m1 in run__Queue:
                    mid1 = m1['mid']
                    for m2 in device_mid_text:
                        mid2 = device_mid_text[m2]
                        if str(mid1) == str(mid2):
                            n = str(m1).replace(str(mid1),str(m2),10)
                            lst_run.append(n)
                for val in lst_run:
                    j = eval(str(val))
                    del j['time']
                    runqueueList.append(j)
                    global textrun
                    for runQueueDevice in runqueueList:
                        textrun = eval(str(runQueueDevice))
                    if textrun['level'] == 1:
                        runqueue_1.append(textrun['mid'])
                    elif textrun['level'] == 2:
                        runqueue_2.append(textrun['mid'])
                    elif textrun['level'] == 3:
                        runqueue_3.append(textrun['mid'])
                    elif textrun['level'] == 4:
                        runqueue_4.append(textrun['mid'])
            except Exception:
                pass
            l1 = []
            l2 = []
            for device in Queue['运行队列'].values():
                if device != []:
                    key = util.get_key(self,d=Queue['运行队列'], value=device)
                    l1.append(key[0])
                    l2.append(device)
            d_runqueue = dict(zip(l1, l2))
            all_queue = {"待机队列":d_readyqueue,"运行队列":d_runqueue}
            logger.info('网关队列信息：{}'.format(all_queue))
            logger.info('期望队列信息：{}'.format(queue_info))
            if all_queue == queue_info:
                logger.warning('用例{}输出网关队列信息与期望队列一致！'.format(test_id))
            else:
                logger.error("用例{}输出网关队列信息与期望队列有差异！".format(test_id))
                print("期望队列信息：{}".format(queue_info))
                print("实际队列信息：{}".format(all_queue))
            assert all_queue == queue_info


