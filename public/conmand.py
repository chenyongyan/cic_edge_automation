#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import time
import paramiko
from public.readConfig import readConfig
from paramiko.client import SSHClient,AutoAddPolicy


class conmand:

    def __init__(self):
        self.readConfig = readConfig()
        self.logPath = self.readConfig.readConfi(item="Path",key="log_dir")
        self.ssh_host = self.readConfig.readConfi(item="ssh",key="ssh_host")
        self.ssh_port = self.readConfig.readConfi(item="ssh",key="ssh_port")
        self.ssh_user = self.readConfig.readConfi(item="ssh", key="ssh_user")
        self.ssh_pwd = self.readConfig.readConfi(item="ssh", key="ssh_pwd")



    def curl(self,method="", url="", data=None, headers={}):
        timestap = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        day = time.strftime("%Y-%m-%d", time.localtime())
        ret_list = []
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        if method in ["POST","post"]:
            headerList = []
            for k, v in headers.items():
                header = "-H '{}'".format(str(k) + ":" + str(v))
                headerList.append(header)
            Curl = "curl -i -X{} '{}' -d '{}' {}".format(method,url,data," ".join(headerList))
            with open(name=str(self.logPath) + str(day) + ".log", mode="a+", encoding="utf-8") as f:
                f.write(str(timestap)+"| INFO |" + str(Curl) + "\n")
                f.close()
            client.connect(hostname=self.ssh_host,port=self.ssh_port,username=self.ssh_user,password=self.ssh_pwd)
            stdin, stdout, stderr = client.exec_command(Curl)
            for line in stdout:
                ret_list.append(str(line).replace("\r","").strip("\n"))
            with open(name=str(self.logPath) + str(day) + ".log", mode="a+", encoding="utf-8") as f1:
                f1.write(str(timestap) + "| INFO |" + str(ret_list[-1]) + "\n")
                f1.write("\n")
                f1.close()
            client.close()
            if str(ret_list[0][9:12]) != "200":
                return ret_list[0]
            else:
                result=eval(str(ret_list[-1]).replace("null","None").replace("false","False").replace("true","True").replace("\\",""))
                return result
        if method in ["GET","get"]:
            headerList = []
            for k, v in headers.items():
                header = "-H '{}'".format(str(k) + ":" + str(v))
                headerList.append(header)
            Curl = "curl -i -X{} '{}' {}".format(method,url," ".join(headerList))
            with open(name=str(self.logPath) + str(day) + ".log", mode="a+", encoding="utf-8") as f:
                f.write(str(timestap)+"| INFO |" + str(Curl) + "\n")
                f.close()
            client.connect(hostname=self.ssh_host,port=self.ssh_port,username=self.ssh_user,password=self.ssh_pwd)
            stdin, stdout, stderr = client.exec_command(Curl)
            for line in stdout:
                ret_list.append(str(line).replace("\r","").strip("\n"))
            with open(name=str(self.logPath) + str(day) + ".log", mode="a+", encoding="utf-8") as f1:
                f1.write(str(timestap) + "| INFO |" + str(ret_list[-1]) + "\n")
                f1.write("\n")
                f1.close()
            client.close()
            if str(ret_list[0][9:12]) != "200":
                return ret_list[0]
            else:
                result=eval(str(ret_list[-1]).replace("null","None").replace("false","False").replace("true","True").replace("\\",""))
                return result



    def run_cmd(self,command):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(hostname=self.ssh_host,port=self.ssh_port,username=self.ssh_user,password=self.ssh_pwd)
        stdin, stdout, stderr = client.exec_command(command)
        return stdout.read().decode() # "unicode-escape"





