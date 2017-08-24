from Utilities import runSQL
from Utilities import globeVar

#####################################################################
#
#
#
#
#
#
#
#####################################################################

print("setting up envirment for myblog")
print("checking database...")
print("create database...")
print("insert default value...")
sql = "INSERT INTO `categories`( `CNAME`, `CACOUNT`, `CURL`) VALUES ('%s',0,'%s')"%("未分类","uncategoried")
if runSQL.runInsert(sql):
    print("insert finished.")
else:
    print("failed to insert.")


