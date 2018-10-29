import socket,os
import struct
import json,os,hashlib,sys
from logg import *
from get import *

def client():
    #主逻辑
    from config import setting
    print(setting.PORT)
    phone=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    phone.connect((setting.HOST,setting.PORT))

    while 1:
        #发命令
        msg=input('--')
        if not msg:continue
        phone.send(msg.encode('utf-8'))
        cmds=msg.split()
        if cmds[0] == 'get':
            get(cmds,phone)

    phone.close()

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    sys.path.append(BASE_DIR)
    client()