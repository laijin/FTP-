import hashlib
def login(func):
    def inner(*args,**kwargs):
        username = input("用户名:")
        password = input("密码:")
        f = open('userinfo', encoding='utf-8')
        password = bytes(password, encoding='utf-8')
        try:
            for line in f:
                name, pwd ,pwd_md5= line.strip().split('|')
                md5=hashlib.md5(password)
                md=md5.hexdigest()
                if username == name and  pwd_md5 == md:
                    return func(*args, **kwargs)
            else:
                print('输入错误')
        except ValueError:
            print('无此人或密码错误')

    return inner