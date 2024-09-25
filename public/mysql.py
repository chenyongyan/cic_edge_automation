#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import pymysql
from rediscluster import RedisCluster
from public.readConfig import readConfig

class mysql:

    def __init__(self):
        self.readConfig = readConfig()
        ConfPath = self.readConfig.readConfi("Path","conf_dir")
        File = open(name=ConfPath + "config.json", mode='r', encoding='UTF-8')
        self.file = json.load(File)


    def redisDB(self,excType="GET",conmmandText="",setName="",setValue="",getName=""):
        """Redis集群操作"""
        startup_nodes = [
            {"host": "10.16.4.115", "port": 7001},
            {"host": "10.16.4.115", "port": 7002},
            {"host": "10.16.4.115", "port": 7003},
            {"host": "10.16.4.115", "port": 7004},
            {"host": "10.16.4.115", "port": 7005},
            {"host": "10.16.4.115", "port": 7006},
        ]
        redisExc = RedisCluster(startup_nodes=startup_nodes,decode_responses=True,skip_full_coverage_check=True)
        if excType in ["DELETE","delete"]:
            redisExc.delete(conmmandText)
        elif excType in ["SET","set"]:
            redisExc.set(name=setName,value=setValue)
        elif excType in ["GET","get"]:
            redisExc.get(getName)


    def mysqlDB(self,excType="SELECT",sql=""):
        """
        SHOW DATABASES
        SHOW TABELS FROM DATABASES
        """
        try:
            db = pymysql.connect(
                host=self.file["mysql"]["host"],
                user=self.file["mysql"]["user"],
                port=self.file["mysql"]["port"],
                password=self.file["mysql"]["password"],
                database=self.file["mysql"]["database"],
            )
            cursor = db.cursor(pymysql.cursors.DictCursor)
            if excType in ["SELECT","select"]:
                cursor.execute(sql)
                desc = cursor.description
                result = cursor.fetchall()
                if result == ():
                    print(desc)
                    print("查询无数据。")
                else:
                    count = 0
                    print()
                    for i in result:
                        count += 1
                        print("{}".format(i))
                    print("查询完毕！共检索出{}条结果。".format(count))
                    db.close()
                    return result
            else:
                cursor.execute('SET FOREIGN_KEY_CHECKS=0;')
                cursor.execute(sql)
                cursor.execute('SET FOREIGN_KEY_CHECKS=1;')
                db.commit()
                print("{} 语句提交成功！".format(sql))
        except Exception as err:
            print(err)


