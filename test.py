import makeJSON
import time
from bson.objectid import ObjectId
from pymongo import MongoClient
import json
from bson import ObjectId

class Database:
    def __init__(self, host):
        self.host = host
        self.client = MongoClient(host)
    
    def get_db(self):
        return self.client.get_connection()
    
    def close(self):
        self.client.close()

databaseConnection = Database("mongodb+srv://IoTadmin:admin888@maincluster.xh201.mongodb.net/")
database = databaseConnection.client.get_database("TestDatabase")
testdatabase = databaseConnection.client.get_database("TestDatabase")

charger = testdatabase.get_collection("charger")#reach collections
human_motion = testdatabase.get_collection("human_motion")
panel = testdatabase.get_collection("panel")
#speaker = testdatabase.get_collection("speaker")
temp_humid = testdatabase.get_collection("temp_humid")
#user = testdatabase.get_collection("user")
waterleak =testdatabase.get_collection("waterleak")
linkage = testdatabase.get_collection("linkage")
print("Connected successfully")

thelinkage = linkage.find_one({'ownerid': ObjectId("6784559cdb5ebfa5ad8cc783")})
thechargerid = thelinkage["chargerid"]
themotionid = thelinkage["human_motionid"]
thepanelid = thelinkage["panelid"]
thetemphumidid = thelinkage["temp_humidid"]
thewaterleakid = thelinkage["waterleakid"]

historydatabase = databaseConnection.client.get_database("TestHistory")#connect to database history
chargerhis = historydatabase.get_collection("charger")#reach collections
human_motionhis = historydatabase.get_collection("human_motion")
panelhis = historydatabase.get_collection("panel")
#speaker = testdatabase.get_collection("speaker")
temp_humidhis = historydatabase.get_collection("temp_humid")
#user = testdatabase.get_collection("user")
waterleakhis =historydatabase.get_collection("waterleak")
linkagehis = historydatabase.get_collection("linkage")
#print("Connected database history successfully")

def autoUpdate():
    while True:
        try:
            charger = testdatabase.get_collection("charger")
            thecharger = charger.find_one({'_id': thechargerid})##record to current database
            #print(thecharger)
            thechargerpower = thecharger["power"]
            thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set': {'ischarger': thechargerpower}})

            thecharger = charger.find_one({'_id': thechargerid})
            chargerjson = json.dumps(thecharger, default=str)
            #print(chargerjson)
            data_dict = json.loads(chargerjson)
            #print(data_dict)
            data_dict.pop("_id", None)
            #print(data_dict)
            data_dict["deviceid"] = thechargerid
            print(data_dict)
            #updated_chargerjson = json.dumps(data_dict)
            #print(updated_chargerjson)

            #chargerjson["deviceid"] = thechargerid
            thechargerhis = chargerhis.insert_one(data_dict)##record to history database
            print(thechargerhis)
            
        except Exception as e:
            chargerData = makeJSON.makeJSON.charger("unknown", "unknown", "unknown", "unknown", "unknown", "unknown", False)
            thecharger = charger.find_one_and_update({'_id': thechargerid},{'$set': chargerData})
            thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set':{'ischarger': False}})

            thechargerhis = chargerhis.insert_one(chargerData)
        print("Complete one loop")
        time.sleep(2.5)

autoUpdate()