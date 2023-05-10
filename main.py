# -*- coding: utf-8 -*-

import socket
import struct
import binascii
import re
import time


def awake(mac_address):
    '''
    唤醒远程主机
    :param mac_address: mac地址
    :return:
    '''
    BROADCAST = "192.168.5.1"
    mac_address = mac_address.replace("-", "").replace(":", "")  # 去掉mac地址中的特殊符号
    data = ''.join(['FFFFFFFFFFFF', mac_address * 20])  # 构造原始数据格式
    send_data = b''
    # 把原始数据转换为16进制字节数组，
    for i in range(0, len(data), 2):
        send_data = b''.join([send_data, struct.pack('B', int(data[i: i + 2], 16))])
    # 通过socket广播出去，为避免失败，间隔广播三次
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # socket.SO_BROADCAST
        sock.sendto(send_data, (BROADCAST, 7))
        time.sleep(1)
        sock.sendto(send_data, (BROADCAST, 7))
        time.sleep(1)
        sock.sendto(send_data, (BROADCAST, 7))
        print("唤醒数据已发送")
    except Exception as e:
        print(e)
    finally:
        # 关闭套接字
        sock.close()

def shutdown(mac_address):
    print("关机")

def op(open_flag = "1"):
    # 定义字典
    machine_dict = {
        "1": {"mac": "00:1B:21:0B:3F:6D", "desc": "ML-PC"},
        "2": {"mac": "00:1B:21:0B:3F:6D", "desc": "小艾-PC"},
        "3": {"mac": "00:3e:e1:cb:a2:8f", "desc": "我的垃圾桶"}
    }

    print("请选择要执行的机器:")
    for k, v in machine_dict.items():
        print(k + ". " + v["desc"])

    # 获取用户输入
    choice = input("请输入要执行的机器:")

    # 根据用户输入获取mac地址
    mac_address = machine_dict[choice]["mac"]
    print(f"解析出的mac地址：{mac_address}")
    if mac_address is not None:
        # 唤醒远程主机
        if open_flag == "1":
            awake(mac_address)
            print("唤醒成功")
        elif open_flag == "2":
            shutdown(mac_address)
            print("关机成功")
    else:
        print("机器不存在")

# main
if __name__ == '__main__':
    # 选择操作是开机，还是关机
    print("请选择要执行的操作:")
    print("1. 开机")
    print("2. 关机")
    shut_choice = input("请输入要执行的操作:")
    if shut_choice == "1":
        # 开机
        op("1")
        pass
    elif shut_choice == "2":
        # 关机
        op("2")
        pass


