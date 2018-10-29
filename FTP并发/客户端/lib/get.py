import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import socket
import struct
import json,os,hashlib
from config import setting
from logg import *

dow_shar_dir=setting.BASE_DIR

def write_file(f,get_size,file_size,phone):
    #读取文件
    while get_size<file_size:
        res=phone.recv(8192)
        f.write(res)
        get_size+=len(res)
        float_rate=float(get_size)/float(file_size)
        rat_part=round(float_rate*100,2)
        sys.stdout.write('下载中%s...\n'%rat_part)
        sys.stdout.flush()

def verification_filemd5(filemd5,filename):
    #对文件进行加密以及判断文件MD5是否一致
    file_path = os.path.join(dow_shar_dir, filename)
    print(file_path)
    f=open(file_path,'rb')
    filedata=f.read()
    md5 = hashlib.md5(filedata)
    md=md5.hexdigest()
    if md == filemd5:
        print('下载文件成功')
    else:
        print('下载文件失败')

def appendfile_content(file_path,temp_file_size,file_size,phone):
    #文件断点追加内容
    f=open(file_path,'ab')
    f.seek(temp_file_size)
    get_size = temp_file_size
    while get_size < file_size:
        res=phone.recv(8192)
        f.write(res)
        get_size+=len(res)
        float_rate=float(get_size)/float(file_size)
        rat_part=round(float_rate*100,2)
        sys.stdout.write('下载中%s...\n'%rat_part)
        sys.stdout.flush()

def recv_file_header(header_size,phone):
    #接收文件的报头，对报头进行处理，返回filename,file_size,filemd5
    header_type=phone.recv(header_size)
    header_dic=json.loads(header_type)
    total_size=header_dic['file_size']
    filename=header_dic['filename']
    filemd5=header_dic['filemd5']
    return (filename,total_size,filemd5)

def get(cmds,phone):
    #exp: get 序列化.png
    filename = cmds[1]
    file_path = os.path.join(dow_shar_dir, filename)
    if os.path.isfile(file_path):  # 如果文件存在，支持续传功能
        temp_file_size = os.path.getsize(file_path)
        phone.send(struct.pack('i', temp_file_size))
        header_size = struct.unpack('i', phone.recv(4))[0]
        if header_size:
            filename, file_size, filemd5 = recv_file_header(header_size,phone)
            if temp_file_size == file_size:#判断是否下载完成
                print('此文件已经存在')
            else:
                print('继续下载文件')
                appendfile_content(file_path, temp_file_size,file_size,phone)
                verification_filemd5(filemd5,filename)#判断MD5是否一致
        else:
            logg('文件已经下载完')
    else:  # 如果文件不存在，则是直接下载
        phone.send(struct.pack('i', 0))
        obj = phone.recv(1024)
        header_size = struct.unpack('i', obj)[0]
        if header_size == 0:
            print("\033[31;1mfile does not exist!\033[0m")
        else:
            filename, file_size, filemd5 = recv_file_header(header_size,phone)
            download_filepath = os.path.join(dow_shar_dir, filename)
            with open(download_filepath, 'wb') as f:
                get_size = 0
                write_file(f, get_size, file_size,phone)
            verification_filemd5(filemd5,filename)