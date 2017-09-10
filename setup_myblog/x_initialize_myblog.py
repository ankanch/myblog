import pymysql as SQL
from time import gmtime, strftime,time

#####################################################################
#                                                                   #
#                   myblog ezsetup script                           #
#                           v 0.9                                   #
#                                                                   #
#         This script will help to you to setup related             #
#        envirment that myblog needs,like database, admin.          #
#                                                                   #
#                    9 Sep. 2017 by Kanch                           #
#               https://github.com/ankanch/myblog                   #
#####################################################################
VAR_DB_HOST = ""
VAR_DB_PASSWORD = ""
VAR_DB_NAME = "myblog"

COPYRIGHT = ""
with open("copyright") as f:
    COPYRIGHT = f.read()

def runUpdateN(sql):
    DBCONN = SQL.connect(host=VAR_DB_HOST, port=3306,user="root",passwd=VAR_DB_PASSWORD,db="mysql",charset='UTF8')
    with DBCONN.cursor() as CUR:
        try:
            CUR.execute(sql)
            DBCONN.commit()
        except Exception as e:
            DBCONN.close()
            print("\t>>ERROR:",e)
            return False
    DBCONN.close()
    return True


def runUpdate(sql):
    DBCONN = SQL.connect(host=VAR_DB_HOST, port=3306,user="root",passwd=VAR_DB_PASSWORD,db=VAR_DB_NAME,charset='UTF8')
    with DBCONN.cursor() as CUR:
        try:
            CUR.execute(sql)
            DBCONN.commit()
        except Exception as e:
            DBCONN.close()
            print("\t>>ERROR:",e)
            return False
    DBCONN.close()
    return True

def replaceSpecialCharters(raw):
    charset = {
    "\"":"xASC_DQ",
    "'":"xASC_SQ",
    "`":"xASC_CQ",
    "&":"xASC_AND",
    ")":"xASC_RS",
    "(":"xASC_LS",
    "[":"xASC_RR",
    "]":"xASC_LR",
    }
    for ch in charset:
        raw = raw.replace(ch,charset[ch])
    return raw

if __name__ == "__main__":
    sql = ""
    #mysql_upgrade
    # Welcome
    print(COPYRIGHT)
    print(">>>myblog ezsetup is running")
    y = input("\t>>Input 'Y' to start setup myblog:____\b\b\b")
    if y.lower() != "y":
        print(">>>User Cancelled Stup.\n")
        exit()
    
    # start setup
    print(">>>[1]setting up database:")
    VAR_DB_HOST = input("\t>>Input your database host:")
    VAR_DB_PASSWORD = input("\t>>input your password:")

    print("\t>>checking database...")
    DD = None
    try:
        DD = SQL.connect(host=VAR_DB_HOST, port=3306,user="root",passwd=VAR_DB_PASSWORD,db="mysql",charset='UTF8',connect_timeout=20)
        # check sql version
        ver = []
        with DD.cursor() as d:
            sql = "SELECT VERSION();"
            d.execute(sql)
            DD.commit()
            re = d.fetchall()[0][0]
            print(re)
            ver = re.split(".")
        if not (ver[0] >= '5' and ver[1] >= '5' and ver[3] >= '3'):
            print(">>>ERROR: You have mysql version",".".join(ver),",but the minimal version myblog support is 5.5.3!Please upgrade your mysql!")
            DD.close()
            exit()
    except Exception as e:
        print("\t>>ERROR:",e)
        print(">>>[ERROR] - setup exit.")
        exit()
    DD.close()

    print("\t>>create database `myblog`...")
    # create database here
    with open("./sqlscripts/createDB_User.sql") as f:
        sql = f.read()
        sql  = sql.replace("\n","")
    myblog_pass = input("\t>>please set a password for user `myblogx`:")
    sql = sql.replace("@PASSWORD@",myblog_pass)
    print("\t>>processing....")
    if runUpdateN(sql) == False:
        print(">>>ERROR: ezsetup exit!\n>>>Please create database user for myblog with user name `myblogx` manully!")
        print(">>>For more information,plaese visit: https://github.com/ankanch/myblog")
        exit()

    print("\t>>writing config...")
    configs = ""
    with open("../config/config.py","r") as f:
        configs = f.read()
    configs = configs.replace("@HOST@",VAR_DB_HOST)
    configs = configs.replace("@PASSWORD@",myblog_pass)
    with open("../config/config.py","w") as f:
        f.write(configs)

    print("\t>>creating table admin....")
    with open("./sqlscripts/createTBadmin.sql") as f:
        sql = f.read()
        sql  = sql.replace("\n","")
    runUpdate(sql)

    print("\t>>creating table categories....")
    with open("./sqlscripts/createTBCategories.sql") as f:
        sql = f.read()
        sql  = sql.replace("\n","")
    runUpdate(sql)

    print("\t>>creating table articles....")
    with open("./sqlscripts/createTBArticles.sql") as f:
        sql = f.read()
        sql  = sql.replace("\n","")
    runUpdate(sql)

    # data base created ,now start insering some defualt values
    # insert default uncategorized name
    print(">>>[2]insert default value...")
    sql = "INSERT INTO `categories`( `CNAME`, `CACOUNT`, `CURL`) VALUES ('%s',0,'%s')"%("uncategoried","uncategoried")
    runUpdate(sql)

    # insert an default articles.
    timestr = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    ac = ""
    with open("./defaultArticle/intro.article",encoding='utf-8' ,errors='ignore') as f:
        ac = f.read()
    with open("./sqlscripts/insertArticle.sql",encoding='utf-8',errors='ignore') as f:
        sql = f.read()
    sql = sql.replace("@content",replaceSpecialCharters(ac))
    sql = sql .replace("@timestr",timestr)
    runUpdate(sql)

    # insert myblog admin
    print(">>>[3]setting admin...")
    username = input("\t>>Please input your username:")
    password = input("\t>>Please input your password:")
    print("\t>>updating....")
    with open("./sqlscripts/insertAdmin.sql") as f:
        sql = f.read()
        sql  = sql.replace("\n","")
    sql = sql.replace("@USERNAME@",username)
    sql = sql.replace("@PASSWORD@",password)
    runUpdate(sql)
    print(">>>myblog has been set up.\n>>>Thank you for choosing myblog.")
