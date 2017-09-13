import pymysql as SQL
from os import system
from shutil import copy2
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
NEED = "systemd, NGINX"
STR_NGINX = """server {
    listen 80;
    server_name @server_domain_or_IP;

    location / {
        include proxy_params;
        proxy_pass http://@server_internalIP:8000;
    }
}"""

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
            ver = [ int(x[0]) for x in re.split(".")]
        if int(ver[0]) <=5:
            if int(ver[1]) <=5:
                if int(ver[2][0]) < 3 and len(ver[3]) == 1:
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
    print(">>>myblog has been set up.\n>>>[4]We are setting up some essential python libaries.")
    system("pip3 install flask pymysql gunicorn")


    print(">>>[5] let's set the host Ip where you will run myblog.")
    host_ip = input("\t>>please enter your host IP:")
    internal_ip = input("\t>>please enter your internal IP:")
    with open("../config/config.py","r",encoding='utf-8') as f:
        configs = f.read()
    configs = configs.replace("@SITE_HOST@",internal_ip)
    with open("../config/config.py","w",encoding='utf-8') as f:
        f.write(configs)
    with open("./configs/nginx/myblog","w") as f:
        STR_NGINX = STR_NGINX.replace("@server_domain_or_IP",host_ip).replace("@server_internalIP",internal_ip)
        f.write(STR_NGINX)

    print(">>>[6]copy files...")
    copy2("./configs/upstart/myblog.conf","/etc/init/")
    copy2("./configs/systemd/myblog.service","/etc/systemd/system/")
    copy2("./configs/nginx/myblog","/etc/nginx/sites-available/")
    copy2("./configs/mode.server","../mode.server")
    print("\t>>linking..")
    system("sudo systemctl start myblog")
    system("sudo systemctl enable myblog")
    system("sudo ln -s /etc/nginx/sites-available/myblog /etc/nginx/sites-enabled")
    print("\t>>restarting nginx...")
    system("sudo service nginx restart")

    print(""">>>All done! To run myblog, simplily return upper dir and run `python3 app.py`, then let it stays background.""")
    print(">>>Thank you for choosing myblog.")
