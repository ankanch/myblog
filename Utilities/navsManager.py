from Utilities import globeVar 

NAVS_LIST = []
comments = """# this file stores the navigations of the top bar. 
# format: nagavigation name,navigation type,navigation target
#0]       order : order to show
#1]       navigation name: name to diaplay on the top navigation bar
#2]       navigation url[unique]: url to visit this one
#3]       navigation type:  navigation type [file], file, external URL [exurl]
#4]       navigation target: extenerl URL or file

"""
TYPE_HTML_FILE = "file"
TYPE_EXTERNAL_URL = "exurl"

def addNav(navorder,navname,navtype,navurl,navtarget):
    navdata = [navorder,navname,navurl,navtype,navtarget]
    for nav in NAVS_LIST:
        if navurl == nav[2]:
            return False
    NAVS_LIST.append(navdata)
    navstr = ",".join(navdata)
    updateNavigationConfig()
    return True

def updateNav(navurl,navorder=None,navname=None,navtype=None,navtarget=None):
    CHANGED = False
    for i,nav in enumerate(NAVS_LIST):
        if nav[2] == navurl:
            if navorder:
                NAVS_LIST[i][0] = navorder
            if navname:
                NAVS_LIST[i][1] = navname
            if navtype:
                NAVS_LIST[i][3] = navtype
            if navtarget:
                NAVS_LIST[i][4] = navtarget
            CHANGED = True
            break
    if CHANGED:
        updateNavigationConfig()
        return True
    else:
        return False

def deleteNav(navurl):
    index = None
    for i,nav in enumerate(NAVS_LIST):
        if nav[2] == navurl:
            index = i
            break
    if index:
        NAVS_LIST.pop(index)
        updateNavigationConfig()
        return True
    return False


def updateNavigationConfig():
    linedata = [ ",".join(x) for x in NAVS_LIST ]
    with open(globeVar.RCFG.VAR_CONFIG_NAVS,"w",encoding='utf-8') as f:
        linedata = "\r\n".join(linedata)
        f.write(comments + linedata)

def loadNavigationConfig():
    with open(globeVar.RCFG.VAR_CONFIG_NAVS,encoding='utf-8') as f:
        dta = f.readlines()
        dta = [ x.replace("\n","") for x in dta if x[0] != "#" and len(x) > 3 ]
        global NAVS_LIST
        NAVS_LIST = [ x.replace("\r","").split(",") for x in dta ]

# helper function
def loadTarget(url):
    """
    returns: success,name,target
    """
    for nav in NAVS_LIST:
        print(nav[2],url)
        if nav[2] == url:
            if nav[3] == TYPE_HTML_FILE:
                return True,nav[1],nav[4]
    return False,None,None

