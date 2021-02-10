#python library
import datetime
import pickle

idCount = 0

#Functions

def readDatabase():
    pickle_off = open ("datafile.txt", "rb")
    database = pickle.load(pickle_off)
    return database


def writeDatabase(newDatabase):
    with open('datafile.txt', 'wb') as fh:
        pickle.dump(newDatabase, fh)

def clearDatabase():
    writeDatabase([])


#Assigns an ID to each database entry, to keep track of additions and removals.
def messageID():
    global idCount
    idCount = idCount + 1
    return idCount

#Adds a message to database and sorts it.
def addMessage(phone,message,scheduledTime):
    database = readDatabase()
    addedID = messageID()
    data = {"id":addedID,"phone":phone,"message":message,"time":scheduledTime}
    database.append(data)
    writeDatabase(database)
    sortDatabase()
    print(f"Message {addedID} has been added")

#Removes the first database entry (used after message is sent)
def removeMessage():
    database = readDatabase()
    temporaryID = database[0]["id"]
    writeDatabase(database[1:])
    print(f"Message {temporaryID} has been removed")


#Sorts the database entries from soonest to latest.
def sortDatabase():
    database = readDatabase()
    database = sorted(database, key=lambda k: datetime.datetime.strptime(k["time"], "%m-%d-%Y %H:%M"))
    writeDatabase(database)
    print(database)
    

if __name__ == "__main__":
    readDatabase()
    writeDatabase([9999])
    database = readDatabase()
    print(type(database),database)
    database.append(3333)
    print(type(database),database)
    writeDatabase(database)
    readDatabase()


