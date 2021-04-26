from bottle import route, post, run, request, static_file, get, response, template, error
from datetime import datetime, timedelta
import os
import re
import backend
import time
import json
import psycopg2

def usernamemethod():
    cursor = conn.cursor()
    information1 = "SELECT  username FROM account "
    cursor.execute(information1)
    conn.commit()
    records = cursor.fetchall()
    for row in records:
        if request.get_cookie("isUser" + re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(row[0])))) is "1":
            link = "/profile/" + str(re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(row[0]))))
            info = {"username": row[0], 'link':link}
            return info
    info = {'username':'Guest', 'link':'/'}
    cursor.close()
    return info

def getUsername():
    cursor = conn.cursor()
    information1 = "SELECT  username FROM account "
    cursor.execute(information1)
    conn.commit()
    records = cursor.fetchall()
    for row in records:
        if request.get_cookie("isUser" + re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(row[0])))) is "1":
            cursor.close()
            return row[0]

def getEmlaLink():
    cursor = conn.cursor()
    information1 = "SELECT username, " + '"emlaLink"' +" FROM account "
    cursor.execute(information1)
    conn.commit()
    records = cursor.fetchall()
    for row in records:
        if row[0] == "domor8123":
            return {"emlaLink":row[1]}

@route('/')
def home():
    usernameInfo = usernamemethod()
    usernameInfo.update(backend.chastInfo())
    return template('static/index.tpl', usernameInfo)

@route('/about-me')
def aboutMe():
    return template('static/about-me.tpl', usernamemethod())

@route('/contact-me')
def contactMe():
    return template('static/Contact.tpl', usernamemethod())

@route('/Updates')
def Update():
    return template('static/Update.tpl', usernamemethod())

@route('/member-signup')
def membersignup():
    return template('static/signup.tpl', usernamemethod())

@post('/member-signup-Success')
def memberSignupSuccess():
    username = request.forms.get("Username")
    password = request.forms.get("Password")
    checkpassword = request.forms.get("checkPassword")
    email = request.forms.get("Email")
    checkemail = request.forms.get("checkEmail")
    if password != checkpassword or email != checkemail:
        return '''<meta http-equiv="refresh" content="0; URL='./member-signup'" />'''
    if backend.insertAccount(email, password, username):
        backend.generateSessionToken(username)
        response.set_cookie("isUser" + str(re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(username)))), "1", expires=time.mktime((datetime.now() + timedelta(hours=1)).timetuple()))
        return '''<meta http-equiv="refresh" content="0; URL='./'" />'''
    else:
        return '''<meta http-equiv="refresh" content="0; URL='./member-signup'" />'''

@route('/member-login')
def memberlogin():
    return template('static/login.tpl', usernamemethod())

@post('/member-login-Success')
def memberloginSuccess():
    username = request.forms.get("Username")
    password = request.forms.get("Password")
    if backend.checkifuser(username, password):
        backend.generateSessionToken(username)
        response.set_cookie("isUser" + re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(username))), "1", expires=time.mktime((datetime.now() + timedelta(hours=1)).timetuple()))
        return '''<meta http-equiv="refresh" content="0; URL='./'" />'''
    else:
        return '''<meta http-equiv="refresh" content="0; URL='./member-login'" />'''

@route('/chast')
def chast():
    usernameInfo = usernamemethod()
    usernameInfo.update(getEmlaLink())
    if request.get_cookie("isUser" + re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(getUsername())))) is "1":
        if getUsername() == "domor8123":
            return '''<meta http-equiv="refresh" content="0; URL='./'" />'''
        return template('static/chaste.tpl', usernameInfo)
    return '''<meta http-equiv="refresh" content="0; URL='./'" />'''

@route('/amazonWishlist')
def amazonWishlist():
    if request.get_cookie("isUser" + re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(getUsername())))) is "1":
        return '''<meta http-equiv="refresh" content="0; URL='https://www.amazon.com/hz/wishlist/dl/invite/4PsoXGI?ref_=wl_share'" />'''
    return '''<meta http-equiv="refresh" content="0; URL='https://www.amazon.com/hz/wishlist/ls/1A8RYFH8ZMSUC?ref_=wl_share'" />'''

