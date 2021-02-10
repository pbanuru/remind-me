#python libraries
import datetime
import random
from time import sleep
from flask import Flask, flash, redirect, render_template, request, session, abort
from multiprocessing import Process



#user libraries
from twilioAPI import sendMessage
from database import addMessage,removeMessage,readDatabase,writeDatabase

app = Flask(__name__)
    
@app.route("/",methods = ['POST', 'GET'])
def parseReminderAndQueue():
    statusMessage = ''
    if request.method == 'POST':
        result = request.form
        print(result)
        message,scheduledTime,phone = parseReminder(result)
        print("Parsed",message,scheduledTime,phone)
        addMessage(phone,message,scheduledTime)
        statusMessage = "Message Added"
    return render_template("index.html", statusMessage = statusMessage)


 
#functions 09-20-2020 22:05
#ImmutableMultiDict([('message', 'sleep at 10'), ('time', '2020-09-20T22:05'), ('number', '(408)-708-6711')])
def parseReminder(formOutput):
    tempTime = formOutput['time']
    tempTime = tempTime.replace('T', ' ')
    #'2020-09-20 22:05' T removed
    finalTime = tempTime[5:10]+ '-' +tempTime[0:4] + tempTime[10:16]
    #'09-20-2020 22:05' Month moved to end

    return formOutput['message'], finalTime, formOutput['number']


#Returns the current time in the format "MM-DD-YY hh:mm"
def timeCheck():
    #current_time = datetime.datetime.now()
    #current_time = f"{current_time.month}-{current_time.day}-{current_time.year} {current_time.hour}:{current_time.minute}"
    current_time = datetime.datetime.now().strftime("%m-%d-%Y %H:%M")
    return current_time
    
#repeatedly runs sendMessageIfTimeMatches, checking if it is time to send the "soonest" message in database.
def databaseLoop():
    while True:
        print("looping")
        sendMessageIfTimeMatches()
        sleep(5)

#Checks once if the current time matches the time a message must be sent, sends the message if yes, and removes that entry from the database.
def sendMessageIfTimeMatches():
    database = readDatabase()
    print("Database:", database)
    if database != []:
        current_time = timeCheck()
        print("CurrentTime:",current_time,"Scheduled:",database[0]["time"])
        if current_time >= database[0]["time"]:
            sendMessage(database[0])
            removeMessage()

#Code to Run
if __name__ == "__main__":
    writeDatabase([])
    p1 = Process(target = databaseLoop)
    p1.start()
    app.run()
    app.debug=True
    

    

    
    '''print(database,"\n")
    addMessage("4087296744","Hello2","9-19-2020 16:3")
    addMessage("4087296744","Hello3","9-19-2021 16:3")
    addMessage("4087296744","Hello3","9-18-2020 16:4")
    addMessage("4087296744","Hello3","3-19-2020 16:4")
    print(database,"\n")'''


