from queue import Queue
from threading import Thread
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from config import setting

class MyThread:
    def __init__(self,maxthread=setting.MAXTHREAD):
        self.maxthread = maxthread
        #初始化一个Queue对象
        self.q = self.queue =Queue(maxthread)
        #在队列中存放maxthread个对象，起到线程池的作用
        for i in range(maxthread):
            self.q.put(Thread)

    def put_thread(self):
        self.q.put(Thread)

    def get_thread(self):
        return self.q.get()
# q=MyThread()