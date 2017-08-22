from Utilities import runSQL

def checkExistence(cate_name,cate_url):
    sql = "SELECT `CNAME`,`CURL` FROM `categories` WHERE `CNAME`='%s' OR `CURL`='%s'"%(cate_name,cate_url)
    result = runSQL.runSelect(sql)
    if len(result) == 0:
        return True
    return False

def addNewCate(cate_name,cate_url):
    sql = "INSERT INTO `categories`( `CNAME`, `CACOUNT`, `CURL`) VALUES ('%s',0,'%s')"%(cate_name,cate_url)
    if runSQL.runInsert(sql):
        return True
    return False

def deleteCate(xid):
    sql = "DELETE FROM `categories` WHERE `CID`=" + str(xid)
    if runSQL.runDelete(sql):
        return True
    return False

def changeCate(xid,new_name,new_url):
    sql  = "UPDATE `categories` SET `CNAME`='%s',`CURL`='%s' WHERE `CID`=%s"%(new_name,new_url,str(xid))
    if runSQL.runUpdate(sql):
        return True
    return False

def getAllCates():
    sql = "SELECT * FROM `categories` WHERE 1"
    result = runSQL.runSelect(sql)
    return result