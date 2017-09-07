import pymysql as SQL

#####################################################################
#
#
#
#
#
#
#
#####################################################################
VAR_DB_HOST = ""
VAR_DB_USER = ""
VAR_DB_PASSWORD = ""
VAR_DB_NAME = "myblog"

def runUpdate(sql):
    DBCONN = SQL.connect(host=VAR_DB_HOST, port=3306,user=VAR_DB_USER,passwd=VAR_DB_PASSWORD,db=VAR_DB_NAME,charset='UTF8')
    with DBCONN.cursor() as CUR:
        try:
            CUR.execute(sql)
            DBCONN.commit()
        except:
            DBCONN.close()
            return False
    DBCONN.close()
    return True


if __name__ == "__main__":
    print("setting up envirment for myblog")
    VAR_DB_HOST = input("Input your database host:")
    VAR_DB_USER = input("input your mysql database root username:")
    VAR_DB_PASSWORD = input("input your password:")
    print("checking database...")

    print("create database...")
    sql = "CREATE DATABASE myblog; USE myblog;"
    sql = """CREATE TABLE articles(
        AID  int(10) unsigned not null primary auto_increment,
        ATITLE  text not null,
        ACONTENT  mediumtext not null,
        ACATEGORY  text not null,
        AKEYWORDS  text not null,
        AURL  tinytext not null,
        AREADINGS  int(10) unsigned not null,
        DATE  tinytext not null,
        DRAFT  tinyint(1),
        TRASH tinyint(1)
    )"""
    sql = """CREATE TABLE categories(
        CID  int(11) not null primary auto_increment,
        CNAME  text not null,
        CACOUNT  int(10) unsigned not null,
        CURL tinytext not null
    )"""
    sql = """CREATE TABLE admin(
        ID int(11) not null primary ,
        USERNAME  tinytext not null,
        PASSWORD  text not null,
        LOCKED  tinyint(1) not null,
        SESSIONS text not null
    )"""


    print("insert default value...")
    sql = "INSERT INTO `categories`( `CNAME`, `CACOUNT`, `CURL`) VALUES ('%s',0,'%s')"%("未分类","uncategoried")
    if runSQL.runInsert(sql):
        print("insert finished.")
    else:
        print("failed to insert.")

    print("setting admin...")
    username = input(">>>Please input your username:")
    password = input(">>>Please input your password:")
    print("updating....")
    sql = ""

    print("myblog has been set up.\n Thank you for choosing myblog.")
