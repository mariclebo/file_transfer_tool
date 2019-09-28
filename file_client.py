#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
import os
import hashlib
import json
import time


def get_file_md5(file_path):
    m = hashlib.md5()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(1024)
            if len(data) == 0:
                break    
            m.update(data)
    
    return m.hexdigest().upper()

# while True:
#     try:
#         sock = socket.socket()
#         sock.connect((server_ip, server_port))
#     except:
#         time.sleep(1)
#     else:
#         break

def client_reg_send():
    req = '{"op": 2, "args": {"uname":conf["args"]["uname"], "passwd":conf["args"]["passwd"]}}'
    header = "{:<15}".format(len(req)).encode()
    sock.send(header)
    sock.send(req.encode())

def client_reg_recv():
    data_len = sock.recv(15).decode().rstrip()
    if len(data_len) > 0:
        data_len = int(data_len)
        recv_size = 0
        json_data = b""
        while recv_size < data_len:
            tmp = sock.recv(data_len - recv_size)
            if tmp == 0:
                break
            json_data += tmp
            recv_size += len(tmp)
        
        json_data = json_data.decode()
        rsp = json.loads(json_data)
        if rsp["error_code"] == 0:
            print("注册成功!")
        else:
            print("注册失败!")


def client_login_send():
    req = '{"op": 1, "args": {"uname":conf["args"]["uname"], "passwd":conf["args"]["passwd"], "phone":conf["args"]["phone"], "email":conf["args"]["email"]}}'
    header = "{:<15}".format(len(req)).encode()
    sock.send(header)
    sock.send(req.encode())


def client_login_recv():
    data_len = sock.recv(15).decode().rstrip()
    if len(data_len) > 0:
        data_len = int(data_len)
        recv_size = 0
        json_data = b""
        while recv_size < data_len:
            tmp = sock.recv(data_len - recv_size)
            if tmp == 0:
                break
            json_data += tmp
            recv_size += len(tmp)
        
        json_data = json_data.decode()
        rsp = json.loads(json_data)
        if rsp["error_code"] == 0:
            print("登录成功!")
            while True:
                file_path = sock.recv(300).decode().rstrip()
                if len(file_path) == 0:
                    break

                file_size = sock.recv(15).decode().rstrip()
                if len(file_size) == 0:
                    break
                file_size = int(file_size)

                file_md5 = sock.recv(32).decode()
                if len(file_md5) == 0:
                    break

                # 如果为空文件夹
                if file_size == -1:
                    print("\n成功接收空文件夹 %s" % file_path)
                    os.makedirs(file_path, exist_ok=True)
                    continue

                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                print("\n正在接收文件 %s，请稍候......" % file_path)

                f = open(file_path, "wb")

                recv_size = 0
                while recv_size < file_size:
                    file_data = sock.recv(file_size - recv_size)
                    if len(file_data) == 0:
                        break

                    f.write(file_data)
                    recv_size += len(file_data)

                f.close()

                recv_file_md5 = get_file_md5(file_path)

                if recv_file_md5 == file_md5:
                    print("成功接收文件 %s" % file_path)
                else:
                    print("接收文件 %s 失败（MD5校验不通过）" % file_path)
                    break
            
            sock.close()
            print("接受完成!")
        else:
            print("登录失败!")
    
    

def client_check_user_send():
    req = '{"op": 3, "args": {"uname":conf["args"]["uname"]}}'
    header = "{:<15}".format(len(req)).encode()
    sock.send(header)
    sock.send(req.encode())


def client_check_user_recv():
    data_len = sock.recv(15).decode().rstrip()
    if len(data_len) > 0:
        data_len = int(data_len)
        recv_size = 0
        json_data = b""
        while recv_size < data_len:
            tmp = sock.recv(data_len - recv_size)
            if tmp == 0:
                break
            json_data += tmp
            recv_size += len(tmp)
        
        json_data = json_data.decode()
        rsp = json.loads(json_data)
        if rsp["error_code"] == 0:
            print("用户不存在!")
        elif rsp["error_code"] == 1:
            print("用户已存在!")



def main():
    # 加载配置信息
    global conf
    global sock
    conf = json.load(open("cli_conf.json"))
    sock = socket.socket()
    sock.connect((conf["server_ip"], conf["server_port"]))
    print("用户操作提示!\n1.用户注册;\n2.用户登录;\n3.用户名校验;")

    o = int(input("请输入你想要执行的操作: "))

    if o == 1:
        client_reg_send()
        client_reg_recv()
    elif o == 2:
        client_login_send()
        client_login_recv()
    elif o == 3:
        client_check_user_send()
        client_check_user_recv()
    else:
        pass

if __name__ == "__main__":
    main()











