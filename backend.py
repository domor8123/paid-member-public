from datetime import datetime, timedelta
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from paypalhttp import HttpError
from apiclient import errors
from httplib2 import Http
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random, base64, string, json, os, pickle, io, shutil, ssl, smtplib, re
import psycopg2
import urllib
import urllib.request
import requests

password = {}
with open("information.json") as secretinformation:
    data = json.load(secretinformation)
conn = psycopg2.connect(user=data.get("databaseAddress")[0:data.get('databaseAddress').find("@")], password=data.get("databasePassword"), host=data.get("databaseAddress")[data.get("databaseAddress").find('@')+1:len(data.get("databaseAddress"))], database=data.get("database"))

def generateSessionToken(username):
    sessionToken = ''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase + string.punctuation) for _ in range(120))
    return encryption(sessionToken,username)

def generateRandomPasscode(passwords, username):
    Passcode = ''.join(random.choice(passwords + string.ascii_lowercase + string.digits + string.ascii_uppercase + string.punctuation) for _ in range(120))
    return encryption(Passcode,"mysql" + username)

def generateRandomEmail(email, username):
    Passcode = ''.join(random.choice(email + string.ascii_lowercase + string.digits + string.ascii_uppercase + string.punctuation) for _ in range(120))
    return encryption(Passcode,"mysql" + username)

def encryptedtext(value):
    #---- Returns encrypted Token ----
    try:
        return password.get(value)[0]
    except TypeError:
        return "doesn't exist"

def checkifuser(username, password):
    cursor = conn.cursor()
    information1 = "SELECT  username FROM account "
    cursor.execute(information1)
    conn.commit()
    records = cursor.fetchall()
    for row in records:
        if row[0] == username and password == decryption("password" + username, username):
            cursor.close()
            return True
    cursor.close()
    return False

def insertAccount(Email, password, username):
    cursor = conn.cursor()
    information1 = "SELECT  username, email FROM account "
    cursor.execute(information1)
    conn.commit()
    records = cursor.fetchall()
    x = cursor.rowcount
    for row in records:
        if row[0] == username and row[1] == Email:
            return False
    results = ("INSERT INTO account"
                "(user_id, username, password, email)"
                "VALUES (%s, %s, %s, %s)")
    sendEmail(username)
    results_data = (x, username, generateRandomPasscode(password, username), generateRandomEmail(Email, username))
    cursor.execute(results, results_data)
    conn.commit()
    cursor.close()
    return True

def sendEmail(username):
    server = smtplib.SMTP("smtp.gmail.com", 587 )  ## This will start our email server
    server.starttls(context=ssl.create_default_context())         ## Starting the server
    server.login(data.get("email"), data.get("EmailPassword"))
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = data.get("email")
    mimeMessage['subject'] = "account created from membership website"
    mimeMessage.attach(MIMEText(username + " has made an account.", 'plain'))
    server.sendmail(data.get("email"), data.get("email"), mimeMessage.as_string())
    server.quit()
    
def deleteAccount(username):
    cursor = conn.cursor()
    information1 = "SELECT username FROM account "
    cursor.execute(information1)
    conn.commit()
    records = cursor.fetchall()
    for row in records:
        if row[0] == "domor8123":
            cursor = conn.cursor()
            results1 = "DELETE FROM account WHERE username = '" + username + "'"
            cursor.execute(results1)
            conn.commit()
            cursor.close()

def emlaLinkGenerate(emlaLink):
    cursor = conn.cursor()
    information1 = "SELECT username, `emlaLink` FROM account "
    cursor.execute(information1)
    conn.commit()
    records = cursor.fetchall()
    for row in records:
        if row[0] == "domor8123":
            cursor = conn.cursor()
            results1 = "UPDATE account set `emlaLink` = %s WHERE username = %s"
            results_data1 = ("https://www.emlalock.com/#/f/" + emlaLink, row[0])
            cursor.execute(results1, results_data1)
            conn.commit()
            cursor.close()
            
def chastInfo():
    url = urllib.request.urlopen("https://api.emlalock.com/plugin?userid=" + data.get("EmlaUserId"))
    content = url.read()
    emlalock = content.decode('utf-8')
    emlalock = emlalock.replace("#444", '#ff527c')
    return {'countdowntimer':emlalock}

def changeEmail(changeEmail, username):
    cursor = conn.cursor()
    results1 = "UPDATE account set email = %s WHERE username = %s"
    results_data1 = (generateRandomEmail(changeEmail, username), username)
    cursor.execute(results1, results_data1)
    conn.commit()

def changeUsername(changeUsername, username):
    cursor = conn.cursor()
    information1 = "SELECT username FROM account "
    cursor.execute(information1)
    conn.commit()
    records = cursor.fetchall()
    for row in records:
        if row[0] == changeUsername:
            return False
        if row[0] == username:
            results1 = "UPDATE account set username = %s WHERE username = %s"
            results_data1 = (changeUsername, username)
            cursor.execute(results1, results_data1)
            conn.commit()
            cursor.close()

def changePassword(changePassword, username):
    cursor = conn.cursor()
    results1 = "UPDATE account set password = %s WHERE username = %s"
    results_data1 = (generateRandomPasscode(changePassword, username), username)
    cursor.execute(results1, results_data1)
    conn.commit()
    cursor.close()