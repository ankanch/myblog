from Utilities import runSQL
from Utilities import adminManager
from Utilities import globeVar  # the site.cfg has been preloaded in this module's VAR dict
import sys
sys.path.append("./config")
from config import config as CFG

def getBasicInfo():
    sql_articles = "SELECT COUNT(*) FROM `articles`"
    sql_categories = "SELECT COUNT(*) FROM `categories`"
    sql_readings = "SELECT SUM(`AREADINGS`) FROM `articles`"
    last_login = adminManager.getLastLogin()
    articl_sum = runSQL.runSelect(sql_articles)[0][0]
    cate_sum = runSQL.runSelect(sql_categories)[0][0]
    readings_sum = runSQL.runSelect(sql_readings)[0][0]
    return [articl_sum,cate_sum,readings_sum,last_login]

def updateSiteInfo(name,copyrightx):
    setSiteSettingInfo("SITE_TITLE",name)
    setSiteSettingInfo("SITE_FOTTER_COPYRIGHT",copyrightx)
    saveSiteSettingInfoChanges()


def getSiteSettingInfo(name):
    if type(name) == list:
        return [globeVar.VARS[n][0] for n in name]
    return globeVar.VARS[name][0]

def setSiteSettingInfo(name,value):
    globeVar.VARS[name][0] = value
    return name
def saveSiteSettingInfoChanges():
    raw_str = ""
    for k,v in globeVar.VARS.items():
        raw_str = k + v[1]  + str(v[0]) + "\r\n"
    with open(CFG.VAR_CONFIG_FILE,"w") as ff:
        ff.write(raw_str)