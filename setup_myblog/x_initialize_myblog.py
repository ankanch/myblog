import pymysql as SQL

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


if __name__ == "__main__":
    sql = ""
    
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
    print(VAR_DB_HOST)
    print("\t>>checking database...")
    DD = None
    try:
        DD = SQL.connect(host=VAR_DB_HOST, port=3306,user="root",passwd=VAR_DB_PASSWORD,db="mysql",charset='UTF8',connect_timeout=20)
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
    runUpdateN(sql)
    myblog_pass = input("\t>>please set a password for user `myblog`:")
    sql = sql.replace("@PASSWORD@",myblog_pass)
    print("\t>>processing....")
    print("\t>>creating table admin....")
    with open("./sqlscripts/createTBadmin.sql") as f:
        sql = f.read()
        sql  = sql.replace("\n","")
    runUpdate(sql)
    print("\t>>inserting user `myblog` with password",myblog_pass)
    #run sql to create myblog user and password here
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
