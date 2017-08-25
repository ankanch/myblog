import time
import flask
import os
import json
from config import config as CFG
from config import urlmap
from Utilities import globeVar
from Utilities import sessionManager,categoryManager,adminManager,othersManager,articlesManager
from Utilities import message as Message
from functools import wraps
from flask import Flask, jsonify, redirect, render_template, request,make_response,send_file,Response


app = Flask(__name__)

# init 
ConfigDict =  globeVar.VARS
print(ConfigDict)

@app.route('/')
def index():
    al = articlesManager.getArticlesList(5)
    cate = categoryManager.getAllCates()
    return render_template("index.html",TITLE=ConfigDict["SITE_TITLE"],NAVIGATION_BAR=urlmap.URLMAP_NAVIGATION,\
                            AC=al,CATE=cate)

@app.route('/<url>')
def xRoute(url):
    if url in urlmap.URLMAP_NAVIGATION.keys():
        return render_template(urlmap.URLMAP_NAVIGATION[url][1])
    else:
        pass

@app.route('/article/<url>')
def showArticle(url):
    al = articlesManager.getArticlesList(5)
    cate = categoryManager.getAllCates()
    code,data,content = articlesManager.getArticleByURL(url)
    if code:
        return render_template("article.html",TITLE=ConfigDict["SITE_TITLE"],\
                ATITLE=data[1],CATES=data[3],DATE=data[7],READINGS=data[6],CONTENT=content,\
                NAVIGATION_BAR=urlmap.URLMAP_NAVIGATION,AC=al,CATE=cate)
    return render_template("error_404.html")

# >>WRAPS of FLASK
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        session = request.cookies.get("session")
        if adminManager.checkSession(session) == False:
            return render_template("admin_login.html",ERROR=True)
        return f(*args, **kwargs)
    return decorated

# >>ADMIN RELATED

@app.route('/myblog/admin')
def admin():
    session = request.cookies.get("session")
    if adminManager.checkSession(session):
        return render_template("admin_center.html",BASIC_INFO=othersManager.getBasicInfo(),CATES=categoryManager.getAllCates())
    else:
        return render_template("admin_login.html",ERROR=True)

@app.route('/admin/newpost')
@requires_auth
def newpost():
    cates = categoryManager.getAllCates()
    return render_template("admin_new_article.html",CATES=cates)

@app.route('/editpost/<xid>')
@requires_auth
def editpost(xid):
    cates = categoryManager.getAllCates()
    code,data,content = articlesManager.getArticleByID(xid)
    return render_template("admin_new_article.html",CATES=cates,EDIT=True,EAID=data[0],\
                        ETITLE=data[1],ECONTENT=content,EKEYWORDS=data[4],EURL=data[5],CATE=data[3])

# >>GET INTERFACE
@app.route('/get/allcates')
def getallcates():
    data = categoryManager.getAllCates()
    return str(data)

@app.route('/get/articles/<where>/<page_start>')
def getArticles(where,page_start):
    """
    This function wil get one page of articles at one time.
    the parameter `where` specified the display page of articles, index page or admin center
    """
    if where == "index":
        pass
    elif where == "admin":
        data = articlesManager.getArticlesListD(page_start*15,15)
        return json.dumps(data)

# >>POST INTERFACE

@app.route('/search',methods=['POST','GET'])
def search():
    key = request.form['key']
    result = articlesManager.searchArticle(key)
    return render_template("search_result.html",NAVIGATION_BAR=urlmap.URLMAP_NAVIGATION,\
                            TITLE=ConfigDict["SITE_TITLE"],DATA=result)

@app.route('/adminlogin',methods=['POST','GET'])
def adminlogin():
    if request.method == 'POST':
        uname = request.form['username']
        upwd = request.form['password']
        code,data = adminManager.loginAdmin(uname,upwd)
        if code == 0:
            session = sessionManager.generateSessionID()
            adminManager.addSession(session)
            redirect_to_admin = redirect("/myblog/admin")
            response = app.make_response(redirect_to_admin )  
            response.set_cookie('session',value=session)
            return response
        else:
            return render_template("admin_login.html",ERROR=True,MSG=data)
    else:
        session = request.cookies.get("session")
        if adminManager.checkSession(session):
            return redirect("/myblog/admin")
        return render_template("admin_login.html")

@app.route('/addCate',methods=['POST'])
@requires_auth
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
@requires_auth
def deleteCate():
    cate_id = request.form['id']
    if categoryManager.deleteCate(cate_id):
        return globeVar.SUCCESS
    return globeVar.UNSUCCESS

@app.route('/updateCate',methods=['POST'])
@requires_auth
def updateCate():
    cate_id = request.form['id']
    cate_name = request.form['new_cate_name']
    cate_url = request.form['new_cate_url']
    if categoryManager.changeCate(cate_id,cate_name,cate_url):
        return globeVar.SUCCESS
    return globeVar.UNSUCCESS

@app.route('/publish',methods=['POST'])
@requires_auth
def publishArticle():
    title = request.form['article_title']
    cate = request.form['article_cate']
    content = request.form['article_content']
    keywords = request.form['article_keywords']
    url = request.form['article_url']
    code,why = articlesManager.addNewArticle(title,cate,content,keywords,url)
    if code:
        return globeVar.SUCCESS
    return globeVar.UNSUCCESS

@app.route('/quickeditarticle',methods=['POST'])
@requires_auth
def quickEditArticle():
    title = request.form['edit_article_title']
    cate = request.form['article_cate']
    url = request.form['url']
    xid = request.form['id']
    if articlesManager.quickEditArticle(xid,title,cate,url):
        return globeVar.SUCCESS
    return globeVar.UNSUCCESS

@app.route('/update_article',methods=['POST'])
@requires_auth
def updateArticle():
    xid = request.form['id']
    title = request.form['article_title']
    cate = request.form['article_cate']
    content = request.form['article_content']
    keywords = request.form['article_keywords']
    url = request.form['article_url']
    code,why = articlesManager.updateArticle(xid,title,cate,content,keywords,url)
    if code:
        return globeVar.SUCCESS
    return globeVar.UNSUCCESS

@app.route('/move_article_to_trash',methods=['POST'])
@requires_auth
def moveToTrash():
    xid = request.form['id']
    if articlesManager.deleteArticle(xid):
        return globeVar.SUCCESS
    return globeVar.UNSUCCESS

@app.route('/test')
def test_anything():
    #return str(categoryManager.getAllCates())
    return render_template("article.html",NAVIGATION_BAR=urlmap.URLMAP_NAVIGATION,TITLE=ConfigDict["SITE_TITLE"])

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