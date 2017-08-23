from time import gmtime, strftime,time
from Utilities import runSQL
from Utilities import globeVar

SESSION_EXPIRES = 3600*int(globeVar.VARS["LOGIN_EXPIRES"])

def getLastLogin():
    sql = "SELECT `LASTLOGIN` FROM `admin` WHERE 1"
    result = runSQL.runSelect(sql)
    return result[0][0]

def updateLastLogin():
    timestr = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    sql = "UPDATE `admin` SET `LASTLOGIN`='%s' WHERE 1"%timestr
    if runSQL.runUpdate(sql):
        return True
    return False

def loginAdmin(username,password):
    """
    1:account locked,0:login success,-1:password or username not correct.
    """
    sql = "SELECT `USERNAME`, `PASSWORD`,`LOCKED`,`SESSIONS` FROM `admin` WHERE 1"
    result = runSQL.runSelect(sql)[0]
    if result[0]==username and result[1]==password:
        if result[2] == 1:
            return 1,"账户被锁定！"
        updateLastLogin()
        return 0,result[3]
    return -1,"用户名或者密码不正确，请重新输入！<br>连续5次输入错误账户将会被锁定。"


def checkSession(session):
    """t
    check a given session is valid
    """
    session_list,raw = getAdminSessions()
    for saved in session_list:
        #print(saved,session)
        if len(saved)==2 and saved[0] == session:
            if (time() - float(saved[1])) < SESSION_EXPIRES:
                return True
    return False

def addSession(new_session):
    """t
    """
    parsed,raw = getAdminSessions()
    new_session_raw_string = raw[0][0] + "," + new_session + "@" + str(time())
    sql = "UPDATE `admin` SET `SESSIONS`='%s' WHERE 1"%new_session_raw_string
    if runSQL.runUpdate(sql):
        return True
    return False

def deleteSession(src_session):
    """t
    """
    parsed,raw = getAdminSessions()
    new_session_list = []
    for sd in parsed:
        if sd[0] == src_session:
            continue
        new_session_list.append(sd)
    x = [ "@".join(sd) for sd in new_session_list]
    ins_str = ",".join(x)
    if len(ins_str)>0 and ins_str[-1] != ",":
        ins_str += ","
    sql = "UPDATE `admin` SET `SESSIONS`='%s' WHERE 1"%ins_str
    if runSQL.runUpdate(sql):
        return True
    return False

def deleteOutofDateSessions():
    """t
    """
    parsed,raw = getAdminSessions()
    new_session_list = []
    for sd in parsed:
        if len(sd)==2 and (time() - float(sd[1]))> SESSION_EXPIRES:
            continue
        new_session_list.append(sd)
    x = [ "@".join(sd) for sd in new_session_list]
    ins_str = ",".join(x)
    if len(ins_str)>0 and ins_str[-1] != ",":
        ins_str += ","
    sql = "UPDATE `admin` SET `SESSIONS`='%s' WHERE 1"%ins_str
    if runSQL.runUpdate(sql):
        return True
    return False
# >>HELP FUNCTIONS

def parseSessions(session):
    """
    admin login session is used to grant access control.<br>
    format: session1@timestamp,session2@timestamp,session3@timestamp,
    """
    SESSIONS = []
    al = session.split(",")
    for sd in al:
        SESSIONS.append(sd.split("@"))
    return SESSIONS

def getAdminSessions():
    """
    get session from database then parse it.
    return value: parsed session list and raw session list
    """
    sql = "SELECT `SESSIONS` FROM `admin` WHERE 1"
    result = runSQL.runSelect(sql)
    session_list = parseSessions(result[0][0].replace("\n","").replace("\r",""))
    return session_list,result
