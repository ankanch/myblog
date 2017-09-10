import pymysql as SQL

#####################################################################
#                                                                   #
#                myblog revert database script                      #
#                           v 0.9                                   #
#                                                                   #
#         This script will help to you to reset the database,       #
#                  including delete all tables,users                #
#                                                                   #
#                    10 Sep. 2017 by Kanch                          #
#               https://github.com/ankanch/myblog                   #
#####################################################################


print("""
#####################################################################
#                                                                   #
#                       !!!!WARNING!!!!                             #
#                       !!!!WARNING!!!!                             #
#                                                                   #
#                myblog revert database script                      #
#                           v 0.9                                   #
#                                                                   #
#         This script will help to you to reset the database,       #
#                  including delete all tables,users                #
#                                                                   #
#                    10 Sep. 2017 by Kanch                          #
#               https://github.com/ankanch/myblog                   #
#                                                                   #
#                       !!!!WARNING!!!!                             #
#                       !!!!WARNING!!!!                             #
#                                                                   #
#####################################################################
        """)
print(">>>WARNING: You are running revert script, which will wiped all data \
            including delete databases,tables and myblog daba account. \
            Once this be done, you will lose all data.")
key = input("Please enter `YES` to continue:_____\b\b\b\b")
if key != "YES":
    print(">>>revert process stoped.\n>>> User Canceled.\n")
    exit()
root_pwd = input("Please enter your root password of your mysql database:________\b\b\b\b\b\b")
print(">>>REVERTING....")
cfgs = []
VAR_DB_HOST = ""
with open("../config/config.py","r") as f:
    cfgs = f.readlines()
    for line in cfgs:
        if line[0] != "#":
            if line.split("=")[0].replace(" ","") == "VAR_DB_HOST":
                VAR_DB_HOST = line.split("=")[1].replace(" ","").replace("\"","").replace("\n","")
DBCONN = None
try:
    DBCONN = SQL.connect(host=VAR_DB_HOST, port=3306,user="root",passwd=root_pwd,db="myblog",charset='UTF8',connect_timeout=20)
except Exception as e:
    print("\t>>ERROR:",e)
    print(">>>[ERROR] - setup exit.","Target DB @",VAR_DB_HOST)
    exit()
with DBCONN.cursor() as CUR:
    print(">>>deleteing database...")
    sql = "DROP DATABASE myblog;"
    CUR.execute(sql)
    DBCONN.commit()
    print(">>>deleteing user myblogx...")
    sql = "DROP USER 'myblogx'@'%'"
    CUR.execute(sql)
    DBCONN.commit()

print(">>>Data has been wiped!")
print(">>>Reverse Process Finiseed.")