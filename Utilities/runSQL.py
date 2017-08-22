import pymysql as SQL
import sys
sys.path.append("./config")
from config import config as CFG

DBCONN = SQL.connect(host=CFG.VAR_DB_HOST, port=3306,user=CFG.VAR_DB_USER,passwd=CFG.VAR_DB_PASSWORD,db=CFG.VAR_DB_NAME,charset='UTF8')

def runSelect(sql):
    #DBCONN = SQL.connect(host=CFG.VAR_DB_HOST, port=3306,user=CFG.VAR_DB_USER,passwd=CFG.VAR_DB_PASSWORD,db=CFG.VAR_DB_NAME,charset='UTF8')
    result = []
    with DBCONN.cursor() as CUR:
        CUR.execute(sql)
        DBCONN.commit()
        result = CUR.fetchall()
    #DBCONN.close()
    return result

def runInsert(sql):
    #DBCONN = SQL.connect(host=CFG.VAR_DB_HOST, port=3306,user=CFG.VAR_DB_USER,passwd=CFG.VAR_DB_PASSWORD,db=CFG.VAR_DB_NAME,charset='UTF8')
    with DBCONN.cursor() as CUR:
        try:
            CUR.execute(sql)
            DBCONN.commit()
        except:
            DBCONN.close()
            return False
    #DBCONN.close()
    return True

def runDelete(sql):
    #DBCONN = SQL.connect(host=CFG.VAR_DB_HOST, port=3306,user=CFG.VAR_DB_USER,passwd=CFG.VAR_DB_PASSWORD,db=CFG.VAR_DB_NAME,charset='UTF8')
    with DBCONN.cursor() as CUR:
        try:
            CUR.execute(sql)
            DBCONN.commit()
        except:
            DBCONN.close()
            return False
    #DBCONN.close()
    return True

def runUpdate(sql):
    #DBCONN = SQL.connect(host=CFG.VAR_DB_HOST, port=3306,user=CFG.VAR_DB_USER,passwd=CFG.VAR_DB_PASSWORD,db=CFG.VAR_DB_NAME,charset='UTF8')
    with DBCONN.cursor() as CUR:
        try:
            CUR.execute(sql)
            DBCONN.commit()
        except:
            DBCONN.close()
            return False
    #DBCONN.close()
    return True