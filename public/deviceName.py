#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class deviceName:

    def __init__(self):
        pass

    def get_device_name(self,mid):
        """
        根据mid返回对应设备名称
        :param mid:
        :return:
        """
        if mid == '1020070059':
            return '59#压力变送器'
        elif mid == '1020070047':
            return '47#空压机'
        elif mid == '1020070048':
            return '48#空压机'
        elif mid == '1020070049':
            return '49#空压机'
        elif mid == '1020070050':
            return '50#空压机'
        elif mid == '1020070051':
            return '51#空压机'
        elif mid == '1020070052':
            return '52#冷干机'
        elif mid == '1020070053':
            return '53#冷干机'
        elif mid == '1020070054':
            return '54#冷干机'
        elif mid == '1020070055':
            return '55#水冷机组'
        elif mid == '1020070056':
            return '56#阀门'
        elif mid == '1020070057':
            return '57#阀门'
        elif mid == '1020070058':
            return '58#阀门'
        elif mid == '1020070060':
            return '60#流量计'


    def get_protocol_code(self,code):
        """
        根据code返回对应参数名称
        :param code:
        :return:
        """
        if code == 'busPressureBar':
            return '母管压力'
        elif code == "Instantaneous_flow":
            return "瞬时流量"
        elif code == "TOTAL":
            return "累计流量"
        elif code == "runTime":
            return "累计运行时间"
        elif code == "runStatus":
            return "运行状态"
        elif code == "errorStatus":
            return "故障状态"
        elif code == "maintainStatus":
            return "保养状态"
