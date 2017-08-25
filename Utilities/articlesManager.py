from time import gmtime, strftime,time
from Utilities import globeVar
from Utilities import runSQL

def addNewArticle(title,cate,content,keywords,url,draft=False):
    timestr = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    if checkEssentialInfo(url):
        sql = "SELECT * FROM `categories` WHERE`CNAME`='%s'"%cate
        result = runSQL.runSelect(sql)
        if len(result) == 0:
            cate = "未分类"
        sql_update_count = "UPDATE `categories` SET `CACOUNT`=`CACOUNT`+1 WHERE `CNAME`='%s'"%cate
        if draft:
            content = replaceSpecialCharters(content)
            sql = "INSERT INTO `articles`\
                    (`ATITLE`, `ACONTENT`, `ACATEGORY`, `AKEYWORDS`, `AURL`, `AREADINGS`, `DATE`,`DRAFT`,`TRASH`)\
                     VALUES ('%s','%s','%s','%s','%s',0,'%s',1,0)"%(title,content,cate,keywords,url,timestr)
            if runSQL.runInsert(sql):
                return True
            return False,"保存草稿失败，请稍后重试！"
        else:
            content = replaceSpecialCharters(content)
            sql = "INSERT INTO `articles`\
                    (`ATITLE`, `ACONTENT`, `ACATEGORY`, `AKEYWORDS`, `AURL`, `AREADINGS`, `DATE`,`DRAFT`,`TRASH`)\
                     VALUES ('%s','%s','%s','%s','%s',0,'%s',0,0)"%(title,content,cate,keywords,url,timestr)
            #print(sql)
            if runSQL.runInsert(sql):
                runSQL.runUpdate(sql_update_count)
                return True,"文章发布成功"
            return False,"文章发布失败，请稍后重试！"
    return False,"文章和已经发布的文章具有相同的URL"

def updateArticle(xid,title,cate,content,keywords,url):
    content = replaceSpecialCharters(content)
    sql = "UPDATE `articles` SET `ATITLE`='%s',`ACONTENT`='%s',`ACATEGORY`='%s',`AKEYWORDS`='%s',`AURL`='%s',\
            `DRAFT`=0,`TRASH`=0 WHERE `AID`=%s"%(title,content,cate,keywords,url,xid)
    if runSQL.runInsert(sql):
        return True,"文章更新成功"
    return False,"文章更新失败，请稍后重试！"
    

def checkEssentialInfo(url):
    sql = "SELECT * FROM `articles` WHERE `AURL`='%s'"%url
    result = runSQL.runSelect(sql)
    if len(result) > 0:
        return False
    return True

def quickEditArticle(xid,title,cate,url):
    sql = "UPDATE `articles` SET `ATITLE`='%s',`ACATEGORY`='%s',`AURL`='%s' WHERE `AID`=%d"%(title,cate,url,str(xid))
    if runSQL.runUpdate(sql):
        return True
    return False

def deleteArticle(xid):
    sql = "DELETE FROM `articles` WHERE `AID`="+str(xid)
    if runSQL.runDelete(sql):
        return True
    return False

def getArticleByURL(url):
    sql = "SELECT * FROM `articles` WHERE `AURL`='%s'"%url
    result = runSQL.runSelect(sql)
    if len(result) == 0:
        return False,"文章不存在",""
    if result[0][8] == 1 or result[0][9] == 1:
        return False,"文章不可用！",""
    return True,result[0],restoreSpecialCharacter(result[0][2])

def getArticleByID(xid):
    sql = "SELECT * FROM `articles` WHERE `AID`='%s'"%xid
    result = runSQL.runSelect(sql)
    if len(result) == 0:
        return False,"文章不存在",""
    if result[0][8] == 1 or result[0][9] == 1:
        return False,"文章不可用！",""
    return True,result[0],restoreSpecialCharacter(result[0][2])

def getBrief(raw_article):
    raw_article[2] = restoreSpecialCharacter(raw_article[2])
    if len(raw_article[2])>200:
        raw_article[2] = raw_article[2][:200]
    return raw_article


def replaceSpecialCharters(raw):
    charset = globeVar.ARTICLES_SPECIAL_CHAR.keys()
    for ch in charset:
        raw = raw.replace(ch,globeVar.ARTICLES_SPECIAL_CHAR[ch])
    return raw

def restoreSpecialCharacter(ss):
    xcharset = globeVar.ARTICLES_SPECIAL_CHAR.values()
    inv_map = {v: k for k, v in globeVar.ARTICLES_SPECIAL_CHAR.items()}
    for ch in xcharset:
        ss = ss.replace(ch,inv_map[ch])
    return ss

def getArticlesList(num):
    sql = "SELECT * FROM `articles` ORDER BY `DATE` DESC LIMIT %s"%num
    result = [list(article) for article in  runSQL.runSelect(sql)]
    if len(result) > 0:
        return list(map(getBrief,result))
    return result

def getArticlesListD(start,num):
    sql = "SELECT * FROM `articles` ORDER BY `DATE` DESC LIMIT %s,%s"%(start,num)
    result = [list(article) for article in  runSQL.runSelect(sql)]
    if len(result) > 0:
        result = list(map(getBrief,result))
        return result
    return result

def searchArticle(key):
    key = replaceSpecialCharters(key)
    sql = "SELECT  `ATITLE`, `ACONTENT`, `AURL`,  `DATE` FROM `articles` WHERE `ACONTENT` LIKE '%"+ key + "%' or `ATITLE` LIKE '%" + key + "%'"
    result = [[article[0],restoreSpecialCharacter(article[1])[:120],article[2],article[3]] for article in  runSQL.runSelect(sql)]
    return result
