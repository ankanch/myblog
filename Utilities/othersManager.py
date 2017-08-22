from Utilities import runSQL
from Utilities import adminManager

def getBasicInfo():
    sql_articles = "SELECT COUNT(*) FROM `articles`"
    sql_categories = "SELECT COUNT(*) FROM `categories`"
    sql_readings = "SELECT SUM(`AREADINGS`) FROM `articles`"
    last_login = adminManager.getLastLogin()
    articl_sum = runSQL.runSelect(sql_articles)[0][0]
    cate_sum = runSQL.runSelect(sql_categories)[0][0]
    readings_sum = runSQL.runSelect(sql_readings)[0][0]
    return [articl_sum,cate_sum,readings_sum,last_login]
