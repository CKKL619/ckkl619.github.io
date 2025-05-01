from bson.objectid import ObjectId
from pymongo import MongoClient

#   getchargerpower()   returns True/False of charger power should be
#   getmotionpower()    returns True/False of motion sensor power should be
#   gettemphumidpower() returns True/False of temperature & humidity sensor power should be
#   getwaterleakpower() returns True/False of waterleak sensor power should be
#   getspeakerpower()   returns True/False of speaker power should be

"""#example of calling function
import getpower

power = getpower.getchargerpower()

if power == False:
    turnOffCharger()
"""

databaseConnection = MongoClient("mongodb+srv://IoTadmin:admin888@maincluster.xh201.mongodb.net/")
database = databaseConnection.get_database("TestDatabase")

panelcollection = database.get_collection("panel")
linkagecollection = database.get_collection("linkage")

chargerOwner = ObjectId("6784559cdb5ebfa5ad8cc783")
thelinkage = linkagecollection.find_one({'ownerid': chargerOwner})
thepanelid = thelinkage["panelid"]

thepanel = panelcollection.find_one({'_id': thepanelid})
print("Connected successfully for read power")

def getchargerpower():
    power = thepanel["ischarger"]
    return power

def getmotionpower():
    power = thepanel["ishmsensor"]
    return power

def gettemphumidpower():
    power = thepanel["isthsensor"]
    return power

def getwaterleakpower():
    power = thepanel["iswlsensor"]
    return power

def getspeakerpower():
    power = thepanel["isspeaker"]
    return power


if __name__ == '__main__':
    print(getchargerpower())
    print(getmotionpower())
    print(gettemphumidpower())
    print(getwaterleakpower())
    print(getspeakerpower())
