from bottle import route, post, run, request, static_file, get, response
from datetime import datetime, timedelta
import os
import re
import frontend
import backend
import time
import json
import psycopg2

@route('/')
def home():
    cursor = conn.cursor()
    information1 = "SELECT  username FROM account "
    cursor.execute(information1)
    conn.commit()
    records = cursor.fetchall()
    for row in records:
        #---- Grabs encrypted cookie with hidden username string and checks if user logged in ----
        if request.get_cookie("isUser" + re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(row[0])))) is "1":
            return frontend.home(backend.countdownTime(), row[0])
    #---- Shows home screen with a default username of Guest ----
    return frontend.home(backend.countdownTime(), username="Guest")

@route('/about-me')
def aboutMe():
    return static_file('index.html', root=os.path.abspath('static'))

@route('/contact-me')
def contactMe():
    return static_file('Contact.html', root=os.path.abspath('static'))

@route('/Updates')
def Update():
    return static_file('Update.html', root=os.path.abspath('static'))

@route('/member-signup')
def membersignup():
    #---- Shows a page that allows users to sign up ----
    return static_file('signup.html', root=os.path.abspath('static'))

@post('/member-signup-Success')
def memberSignupSuccess():
    #---- grabs all user information ----
    username = request.forms.get("Username")
    password = request.forms.get("Password")
    checkpassword = request.forms.get("checkPassword")
    email = request.forms.get("Email")
    checkemail = request.forms.get("checkEmail")
    #---- Checks if password or emails are different ----
    if password != checkpassword or email != checkemail:
        return static_file('signup.html', root=os.path.abspath('static'))
    #---- Inserts the account into the database ----
    if backend.insertAccount(email, password, username):
        #---- Generates a random session ----
        backend.generateSessionToken(username)
        #---- Takes encrypted session token with username and makes cookie that expires in 1 hour ----
        response.set_cookie("isUser" + str(re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(username)))), "1", expires=time.mktime((datetime.now() + timedelta(hours=1)).timetuple()))
        return '''<meta http-equiv="refresh" content="0; URL='./'" />'''
    else:
        return static_file('signup.html', root=os.path.abspath('static'))

@route('/member-login')
def memberlogin():
    return static_file('login.html', root=os.path.abspath('static'))

@post('/member-login-Success')
def memberloginSuccess():
    #---- Grabs user data ----
    username = request.forms.get("Username")
    password = request.forms.get("Password")
    #---- Checks is user is on database ----
    if backend.checkifuser(username, password):
        #---- Generates a random session token ----
        backend.generateSessionToken(username)
        #---- Creates a cookies with session token and expires in 1 hour ----
        response.set_cookie("isUser" + re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(username))), "1", expires=time.mktime((datetime.now() + timedelta(hours=1)).timetuple()))
        #---- Redirects with a refresh time of 0 back to home page ----
        return '''<meta http-equiv="refresh" content="0; URL='./'" />'''
    else:
        return static_file('login.html', root=os.path.abspath('static'))

@route('/chast')
def chast():
    cursor = conn.cursor()
    information1 = "SELECT  username FROM account "
    cursor.execute(information1)
    conn.commit()
    records = cursor.fetchall()
    for row in records:
        #---- Checks if user is a valid user in database ----
        if request.get_cookie("isUser" + re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(row[0])))) is "1":
            #---- Checks if user is domor8123 as it is not allowed to update timer ----
            if row[0] == "domor8123":
                return '''<meta http-equiv="refresh" content="0; URL='./'" />'''
            return static_file('chaste.html', root=os.path.abspath('static'))
    return '''<meta http-equiv="refresh" content="0; URL='./'" />'''

@post('/chastupdate')
def chastUpdate():
    time = request.forms.get("time")
    cursor = conn.cursor()
    information1 = "SELECT  username FROM account "
    cursor.execute(information1)
    conn.commit()
    records = cursor.fetchall()
    for row in records:
        #---- Not really needed, but checks if user is valid is allowed to updates chastity time ----
        if request.get_cookie("isUser" + re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(row[0])))) is "1":
            backend.chastetime(row[0], time)
    return '''<meta http-equiv="refresh" content="0; URL='./'" />'''

@route('/amazonWishlist')
def amazonWishlist():
    cursor = conn.cursor()
    information1 = "SELECT  username FROM account "
    cursor.execute(information1)
    conn.commit()
    records = cursor.fetchall()
    for row in records:
        if request.get_cookie("isUser" + re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(row[0])))) is "1":
            #---- If user is valid redirects to editable amazon wishlist ----
            return '''<meta http-equiv="refresh" content="0; URL='https://www.amazon.com/hz/wishlist/dl/invite/4PsoXGI?ref_=wl_share'" />'''
    #---- If user isn't valid redirect to viewable amazon wishlist ----
    return '''<meta http-equiv="refresh" content="0; URL='https://www.amazon.com/hz/wishlist/ls/1A8RYFH8ZMSUC?ref_=wl_share'" />'''

@route('/profile/<username>')
def profile(username):
    cursor = conn.cursor()
    information1 = "SELECT  username FROM account "
    cursor.execute(information1)
    conn.commit()
    records = cursor.fetchall()
    for row in records:
        #---- Editable profile with custom encrypted username directory ----
        if request.get_cookie("isUser" + re.sub('[^A-Za-z0-9]+','',str(backend.encryptedtext(row[0])))) is "1":
            return frontend.profile(row[0])

@post('/profile-updated')
def profileupdate():
    #---- Grabs all user information ----
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

@route('/static/<filename>')
def server_static(filename):
    #---- Static files ----
    return static_file(filename, root=os.path.abspath('static'))

with open("information.json") as secretinformation:
    data = json.load(secretinformation)
#---- Connects to pgsql server ----
conn = psycopg2.connect(user=data.get("databaseAddress")[0:data.get('databaseAddress').find("@")], password=data.get("databasePassword"), host=data.get("databaseAddress")[data.get("databaseAddress").find('@')+1:len(data.get("databaseAddress"))], database=data.get("database"))
#---- Runs bootle webserver of python web app to work ----
run(host=data.get("webserver")[0:data.get("webserver").find(":")], port=os.environ.get('PORT', 5000), debug=True)
