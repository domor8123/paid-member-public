from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from mimetypes import MimeTypes
from apiclient import errors
from httplib2 import Http
from email.mime.text import MIMEText
import random, base64, string, json, os, pickle, io, shutil
import psycopg2

password = {}
#----
with open("information.json") as secretinformation:
    data = json.load(secretinformation)
#---- Creates pgsql connection with the hidden credentials in information.json ----
conn = psycopg2.connect(user=data.get("databaseAddress")[0:data.get('databaseAddress').find("@")], password=data.get("databasePassword"), host=data.get("databaseAddress")[data.get("databaseAddress").find('@')+1:len(data.get("databaseAddress"))], database=data.get("database"))

def generateSessionToken(username):
    #---- Random generates a string ----
    sessionToken = ''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase + string.punctuation) for _ in range(120))
    return encryption(sessionToken,username)

def generateRandomPasscode(password, username):
    #---- Random generates a string with password ----
    Passcode = ''.join(random.choice(password + string.ascii_lowercase + string.digits + string.ascii_uppercase + string.punctuation) for _ in range(120))
    return encryption(Passcode,"mysql" + username)

def generateRandomEmail(email, username):
    #---- Random generates a string with password
    Passcode = ''.join(random.choice(email + string.ascii_lowercase + string.digits + string.ascii_uppercase + string.punctuation) for _ in range(120))
    return encryption(Passcode,"mysql" + username)

def checkifuser(username, password):
    #---- Genreates a unique password for username to grab current password ----
    generateRandomPasscode(password, username)
    cursor = conn.cursor()
    information1 = "SELECT  username FROM account "
    cursor.execute(information1)
    conn.commit()
    records = cursor.fetchall()
    for row in records:
        #---- Check if username and password are correct to what is stored in database ----
        if row[0] == username and password == decryption(username):
            return True
    return False

def insertAccount(Email, password, username):
    cursor = conn.cursor()
    information1 = "SELECT  username, email FROM account "
    cursor.execute(information1)
    conn.commit()
    records = cursor.fetchall()
    x = cursor.rowcount
    for row in records:
        #---- Compares is username and email have already been used ----
        if row[0] == username and row[1] == Email:
            return False
    results = ("INSERT INTO account"
                "(user_id, username, password, email, lockset)"
                "VALUES (%s, %s, %s, %s, %s)")
    #---- Inserts user_id and generateRandomPasscode, Email, and datetime.now() ----
    results_data = (x, username, generateRandomPasscode(password, username), generateRandomEmail(Email, username), str(datetime.now()))
    cursor.execute(results, results_data)
    conn.commit()
    return True

def chastetime(username, time):
    #---- Splits time in 1 and hours ----
    time = time.split("h")
    cursor = conn.cursor()
    information = "SELECT username, lockset FROM account"
    cursor.execute(information)
    conn.commit()
    records = cursor.fetchall()
    number = False
    for row in records:
        if row[0] != "domor8123":
            #---- Will compare if user last signup or changed time is greater than 24 hours ----
            if datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S.%f") >= datetime.now()-timedelta(hours=24) and row[0] == username:
                #---- Updates user with current datetime and resets the 24 hour counter ----
                results1 = "UPDATE account set lockset = %s WHERE username = %s"
                results_data = (datetime.now(), username)
                cursor.execute(results1, results_data)
                conn.commit()
                number = True
        if number:
            if row[0] == "domor8123":
                #---- Changes string to days, hours, minutes, seconds strings ----
                timeString = row[1]
                if timeString.find('day')!= -1:
                    day = timeString.index("day")
                    hours = timeString.index(",")
                    minutes = timeString.index(":", day)
                    seconds = timeString.index(":", minutes+1)
                    dayString = timeString[0:day]
                    hoursString = timeString[hours+2:minutes]
                    minutesString = timeString[minutes+1:seconds]
                    secondsString = timeString[seconds+1:len(row[1])]
                    totaltime = timedelta(seconds=(int(secondsString) + (int(minutesString)*60) + (int(hoursString)*3600) + (int(dayString)*86400)))
                else:
                    hours = timeString.index(":")
                    minutes = timeString.index(":", hours)
                    seconds = timeString.index(":", minutes+1)
                    hoursString = timeString[0:hours]
                    minutesString = timeString[minutes+1:seconds]
                    secondsString = timeString[seconds+1:len(row[1])]
                    totaltime = timedelta(seconds=(int(secondsString) + (int(minutesString)*60) + (int(hoursString)*3600)))
                results1 = "UPDATE account set lockset = %s WHERE username = %s"
                #---- Changes user domor8123 locketset value to add the current time and the change of time for x hours ----
                results_data1 = (str(totaltime +timedelta(hours=int(time[0]))), "domor8123")
                cursor.execute(results1, results_data1)
                conn.commit()

def countdownTime():
    cursor = conn.cursor()
    information = "SELECT username, lockset FROM account"
    cursor.execute(information)
    conn.commit()
    records = cursor.fetchall()
    for row in records:
        if row[0] == "domor8123":
            timeString = row[1]
            print("timestring", timeString)
            if timeString.find('day')!= -1:
                day = timeString.index("day")
                hours = timeString.index(",")
                minutes = timeString.index(":", day)
                seconds = timeString.index(":", minutes+1)
                dayString = timeString[0:day]
                hoursString = timeString[hours+2:minutes]
                minutesString = timeString[minutes+1:seconds]
                secondsString = timeString[seconds+1:len(row[1])]
                #---- Displays countdown timer that is readable via html ----
                return ("%d D: %d H : %d M: %d S" % (int(dayString), int(hoursString), int(minutesString), int(secondsString)))
            else:
                hours = timeString.index(":")
                minutes = timeString.index(":", hours)
                seconds = timeString.index(":", minutes+1)
                hoursString = timeString[0:hours]
                minutesString = timeString[minutes+1:seconds]
                secondsString = timeString[seconds+1:len(row[1])]
                #---- DIsplays countdown timer that is redable via html ----
                return ("%d H : %d M: %d S" % (int(hoursString), int(minutesString), int(secondsString)))
    return ("%d D: %d H : %d M: %d S" % (0, 0, 0, 0))

def changeEmail(changeEmail, username):
    #---- User changable username ----
    cursor = conn.cursor()
    results1 = "UPDATE account set email = %s WHERE username = %s"
    #---- Generates new showable email on database ----
    results_data1 = (generateRandomEmail(changeEmail, username), username)
    cursor.execute(results1, results_data1)
    conn.commit()

def changeUsername(changeUsername, username):
    #---- Changeable username ----
    cursor = conn.cursor()
    information1 = "SELECT username FROM account "
    cursor.execute(information1)
    conn.commit()
    records = cursor.fetchall()
    for row in records:
        if row[0] == changeUsername:
            #---- Checks if new username is already used/created ----
            return False
        if row[0] == username:
            #---- Changes username to selected username ----
            results1 = "UPDATE account set username = %s WHERE username = %s"
            results_data1 = (changeUsername, username)
            cursor.execute(results1, results_data1)
            conn.commit()

def changePassword(changePassword, username):
    #---- User changable password ----
    cursor = conn.cursor()
    results1 = "UPDATE account set password = %s WHERE username = %s"
    #---- Generates new showable password on database ----
    results_data1 = (generateRandomPasscode(changePassword, username), username)
    cursor.execute(results1, results_data1)
    conn.commit()