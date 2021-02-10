#import Twilio functionality.
from twilio.rest import Client
 
# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure

#Creates the "content" of a message. Can be used in sendMessage(content) to test sending a message.
def getContentsOfMessage():
    content = {}
    phone = "4087486211"
    message = "wooshwoosh"
    scheduledTime = "9-19-2020 15:03"
    
    content["phone"] = phone
    content["message"] = message
    content["time"] = scheduledTime
    return content
    
#Sends message through Twilio
def sendMessage(content):

    credentials = open("credentials.txt", "r") #access credentials.txt file, please enter your Account SID, Auth Token, and Twilio phone number in credentials.txt
    for x, line in enumerate(credentials): #Reads specific lines of credentials.txt and saves to variables.
        x+=1
        if x == 2:
            account_sid = line
        if x == 5:
            auth_token = line
        if x == 8:
            twilio_phone_number = line
    credentials.close() #close credentials file

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=content["message"],
                        from_=twilio_phone_number, 
                        to=content["phone"]
                    )
    
    print(message.sid)


if __name__ == "__main__":
    sendMessage(getContentsOfMessage)