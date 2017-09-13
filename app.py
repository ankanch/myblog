import os
from config import config as CFG
from time import sleep

WORKERS_COUNT = 6
WORKERS_TIMEOUT = 180 # seconds


if "mode.server" in os.listdir("./"):
    # when a specific file in current dir,bind IP below  
    os.system("/usr/local/bin/gunicorn -w %d -t %d -b %s:8000 index:app"%(WORKERS_COUNT,WORKERS_TIMEOUT,CFG.SITE_HOST))
elif "mode.debug" in os.listdir("../"):
    # used for debug, only run on a single thread
    os.system("python index.py")
else:
    # local machine for test
    os.system("/usr/local/bin/gunicorn -w %d -t %d -b 127.0.0.1:8000 index:app"%(WORKERS_COUNT,WORKERS_TIMEOUT))

while True:
    sleep(36000)