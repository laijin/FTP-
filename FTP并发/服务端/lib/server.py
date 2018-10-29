import socket
import os, sys
import struct
import json
from login import *
from logg import *
from get import *
import mythread

def Communication(pool,conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data: break
            print('客户端的数据为', data)

            cmds = data.decode('utf-8').split()
            if cmds[0] == 'get':
                get(cmds, conn)
        except ConnectionResetError:
            break
    pool.put_thread()
    conn.close()

# @login
def server():
    from config import setting
    phone=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    phone.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    phone.bind((setting.HOST,setting.PORT))

    phone.listen(setting.MAX_SOCKET_LISTEN)
    print('>>>')
    while True:
        conn,client_addr=phone.accept()
        t=pool.get_thread()
        #使用线程对象创建线程
        obj = t(target=Communication, args=(pool,conn,))
        obj.start()  # 启动线程

    phone.close()
if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    sys.path.append(BASE_DIR)
    pool=mythread.MyThread()
    server()

