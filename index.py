import time
import flask
import os
from config import config as CFG
from config import urlmap
from Utilities import globeVar,sessionManager,categoryManager
from Utilities import message as Message
from flask import Flask, jsonify, redirect, render_template, request,make_response,send_file,Response


app = Flask(__name__)

# init 
ConfigDict =  globeVar.loadConfig()
print(ConfigDict)

@app.route('/')
def index():
    return render_template("index.html",TITLE=ConfigDict["SITE_TITLE"],NAVIGATION_BAR=urlmap.URLMAP_NAVIGATION)

@app.route('/<url>')
def xRoute(url):
    if url in urlmap.URLMAP_NAVIGATION.keys():
        return render_template(urlmap.URLMAP_NAVIGATION[url][1])
    else:
        pass

@app.route('/myblog/admin')
def admin():
    session = request.cookies.get("session")
    if session in globeVar.VARS["SESSIONS"]:
        return render_template("admin_center.html")
    else:
        return render_template("admin_login.html",ERROR=True)

# >>GET INTERFACE
@app.route('/get/allcates')
def getallcates():
    data = categoryManager.getAllCates()
    return str(data)

# >>POST INTERFACE

@app.route('/adminlogin',methods=['POST'])
def adminlogin():
    uname = request.form['username']
    upwd = request.form['password']
    if uname == globeVar.VARS["username"] and upwd == globeVar.VARS["password"]:
        session = sessionManager.generateSessionID()
        globeVar.VARS["SESSIONS"].append(session)
        redirect_to_admin = redirect("/myblog/admin")
        response = app.make_response(redirect_to_admin )  
        response.set_cookie('session',value=session)
        return response
    else:
        return redirect("/myblog/admin")

@app.route('/addCate',methods=['POST'])
def addCate():
    cate_name = request.form['catename']
    cate_url = request.form['cateurl']
    if categoryManager.checkExistence(cate_name,cate_url):
        if categoryManager.addNewCate(cate_name,cate_url):
            return globeVar.SUCCESS
        return globeVar.UNSUCCESS
    else:
        return globeVar.UNSUCCESS

@app.route('/deleteCate',methods=['POST'])
def deleteCate():
    cate_id = request.form['id']
    if categoryManager.deleteCate(cate_id):
        return globeVar.SUCCESS
    return globeVar.UNSUCCESS

@app.route('/updateCate',methods=['POST'])
def updateCate():
    cate_id = request.form['id']
    cate_name = request.form['new_cate_name']
    cate_url = request.form['new_cate_url']
    if categoryManager.changeCate(cate_id,cate_name,cate_url):
        return globeVar.SUCCESS
    return globeVar.UNSUCCESS

if __name__ == '__main__':
    if "mode.server" in os.listdir("./"):
        # when a specific file in current dir,bind IP below  
        # running on beta.baderlab.org
        print(">>>Running as server mode,use http://beta.baderlab.org to visit.")
        app.run(host='192.168.81.218',port=80)
    else:
        # local machine for test
        print(">>>Running on local machine.")
        app.run(host='127.0.0.1',port=80,debug=True)