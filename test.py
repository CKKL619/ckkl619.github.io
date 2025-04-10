from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId
"""make excel
client = MongoClient("mongodb+srv://IoTadmin:admin888@maincluster.xh201.mongodb.net/")
database  = client.get_database("TestHistory")
chargercollection = database.get_collection("charger")

#records = chargercollection.find().skip(5).limit(5)
#for record in records:
#    print(record)

records = chargercollection.find().skip(5).limit(5)
df = pd.DataFrame(list(records))
df.to_excel('output_file.xlsx', index=False, engine='openpyxl')
print("Data exported successfully to 'output_file.xlsx'")
client.close()
print("close connection")
"""

"""
#the history record send to webpage
databaseConnection = MongoClient("mongodb+srv://IoTadmin:admin888@maincluster.xh201.mongodb.net/")
testdatabase = databaseConnection.get_database("TestDatabase")
historydatabase = databaseConnection.get_database("TestHistory")#connect to database history
chargerhis = historydatabase.get_collection("charger")
linkage = testdatabase.get_collection("linkage")

chargerOwner = ObjectId("6784559cdb5ebfa5ad8cc783")

thelinkage = linkage.find_one({'ownerid': chargerOwner})
thechargerid = thelinkage["chargerid"]

chargercollection = historydatabase.get_collection("charger")#getting the history data
records = chargercollection.find({"deviceid": thechargerid }).skip(0).limit(30)"""

databaseConnection = MongoClient("mongodb+srv://IoTadmin:admin888@maincluster.xh201.mongodb.net/")
testdatabase = databaseConnection.get_database("TestDatabase")

charger = testdatabase.get_collection("charger")#reach collections
human_motion = testdatabase.get_collection("human_motion")
panel = testdatabase.get_collection("panel")
#speaker = testdatabase.get_collection("speaker")
temp_humid = testdatabase.get_collection("temp_humid")
#user = testdatabase.get_collection("user")
waterleak =testdatabase.get_collection("waterleak")
linkage = testdatabase.get_collection("linkage")
#print("Connected database successfully")

chargerOwner = ObjectId("6784559cdb5ebfa5ad8cc783")

thelinkage = linkage.find_one({'ownerid': chargerOwner})
thechargerid = thelinkage["chargerid"]
themotionid = thelinkage["human_motionid"]
thepanelid = thelinkage["panelid"]
thetemphumidid = thelinkage["temp_humidid"]
thewaterleakid = thelinkage["waterleakid"]

themotion = human_motion.find_one({'_id': themotionid})
print(themotion)
thewaterleak = waterleak.find_one({'_id': thewaterleakid})
print(thewaterleak)
thecharger = charger.find_one({'_id': thechargerid})
print(thecharger)
thetemphumid = temp_humid.find_one({'_id': thetemphumidid})
print(thetemphumid)



