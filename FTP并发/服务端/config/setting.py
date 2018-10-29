import os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST='127.0.0.1'
PORT=8880
USER_HOME_DIR = os.path.join(BASE_DIR,'home')
ACCOUNT_FILE=r'%s\config\accounts.ini' %BASE_DIR
MAX_SOCKET_LISTEN=5
MAXTHREAD=3