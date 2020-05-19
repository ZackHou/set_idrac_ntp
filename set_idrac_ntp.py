#! /usr/bin/env python
# -*- coding: utf-8 -*-
# By Zack_Hou, 2020

import os, sys
import subprocess
import time
from threading import Timer
import requests

def run_cmd(cmd, stdout="true", time_out=120):
    """
    Execute shell command.
    """
    result = ""
    pro = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    timer = Timer(time_out, lambda process: process.kill(), [pro])
    try:
        timer.start()
        result = pro.stdout.read()
        if stdout == "true":
            return result
    finally:
        timer.cancel()

#下载racadm安装包
def get_install_racadm_set():

    os_version_6 = run_cmd("cat /etc/redhat-release |grep 'release 6'", 'true')
    os_version_7 = run_cmd("cat /etc/redhat-release |grep 'release 7'", 'true')
    os_version_8 = run_cmd("cat /etc/redhat-release |grep 'release 8'", 'true')

    if os_version_6:
        r = requests.get("https://dl.dell.com/FOLDER05446180M/1/DellEMC-iDRACTools-Web-LX-9.3.0-3379_A00.tar.gz")

        if r.status_code == 200:
            with open('DellEMC-iDRACTools-Web-LX-9.3.0-3379_A00.tar.gz','wb') as code:
                code.write(r.content)
            run_cmd('tar -zxf DellEMC-iDRACTools-Web-LX-9.3.0-3379_A00.tar.gz', 'true')
            run_cmd('rpm -ivh ./iDRACTools/racadm/RHEL6/x86_64/srvadmin-hapi-9.3.0-3379.14516.el6.x86_64.rpm', 'true')
            run_cmd('rpm -ivh ./iDRACTools/racadm/RHEL6/x86_64/srvadmin-argtable2-9.3.0-3379.14516.el6.x86_64.rpm', 'true')
            run_cmd('rpm -ivh ./iDRACTools/racadm/RHEL6/x86_64/srvadmin-idracadm7-9.3.0-3379.14516.el6.x86_64.rpm', 'true')
            print("racadm安装完成")
            #设置iDrac时区为上海
            print("设置时区为Asia/Shanghai")
            run_cmd('/opt/dell/srvadmin/sbin/racadm set iDRAC.Time.Timezone Asia/Shanghai', 'true')
            time.sleep(3)
            #启用iDrac的NTP（1启用0关闭）
            print("开启NTP服务")
            run_cmd('/opt/dell/srvadmin/sbin/racadm set iDRAC.NTPConfigGroup.NTPEnable 1', 'true')
            #设置iDrac NTP服务器1,此处设置的是网上搜的一个阿里的NTP服务器ip，如果需要配置域名NTP地址例如ntp1.aliyun.com，则还需要配置iDrac的dns。
            print("设置NTP1")
            run_cmd('/opt/dell/srvadmin/sbin/racadm set iDRAC.NTPConfigGroup.NTP1 120.25.115.20', 'true')
            # 设置iDrac NTP服务器2此处设置的是网上搜的一个腾讯的NTP服务器ip，如果需要配置域名NTP地址例如time1.cloud.tencent.com，则还需要配置iDrac的dns。
            print("设置NTP2")
            run_cmd('/opt/dell/srvadmin/sbin/racadm set iDRAC.NTPConfigGroup.NTP2 139.199.215.251', 'true')
        else:
            print("CentOS 6 下载iDRACTools-9.3.0失败。")
            return "CentOS 6 下载iDRACTools-9.3.0失败。"
    elif os_version_7:
        r = requests.get("https://dl.dell.com/FOLDER05920767M/1/DellEMC-iDRACTools-Web-LX-9.4.0-3732_A00.tar.gz")

        if r.status_code == 200:
            with open('DellEMC-iDRACTools-Web-LX-9.4.0-3732_A00.tar.gz','wb') as code:
                code.write(r.content)
            run_cmd('tar -zxf DellEMC-iDRACTools-Web-LX-9.4.0-3732_A00.tar.gz', 'true')
            run_cmd('rpm -ivh ./iDRACTools/racadm/RHEL7/x86_64/srvadmin-hapi-9.4.0-3732.15734.el7.x86_64.rpm', 'true')
            run_cmd('rpm -ivh ./iDRACTools/racadm/RHEL7/x86_64/srvadmin-argtable2-9.4.0-3732.15734.el7.x86_64.rpm', 'true')
            run_cmd('rpm -ivh ./iDRACTools/racadm/RHEL7/x86_64/srvadmin-idracadm7-9.4.0-3732.15734.el7.x86_64.rpm', 'true')
            print("racadm安装完成")
            #设置iDrac时区为上海
            print("设置时区为Asia/Shanghai")
            run_cmd('/opt/dell/srvadmin/sbin/racadm set iDRAC.Time.Timezone Asia/Shanghai', 'true')
            time.sleep(3)
            #启用iDrac的NTP（1启用0关闭）
            print("开启NTP服务")
            run_cmd('/opt/dell/srvadmin/sbin/racadm set iDRAC.NTPConfigGroup.NTPEnable 1', 'true')
            # 设置iDrac NTP服务器1,此处设置的是网上搜的一个阿里的NTP服务器ip，如果需要配置域名NTP地址例如ntp1.aliyun.com，则还需要配置iDrac的dns。
            print("设置NTP1")
            run_cmd('/opt/dell/srvadmin/sbin/racadm set iDRAC.NTPConfigGroup.NTP1 120.25.115.20', 'true')
            # 设置iDrac NTP服务器2此处设置的是网上搜的一个腾讯的NTP服务器ip，如果需要配置域名NTP地址例如time1.cloud.tencent.com，则还需要配置iDrac的dns。
            print("设置NTP2")
            run_cmd('/opt/dell/srvadmin/sbin/racadm set iDRAC.NTPConfigGroup.NTP2 139.199.215.251', 'true')
        else:
            print("CentOS 7 下载iDRACTools-9.4.0失败。")
            return "CentOS 7 下载iDRACTools-9.4.0失败。"
    elif os_version_8:
        r = requests.get("https://dl.dell.com/FOLDER05920767M/1/DellEMC-iDRACTools-Web-LX-9.4.0-3732_A00.tar.gz")

        if r.status_code == 200:
            with open('DellEMC-iDRACTools-Web-LX-9.4.0-3732_A00.tar.gz', 'wb') as code:
                code.write(r.content)
            run_cmd('tar -zxf DellEMC-iDRACTools-Web-LX-9.4.0-3732_A00.tar.gz', 'true')
            run_cmd('rpm -ivh ./iDRACTools/racadm/RHEL8/x86_64/srvadmin-hapi-9.4.0-3732.15734.el8.x86_64.rpm', 'true')
            run_cmd('rpm -ivh ./iDRACTools/racadm/RHEL8/x86_64/srvadmin-argtable2-9.4.0-3732.15734.el8.x86_64.rpm',
                    'true')
            run_cmd('rpm -ivh ./iDRACTools/racadm/RHEL8/x86_64/srvadmin-idracadm7-9.4.0-3732.15734.el8.x86_64.rpm',
                    'true')
            # 设置iDrac时区为上海
            print("设置时区为Asia/Shanghai")
            run_cmd('/opt/dell/srvadmin/sbin/racadm set iDRAC.Time.Timezone Asia/Shanghai', 'true')
            time.sleep(3)
            # 启用iDrac的NTP（1启用0关闭）
            print("开启NTP服务")
            run_cmd('/opt/dell/srvadmin/sbin/racadm set iDRAC.NTPConfigGroup.NTPEnable 1', 'true')
            # 设置iDrac NTP服务器1,此处设置的是网上搜的一个阿里的NTP服务器ip，如果需要配置域名NTP地址例如ntp1.aliyun.com，则还需要配置iDrac的dns。
            print("设置NTP2")
            run_cmd('/opt/dell/srvadmin/sbin/racadm set iDRAC.NTPConfigGroup.NTP1 120.25.115.20', 'true')
            # 设置iDrac NTP服务器2此处设置的是网上搜的一个腾讯的NTP服务器ip，如果需要配置域名NTP地址例如time1.cloud.tencent.com，则还需要配置iDrac的dns。
            print("设置NTP2")
            run_cmd('/opt/dell/srvadmin/sbin/racadm set iDRAC.NTPConfigGroup.NTP2 139.199.215.251', 'true')
        else:
            print ("CentOS 8 下载iDRACTools-9.4.0失败。")
            return "CentOS 8 下载iDRACTools-9.4.0失败。"
    else:
        print("不支持的操作系统。")
        return "failed"

#判断机型
def if_model():
    dell_model = run_cmd("dmidecode -t 1|grep 'Dell'", 'true')
    if dell_model:
        print("开始设置iDrac NTP和时区设置")
        if get_install_racadm_set() == "failed":
            print("不支持的操作系统。")
    else:
         print("It's not a dell server")

if __name__ == '__main__':
    if_model()
