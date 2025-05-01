from pymongo import MongoClient
from bson.objectid import ObjectId

#   iswelcome() returns True if it is the situation of welcome
#   iserror()   returns True if it is the situation of error happened
#   isleave()   returns True if it is the situation of telling someone to leave
#   isputback() returns True if it is the situation of unproper placement of charger

"""expected usage:
import soundcondition

while true:
    if iswelcome():
        playwelcome()
    
    if iserror():
        playerror()

    if isleave():
        playleave()

    if isputback():
        playputback()
    
    time.sleep(2.5)

"""

databaseConnection = MongoClient("mongodb+srv://IoTadmin:admin888@maincluster.xh201.mongodb.net/")
testdatabase = databaseConnection.get_database("TestDatabase")

panelcollection = testdatabase.get_collection("panel")
linkagecollection = testdatabase.get_collection("linkage")
chargercollection = testdatabase.get_collection("charger")#reach collections
human_motioncollection = testdatabase.get_collection("human_motion")
#speaker = testdatabase.get_collection("speaker")
temp_humidcollection = testdatabase.get_collection("temp_humid")
#user = testdatabase.get_collection("user")
waterleakcollection =testdatabase.get_collection("waterleak")

chargerOwner = ObjectId("6784559cdb5ebfa5ad8cc783")

thelinkage = linkagecollection.find_one({'ownerid': chargerOwner})
thechargerid = thelinkage["chargerid"]
themotionid = thelinkage["human_motionid"]
thepanelid = thelinkage["panelid"]
thetemphumidid = thelinkage["temp_humidid"]
thewaterleakid = thelinkage["waterleakid"]

print("Connected successfully for read data")

historydatabase = databaseConnection.get_database("TestHistory")
human_motionhis = historydatabase.get_collection("human_motion")

def iswelcome():
    themotion = human_motioncollection.find_one({'_id': themotionid})#get the current human motion data
    ispresence = themotion["ispresence"]

    thecharger = chargercollection.find_one({'_id': thechargerid})
    isusing = thecharger["chargingStatus"]

    if isusing == "charger is being used":
        return False
    elif iserror():
        return False
    elif ispresence == "pir":
        return True
    else:
        return False
    
def iserror():
    thecharger = chargercollection.find_one({'_id': thechargerid})
    thecharger = thepanel["ischarger"]

    themotion = human_motioncollection.find_one({'_id': themotionid})#get the current human motion data
    ispresence = themotion["ispresence"]
    if thecharger == False and ispresence:
        return True
    else:
        return False
    
def isleave():
    thewaterleak = waterleakcollection.find_one({'_id': thewaterleakid})
    iswaterleak = thewaterleak["isleak"]

    themotion = human_motioncollection.find_one({'_id': themotionid})#get the current human motion data
    ispresence = themotion["ispresence"]

    themotionhis = human_motionhis.find({"deviceid":themotionid}).skip(0).limit(10)#check the data around 2 mins
    all_motion_true = all(doc.get("motion", False) for doc in themotionhis)

    if iswaterleak:
        return True
    
    if all_motion_true and ispresence:
        return True
    else:
        return False

def isputback():
    thecharger = chargercollection.find_one({'_id': thechargerid})
    isusing = thecharger["chargingStatus"]
    chargeroutput = thecharger["powerOutput"]
    themotion = human_motioncollection.find_one({'_id': themotionid})#get the current human motion data
    ispresence = themotion["ispresence"]

    if isusing and chargeroutput == "unknown" or chargeroutput == 0:
        if ispresence:
            return True
    else:
        return False
