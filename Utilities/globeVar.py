import sys
sys.path.append("./config")
from config import config as CFG

VARS = {}

def loadConfig():
    """
    This function is used to load config file from path in ./config/config.py
    """
    with open(CFG.VAR_CONFIG_FILE) as ff:
        for line in ff:
            if line[0] != "#":
                line = line.replace("\n","").replace("\r","").split("=")
                VARS[line[0]] = line[1]
    return VARS