from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import time
import psycopg2
import os

def countdownTime():
    #---- Creates connection to pgsql databse ----
    cursor = conn.cursor()
    #---- Selects two columns from the table account ----
    information = "SELECT username, lockset FROM account"
    cursor.execute(information)
    #---- Saves and runs the commond on pgsql ----
    conn.commit()
    #---- Fetches all rows and the columns of username and lockset from table account ----
    records = cursor.fetchall()
    for row in records:
        #---- Checks if username column is eqal to domor8123 ----
        if row[0] == "domor8123":
            timeString = row[1]
            #---- Searches if day string is located in the timestring ----
            if row[1].find('day')!= -1:
                #---- Converts lockset string in database to convertable strings ----
                day = row[1].index("day")
                hours = row[1].index(",")
                minutes = row[1].index(":", day)
                seconds = row[1].index(":", minutes+1)
                dayString = timeString[0:day]
                hoursString = timeString[hours+2:minutes]
                minutesString = timeString[minutes+1:seconds]
                secondsString = timeString[seconds+1:len(row[1])]
                #---- Transforms all days, hours, minutes, seconds to the change of time in seconds ----
                totaltime = timedelta(seconds=(int(secondsString) + (int(minutesString)*60) + (int(hoursString)*3600) + (int(dayString)*86400)))
            else:
                #---- Converts lockset string in database to convertable strings ----
                hours = row[1].index(":")
                minutes = row[1].index(":", hours)
                seconds = row[1].index(":", minutes+1)
                hoursString = timeString[0:hours]
                minutesString = timeString[minutes+1:seconds]
                secondsString = timeString[seconds+1:len(row[1])]
                #---- Transforms all hours, minutes, seconds to the change of time in seconds ----
                totaltime = timedelta(seconds=(int(secondsString) + (int(minutesString)*60) + (int(hoursString)*3600)))
            #---- Gets the change of time and converts into seconds and will continue until the number of seconds is equalivalent to 0 ----
            for remaining in range(int(totaltime.total_seconds()),0,-1):
                #---- Updates domor8123 lockset with a value of change of time that deletes the number of seconds ----
                results1 = """ UPDATE account
                SET lockset = %s
                WHERE username = %s"""
                results_data1 = (str(timedelta(seconds=remaining-1)), "domor8123")
                cursor.execute(results1, results_data1)
                conn.commit()
                #---- Replicates a pause of one second ----
                time.sleep(1)

#---- Uses the secret infrom in information.json file ----
with open("information.json") as secretinformation:
    #---- Loads json dictionary into a python dictionary ----
    data = json.load(secretinformation)
while True:
    #---- Creates a connection object with the user, password, host, port, and database in python dictionary ----
    conn = psycopg2.connect(user=data.get("databaseAddress")[0:data.get('databaseAddress').find("@")], password=data.get("databasePassword"), host=data.get("databaseAddress")[data.get("databaseAddress").find('@')+1:len(data.get("databaseAddress"))], database=data.get("database"))
    countdownTime()
