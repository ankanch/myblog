import sys
sys.path.append("./config")
from config import config as CFG

SUCCESS = "OK"
UNSUCCESS = "U"
VARS = {}

ARTICLES_SPECIAL_CHAR = {
    "\"":"xASC_DQ",
    "'":"xASC_SQ",
    "`":"xASC_CQ",
    "&":"xASC_AND",
    ")":"xASC_RS",
    "(":"xASC_LS",
    "[":"xASC_RR",
    "]":"xASC_LR",
}

def loadConfig():
    """
    This function is used to load config file from path in ./config/config.py
    """
    with open(CFG.VAR_CONFIG_FILE) as ff:
        for line in ff:
            if line[0] != "#" and len(line)>3:
                line = line.replace("\n","").replace("\r","").split("=")
                VARS[line[0]] = line[1]
    return VARS

loadConfig()