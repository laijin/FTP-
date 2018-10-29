import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import socket
import struct
import json
from config import setting
from login import *
from logg import *

dow_shar_dir=setting.BASE_DIR


def send_filedata(cmds,conn,exist_file_size=0):
    #实现断点传输文件的效果
    filename = cmds[1]
    print(cmds)
    file_path = os.path.join(os.getcwd(), filename)
    f=open(file_path,'rb')
    f.seek(exist_file_size)
    while 1:
        data=f.read(1024)
        if data:
            conn.send(data)
        else:
            break

def get(cmds,conn):
    filename = cmds[1]
    file_path = os.path.join(os.getcwd(), filename)
    # print(file_path)
    if os.path.isfile(file_path):
        file_size = os.path.getsize(file_path)
        print(file_size)
        # 以读的方式打开文件，读取文件内容，发送给客户端
        header_dic = {
            'filename': filename,
            'filemd5': '15e426922f8abc86e8c2e14dd9073346',
            'file_size': file_size,
        }
        obj=conn.recv(4)
        print('////')
        exist_file_size = struct.unpack('i',obj)[0]
        header_json = json.dumps(header_dic)
        header_bytes = header_json.encode('utf-8')
        # print(header_bytes, '===========================')
        header_len = struct.pack('i', len(header_bytes))
        # 2、把报头发送给客户端
        conn.send(header_len)
        conn.send(header_bytes)
        if exist_file_size:
            if exist_file_size !=file_size:
                send_filedata(exist_file_size,cmds,conn)
            else:
                logg('已下载文件')
        else:
            #第一次下载文件
            send_filedata(cmds,conn)

    else:
        #发送数据
        logg('发送数据')
        conn.send(struct.pack('i',0))