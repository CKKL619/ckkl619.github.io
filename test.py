import makeJSON
import time
from bson.objectid import ObjectId
from pymongo import MongoClient
#import Motion_sensor, Temp_Hum_sensor, Water_leak_sensor, charger_data

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

thecharger = charger.find_one(thechargerid)
chargernum = thecharger["chargeBoxId"]



print(chargernum)
def autoUpdate():
    while True:
        try:
            raw_motion_data = Motion_sensor.getMotion()
            motion_data = makeJSON.makeJSON.hm(raw_motion_data,True)
            themotion = human_motion.find_one_and_update({'_id': themotionid},{'$set': motion_data})
            thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set': {'ishmsensor': True}})
            print(f"motion:{themotion}panel{thepanel}")
        except Exception as e:
            motion_data = makeJSON.makeJSON.hm("unknown",False)
            themotion = human_motion.find_one_and_update({'_id': themotionid},{'$set': motion_data})
            thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set': {'ishmsensor': False}})
            print(f"update motion failed:{themotion}panel{thepanel}")

        try:
            raw_temperature_data = Temp_Hum_sensor.getTemperature()
            raw_humidity_data = Temp_Hum_sensor.getHumidity()
            temp_humid_data = makeJSON.makeJSON.th(raw_temperature_data,raw_humidity_data,True)
            thetemphumid = temp_humid.find_one_and_update({'_id': thetemphumidid},{'$set': temp_humid_data})
            thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set': {'isthsensor': True}})
            print(f"temp humid:{thetemphumid}panel{thepanel}")
        except Exception as e:
            temp_humid_data = makeJSON.makeJSON.th("unknown","unknown",False)
            thetemphumid = temp_humid.find_one_and_update({'_id': thetemphumidid},{'$set': temp_humid_data})
            thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set': {'isthsensor': False}})
            print(f"update temperature humidity failed:{thetemphumid}panel{thepanel}")

        try:
            raw_waterleak_data = Water_leak_sensor.getWaterleak()
            waterleak_data = makeJSON.makeJSON.wl(raw_waterleak_data,True)
            thewaterleak = waterleak.find_one_and_update({'_id': thewaterleakid},{'$set': waterleak_data})
            thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set': {'iswlsensor': True}})
            
            print(f"waterleak:{thewaterleak}panel{thepanel}")
        except Exception as e:
            waterleak_data = makeJSON.makeJSON.wl("unknown",False)
            thewaterleak = waterleak.find_one_and_update({'_id': thewaterleakid},{'$set': waterleak_data})
            thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set': {'iswlsensor': False}})
            print(f"update waterleak failed:{thewaterleak}panel{thepanel}")
    
        try:
            charger_id = 'CDJ940009'
            chargerData = charger_data.fetch_data_with_curl(charger_id)
            if chargerData != None:
                thecharger = charger.find_one_and_update({'_id': thechargerid},{'$set': chargerData})
                thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set':{'ischarger': True}})
                print(f"charger data:{chargerData}panel{thepanel}")   
            else:
                chargerData = makeJSON.makeJSON.charger("unknown", "unknown", "unknown", "unknown", "unknown", "unknown", False)
                thecharger = charger.find_one_and_update({'_id': thechargerid},{'$set': chargerData})
                thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set':{'ischarger': False}})
                print(f"update charger failed:{thecharger}panel{thepanel}") 
        except Exception as e:
            chargerData = makeJSON.makeJSON.charger("unknown", "unknown", "unknown", "unknown", "unknown", "unknown", False)
            thecharger = charger.find_one_and_update({'_id': thechargerid},{'$set': chargerData})
            thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set':{'ischarger': False}})
            print(f"update charger failed:{thecharger}panel{thepanel}")

        print("Complete one loop")
        time.sleep(2.5)

historydatabase = databaseConnection.client.get_database("TestHistory")#connect to database history
chargerhis = historydatabase.get_collection("charger")#reach collections
human_motionhis = historydatabase.get_collection("human_motion")
panelhis = historydatabase.get_collection("panel")
#speaker = testdatabase.get_collection("speaker")
temp_humidhis = historydatabase.get_collection("temp_humid")
#user = testdatabase.get_collection("user")
waterleakhis =historydatabase.get_collection("waterleak")
linkagehis = historydatabase.get_collection("linkage")
chargercollection = historydatabase.get_collection("charger")#getting the history data
records = list(chargercollection.find({"deviceid": thechargerid }).skip(0).limit(20))

temphumidcollection = historydatabase.get_collection("temp_humid")
threcords = temphumidcollection.find({"deviceid": thetemphumidid }).skip(0).limit(20)


temperature_list = [record['temperature'] for record in threcords]
threcords = temphumidcollection.find({"deviceid": thetemphumidid }).skip(0).limit(20)
humidity_list = [record['humidity'] for record in threcords]

print(humidity_list)
#autoUpdate()