@route('/Products')
def Product():
    return ''''''

@route('/profile/<username>')
def profile(username):
    if request.get_cookie("isUser" + re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(getUsername())))) is "1":
        if getUsername() == "domor8123":
            return '''<meta http-equiv="refresh" content="0; URL='https://data.heroku.com/dataclips/kvusqcufoggubettepdrsmohkhks'" />'''
        return template('static/change-user.tpl', usernamemethod())
    return '''<meta http-equiv="refresh" content="0; URL='./'" />'''

@post('/profile-updated')
def profileupdate():
    previoususername = request.forms.get("previousUsername")
    changeusername = request.forms.get("changeUsername")
    changepassword = request.forms.get("changePassword")
    changecheckpassword = request.forms.get("changecheckPassword")
    changeemail = request.forms.get("changeEmail")
    changecheckemail = request.forms.get("changecheckEmail")
    if changeemail != changecheckemail or changepassword != changecheckpassword:
        return '''<meta http-equiv="refresh" content="0; URL='./profile/''' + str(re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(previoususername)))) + ''''" />'''
    if changeemail != "":
        backend.changeEmail(changeEmail, previoususername)
        return '''<meta http-equiv="refresh" content="0; URL='./profile/''' + str(re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(previoususername)))) + ''''" />'''
    if changepassword != "":
        backend.changePassword(changepassword, previoususername)
        return '''<meta http-equiv="refresh" content="0; URL='./profile/''' + str(re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(previoususername)))) + ''''" />'''
    if changeusername != "":
        backend.changeUsername(changeusername, previoususername)
        backend.generateSessionToken(changeusername)
        response.set_cookie("isUser" + re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(changeusername))), "1", expires=time.mktime((datetime.now() + timedelta(hours=1)).timetuple()))
        return '''<meta http-equiv="refresh" content="0; URL='./profile/''' + str(re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(changeusername)))) + ''''" />'''
    else:
        return '''<meta http-equiv="refresh" content="0; URL='./'" />'''

@route('/delete/<username>')
def deleteUsername(username):
    if request.get_cookie("isUser" + re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(getUsername())))) is "1":
        if getUsername() == "domor8123":
            backend.deleteAccount(username)
            return '''<meta http-equiv="refresh" content="0; URL='https://data.heroku.com/dataclips/kvusqcufoggubettepdrsmohkhks'" />'''
        return '''<meta http-equiv="refresh" content="0; URL='./'" />'''
    return '''<meta http-equiv="refresh" content="0; URL='./'" />'''

@route('/emlalink/<emlalink>')
def chasteLink(emlalink):
    if request.get_cookie("isUser" + re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(getUsername())))) is "1":
        if getUsername() == "domor8123":
            backend.emlaLinkGenerate(emlalink)
    return '''<meta http-equiv="refresh" content="0; URL='./'" />'''
    
@route('/images/<filename>')
def server_Images(filename):
    if request.get_cookie("isUser" + re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(getUsername())))) is "1":
        return static_file(filename, root=os.path.abspath('images'))
    return '''<meta http-equiv="refresh" content="0; URL='./'" />'''

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=os.path.abspath('static'))

@error(404)
def error404(error):
    return '''<meta http-equiv="refresh" content="0; URL='./'" />'''

@error(500)
def error404(error):
    return '''<meta http-equiv="refresh" content="0; URL='./'" />'''

with open("information.json") as secretinformation:
    data = json.load(secretinformation)
conn = psycopg2.connect(user=data.get("databaseAddress")[0:data.get('databaseAddress').find("@")], password=data.get("databasePassword"), host=data.get("databaseAddress")[data.get("databaseAddress").find('@')+1:len(data.get("databaseAddress"))], database=data.get("database"))
run(host=data.get("webserver")[0:data.get("webserver").find(":")], port=os.environ.get('PORT', 5000), debug=True)
#run(host=data.get("webserver")[0:data.get("webserver").find(":")], port=data.get("webserver")[data.get("webserver").find(":")+1: len(data.get("webserver"))], debug=True)
