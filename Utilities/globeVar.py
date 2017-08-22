import sys
sys.path.append("./config")
from config import config as CFG

SUCCESS = "OK"
UNSUCCESS = "U"
VARS = {}

def loadConfig():
    """
    This function is used to load config file from path in ./config/config.py
    """
    with open(CFG.VAR_CONFIG_FILE) as ff:
        for line in ff:
            if line[0] != "#" and len(line)>3:
                line = line.replace("\n","").replace("\r","").split("=")
                if line[0] != "SESSIONS":
                    VARS[line[0]] = line[1]
                else:
                    VARS[line[0]] = line[1].split(",")
    return VARS