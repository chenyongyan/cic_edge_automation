#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import unittest,json
import os,openpyxl,pandas
from public.myddt import ddt,data,unpack
from public.method import method
from public.readConfig import readConfig

@ddt
class case(unittest.TestCase):

    def setUp(self):
        self.readConfig = readConfig()
        self.method = method()
        ConfPath = self.readConfig.readConfig("Path", "conf_dir")
        File = open(file=ConfPath + "config.json", mode='r', encoding='UTF-8')
        self.file = json.load(File)
        self.key_list = []


    def testGetValues_01(self):
        """
        返回数据表格值
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
        for root, dirs, files in os.walk(self.readConfig.readConfi("Path","log_dir")):
            for name in files:
                os.remove(os.path.join(root, name))
        for root, dirs, files in os.walk(self.readConfig.readConfi("Path","report_dir")):
            for name in files:
                os.remove(os.path.join(root, name))

        test_file_list =  os.listdir(self.readConfig.readConfi("Path","file_dir"))
        for fileName in test_file_list:
            os.path.join('{}{}'.format(test_file_list, fileName))
            wb = openpyxl.load_workbook(self.readConfig.readConfi("Path","file_dir") + fileName)
            sheet_names_list = wb.sheetnames
            for sheet_name in sheet_names_list:
                if sheet_name == "配置文件":
                    pass
                else:
                    pd = pandas.read_excel(io=self.readConfig.readConfi("Path","file_dir") + fileName, sheet_name=sheet_name,keep_default_na=False)
                    for rows in pd.index.values:
                        d = dict()
                        # 用例编号
                        d['key1'] = pd.iloc[rows, 0]
                        ID = str(d['key1']).replace("\n","").replace(" ","").replace("，",",")

                        # 测试类型
                        d['key2'] = pd.iloc[rows, 1]
                        Subject = str(d['key2']).replace("\n","").replace(" ","").replace("，",",")

                        # 测试点
                        d['key3'] = pd.iloc[rows, 2]
                        Point = str(d['key3']).replace("\n", "").replace(" ","").replace("，",",")

                        # 用例标题
                        d['key4'] = pd.iloc[rows, 3]
                        Title = str(d['key4']).replace("\n", "").replace(" ","").replace("，",",")

                        # 设备MID
                        list_mid = []
                        d['key5'] = pd.iloc[rows, 4]
                        textTestDevice = str(d['key5']).replace("\n", "").replace(" ","").replace("，",",")
                        list_mid.append(textTestDevice)
                        str_mid = str(list_mid).replace("['","{").replace("']","}")
                        TestDevice = eval(str(str_mid))

                        # 设备条件
                        list_deviceSetUp = []
                        d['key6'] = pd.iloc[rows, 5]
                        textdeviceSetUp = str(d['key6']).replace("\n", "").replace(" ","").replace("，",",")
                        list_deviceSetUp.append(textdeviceSetUp)
                        str_deviceSetUp = str(list_deviceSetUp).replace("['", "{").replace("']", "}")
                        deviceSetUp = eval(str(str_deviceSetUp))

                        # 网关条件
                        list_gatwaySetUp = []
                        d['key7'] = pd.iloc[rows, 6]
                        textgatwaySetUp = str(d['key7']).replace("\n", "").replace(" ","").replace("，",",")
                        list_gatwaySetUp.append(textgatwaySetUp)
                        str_gatwaySetUp = str(list_gatwaySetUp).replace("['", "{").replace("']", "}")
                        gatwaySetUp = eval(str(str_gatwaySetUp))

                        # 操作步骤
                        list_Setpe = []
                        d['key8'] = pd.iloc[rows, 7]
                        textSetpe = str(d['key8']).replace("\n","").replace(" ","").replace("，",",")
                        list_Setpe.append(textSetpe)
                        str_Setpe = str(list_Setpe).replace("['", "{").replace("']", "}")
                        Setpe = eval(str(str_Setpe))

                        # 期望输出队列信息
                        list_Queue = []
                        d['key9'] = pd.iloc[rows, 8]
                        textQueue = str(d['key9']).replace("\n", "").replace(" ","").replace("，",",")
                        list_Queue.append(textQueue)
                        str_Queue = str(list_Queue).replace("['", "{").replace("']", "}")
                        Queue = eval(str(str_Queue))
                        self.key_list.append([rows,ID,Subject,Point,Title,TestDevice,deviceSetUp,gatwaySetUp,Setpe,Queue])

        return self.key_list


    @data(*testGetValues_01())
    @unpack
    def testCase_02(self,ID,Title,deviceSetUp,gatwaySetUp,Setpe,Queue):

        # 网关智控初始化
        self.method.testSetUp(caseTitle=Title)

        # 设备条件初始化
        self.method.deviceSetUp(deviceStatus=deviceSetUp)

        # 网关条件初始化
        self.method.gatwaySetUp(gatwayStatus=gatwaySetUp)

        # 用例执行操作步骤
        self.method.testSetpe(Setpe=Setpe, Title=Title)

        # 用例断言
        self.method.getGatwayQueueAssert(test_id=ID, queue_info=Queue)


if __name__=="__main__":
    unittest.main()