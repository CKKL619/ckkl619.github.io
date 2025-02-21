from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
import Motion_sensor, Temp_Hum_sensor, Water_leak_sensor, charger_data, time

class makeJSON:
    def __init__(self):##defalt
        pass

    def speaker(soundtrack, power):#power should be on and off, TRUE and False
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S") 
        json = {"datetime":current_time,"soundtrack":soundtrack, "power": power}
        return json
    
    def user(ownedCharger, identity, manageCharger):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S") 
        json = {"datetime":current_time,"ownedCharger":ownedCharger, "identity": identity, "power": manageCharger}
        return json
    
    def th(temperature, humidity, power):#for temperature and humidity sensor
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S") 
        json = {"datetime":current_time,"temperature":temperature, "humidity": humidity, "power": power}
        return json

    def wl(isleak, power):#for waterleak sensor
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S") 
        json = {"datetime":current_time,"isleak":isleak, "power": power}
        return json
    
    def hm(ispresence, power):#for human motion sensor
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S") 
        json = {"datetime":current_time,"ispresence":ispresence,  "power": power}
        return json
    
    def charger(chargingStatus, energyConsumption, chargingTime, powerOutput, batteryLevel, gridImpact, power):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S") 
        json = {"datetime":current_time,"chargingStatus":chargingStatus, "energyConsumption": energyConsumption,"chargingTime": chargingTime, "powerOutput": powerOutput, "batteryLevel": batteryLevel,"gridImpact": gridImpact,"power": power}
        return json

    def panel(ischarger, iswlsensor, isthsensor, ishmsensor,isspeaker):#this is for controling the device
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S") 
        json = {"datetime":current_time,"iswlsensor":iswlsensor, "isthsensor": isthsensor,"ishmsensor": ishmsensor, "isspeaker": isspeaker,"ischarger":ischarger}
        return json
    
    def linkage(chargerid, human_motionid, panelid, speakerid, temp_humidid, ownerid, waterleakid):#linking devices together
        json = {"chargerid":chargerid,"human_motionid":human_motionid, "panelid": panelid,"speakerid": speakerid, "temp_humidid": temp_humidid, "ownerid": ownerid, "waterleakid": waterleakid}
        return json

class CreateAndUpdate:
    def buildAcharger():
        def __init__(self):##defalt
            pass
        def __init__(self, user):##defalt
            pass
    
        try:
            client = MongoClient("mongodb+srv://IoTadmin:admin888@maincluster.xh201.mongodb.net/")
            testdatabase  = client.get_database("TestDatabase")#reach database

            charger = testdatabase.get_collection("charger")#reach collections
            human_motion = testdatabase.get_collection("human_motion")
            panel = testdatabase.get_collection("panel")
            speaker = testdatabase.get_collection("speaker")
            temp_humid = testdatabase.get_collection("temp_humid")
            user = testdatabase.get_collection("user")
            waterleak =testdatabase.get_collection("waterleak")
            linkage = testdatabase.get_collection("linkage")
            print("Connected successfully")

            #making a charger in database with linkage to IOT device
            insertCharger = charger.insert_one(makeJSON.charger("Not charging", 0, 0, 0, 0, 0, False))
            print(f"charger inserted with id: {insertCharger.inserted_id}")#get the auto id
            print(insertCharger.acknowledged)

            insertHuman_motion = human_motion.insert_one(makeJSON.hm(False, "No activity", 0, False))
            print(f"charger inserted with id: {insertHuman_motion.inserted_id}")#get the auto id
            print(insertHuman_motion.acknowledged)

            insertPanel = panel.insert_one(makeJSON.panel(False, False, False, False, False))
            print(f"charger inserted with id: {insertPanel.inserted_id}")#get the auto id
            print(insertPanel.acknowledged)

            insertSpeaker = speaker.insert_one(makeJSON.speaker("some BSON soundstrack", False))
            print(f"charger inserted with id: {insertSpeaker.inserted_id}")#get the auto id
            print(insertSpeaker.acknowledged)

            insertTemp_humid = temp_humid.insert_one(makeJSON.th(25, 50, False))
            print(f"charger inserted with id: {insertTemp_humid.inserted_id}")#get the auto id
            print(insertTemp_humid.acknowledged)

            insertUser = user.insert_one(makeJSON.user(["id"], "admin", ["id","id","id","id"]))
            print(f"charger inserted with id: {insertUser.inserted_id}")#get the auto id
            print(insertUser.acknowledged)

            insertWaterleak = waterleak.insert_one(makeJSON.wl(False, 0, False))
            print(f"charger inserted with id: {insertWaterleak.inserted_id}")#get the auto id
            print(insertWaterleak.acknowledged)

            #it is strange that auto gen a user for charger, I will fix it later
            insertLinkage = linkage.insert_one(makeJSON.linkage(insertCharger.inserted_id, insertHuman_motion.inserted_id, insertPanel.inserted_id, insertSpeaker.inserted_id, insertTemp_humid.inserted_id, insertUser.inserted_id, insertWaterleak.inserted_id))
            print(f"charger inserted with id: {insertLinkage.inserted_id}")#get the auto id
            print(insertLinkage.acknowledged)
            
            client.close()
            print("close connection")

        except Exception as e:
            raise Exception("The following error occurred: ", e)
    def updatePower(panelid, device, power):#for control the on and off of device through web or app
        match device:
            case "charger":
                try:
                    client = MongoClient("mongodb+srv://IoTadmin:admin888@maincluster.xh201.mongodb.net/")
                    database  = client.get_database("TestDatabase")
                    linkagecollection = database.get_collection("linkage")
                    chargercollection = database.get_collection("charger")#change this line
                    
                    panelcollection = database.get_collection("panel")
                    updatepanel = panelcollection.update_one({"_id":ObjectId(panelid)},{"$set": {"ischarger":power} })
                    print("panel: charger updated")#log and debug
                    print(f"Charger updated: {updatepanel.modified_count}")

                    print("Connected successfully for update charger")

                    thelinkage = linkagecollection.find_one({'panelid': ObjectId(panelid)})

                    if thelinkage:
                        thedeviceid = thelinkage["chargerid"]#and this line
                        updateResult = chargercollection.update_one({"_id":thedeviceid},{"$set": {"power":power} })#and this line for the rest connection and update
                        print(f"Charger updated: {updateResult.modified_count}")
                        
                    else:
                        print(f"no linkage with this panel")
                    
                    client.close()
                    print("close connection")
                except Exception as e:
                    raise Exception("The following error occurred: ", e)
                return
            
            case"waterleak":
                try:
                    client = MongoClient("mongodb+srv://IoTadmin:admin888@maincluster.xh201.mongodb.net/")
                    database  = client.get_database("TestDatabase")
                    linkagecollection = database.get_collection("linkage")
                    waterleakcollection = database.get_collection("waterleak")

                    panelcollection = database.get_collection("panel")
                    updatepanel = panelcollection.update_one({"_id":ObjectId(panelid)},{"$set": {"iswlsensor":power} })
                    print("panel: waterleak updated")#log and debug
                    print(f"waterleak updated: {updatepanel.modified_count}")

                    print("Connected successfully for update waterleak")

                    thelinkage = linkagecollection.find_one({'panelid': ObjectId(panelid)})

                    if thelinkage:
                        thedeviceid = thelinkage["waterleakid"]
                        #print(f"Charger ID found: {thechargerid}")
                        updateResult = waterleakcollection.update_one({"_id":thedeviceid},{"$set": {"power":power} })
                        print(f"Charger updated: {updateResult.modified_count}")
                        
                    else:
                        print(f"no linkage with this panel")
                    
                    client.close()
                    print("close connection")
                except Exception as e:
                    raise Exception("The following error occurred: ", e)
                return
            
            case"temp_humid":
                try:
                    client = MongoClient("mongodb+srv://IoTadmin:admin888@maincluster.xh201.mongodb.net/")
                    database  = client.get_database("TestDatabase")
                    linkagecollection = database.get_collection("linkage")
                    temphumidcollection = database.get_collection("temp_humid")

                    panelcollection = database.get_collection("panel")
                    updatepanel = panelcollection.update_one({"_id":ObjectId(panelid)},{"$set": {"isthsensor":power} })
                    print("panel: temphumid updated")#log and debug
                    print(f"temphumid updated: {updatepanel.modified_count}")
                    
                    print("Connected successfully for update temphumid")

                    thelinkage = linkagecollection.find_one({'panelid': ObjectId(panelid)})

                    if thelinkage:
                        thedeviceid = thelinkage["temp_humidid"]
                        #print(f"Charger ID found: {thechargerid}")
                        updateResult = temphumidcollection.update_one({"_id":thedeviceid},{"$set": {"power":power} })
                        print(f"Charger updated: {updateResult.modified_count}")
                        
                    else:
                        print(f"no linkage with this panel")
                    
                    client.close()
                    print("close connection")
                except Exception as e:
                    raise Exception("The following error occurred: ", e)
                return
            
            case"human_motion":
                try:
                    client = MongoClient("mongodb+srv://IoTadmin:admin888@maincluster.xh201.mongodb.net/")
                    database  = client.get_database("TestDatabase")
                    linkagecollection = database.get_collection("linkage")
                    humanmotioncollection = database.get_collection("human_motion")

                    panelcollection = database.get_collection("panel")
                    updatepanel = panelcollection.update_one({"_id":ObjectId(panelid)},{"$set": {"ishmsensor":power} })
                    print("panel: humanmotion updated")#log and debug
                    print(f"humanmotion updated: {updatepanel.modified_count}")

                    print("Connected successfully for update humanmotion")

                    thelinkage = linkagecollection.find_one({'panelid': ObjectId(panelid)})

                    if thelinkage:
                        thedeviceid = thelinkage["human_motionid"]
                        #print(f"Charger ID found: {thechargerid}")
                        updateResult = humanmotioncollection.update_one({"_id":thedeviceid},{"$set": {"power":power} })
                        print(f"Charger updated: {updateResult.modified_count}")
                        
                    else:
                        print(f"no linkage with this panel")
                    
                    client.close()
                    print("close connection")
                except Exception as e:
                    raise Exception("The following error occurred: ", e)
                return
            
            case"speaker":
                try:
                    client = MongoClient("mongodb+srv://IoTadmin:admin888@maincluster.xh201.mongodb.net/")
                    database  = client.get_database("TestDatabase")
                    linkagecollection = database.get_collection("linkage")
                    speakercollection = database.get_collection("speaker")

                    panelcollection = database.get_collection("panel")
                    updatepanel = panelcollection.update_one({"_id":ObjectId(panelid)},{"$set": {"isspeaker":power} })
                    print("panel: speaker updated")#log and debug
                    print(f"speaker updated: {updatepanel.modified_count}")

                    print("Connected successfully for update speaker")

                    thelinkage = linkagecollection.find_one({'panelid': ObjectId(panelid)})

                    if thelinkage:
                        thedeviceid = thelinkage["speakerid"]
                        #print(f"Charger ID found: {thechargerid}")
                        updateResult = speakercollection.update_one({"_id":thedeviceid},{"$set": {"power":power} })
                        print(f"Charger updated: {updateResult.modified_count}")
                        
                    else:
                        print(f"no linkage with this panel")
                    
                    client.close()
                    print("close connection")
                except Exception as e:
                    raise Exception("The following error occurred: ", e)
                return
    def updateCharger(chargerid, device, JSONcontent):#for update the current status of devices and sensors(not finished)
        match device:
            case "charger":
                return
            case "temp_humid":
                try:
                    client = MongoClient("mongodb+srv://IoTadmin:admin888@maincluster.xh201.mongodb.net/")
                    database = client.get_database("TestDatabase")
                    linkagecollection = database.get_collection("linkage")
                    temphumidcollection = database.get_collection("temp_humid")
                    chargercollection = database.get_collection("charger")

                    print("Connected successfully for update charger's temp-humid")

                    thelinkage = linkagecollection.find_one({'chargerid': ObjectId(chargerid)})

                    if thelinkage:
                        thedeviceid = thelinkage["temp_humidid"]
                        # print(f"Charger ID found: {thechargerid}")
                        updateResult = temphumidcollection.update_one({"_id": thedeviceid}, {"$set": JSONcontent})
                        print(f"Charger updated: {updateResult.modified_count}")

                    else:
                        print(f"no linkage with this panel")

                    client.close()
                    print("close connection")
                except Exception as e:
                    raise Exception("The following error occurred: ", e)
                return updateResult.modified_count
            case "human_motion":
                return

class Read:
    def powerstatus(chargerid, device):#only checks charger for now
        try:
            client = MongoClient("mongodb+srv://IoTadmin:admin888@maincluster.xh201.mongodb.net/")
            database  = client.get_database("TestDatabase")

            chargercollection = database.get_collection("charger")
            print("Connected successfully for read charger")

            thecharger = chargercollection.find_one({'_id': ObjectId(chargerid)})
            powerstatus = thecharger["power"]
            return powerstatus
            
            client.close()
            print("close connection")
        except Exception as e:
            raise Exception("The following error occurred: ", e)
        return   

    def chargerlist(userid):
        pass




"""
    print("running")
    updateContent = makeJSON.th(00,00,True)
    print(updateContent)
    CreateAndUpdate.updateCharger("6784559bdb5ebfa5ad8cc77e","temp_humid",updateContent)
    print("done")
"""



"""testing update
    result = Read.powerstatus("6784559bdb5ebfa5ad8cc77e","charger")
    print(f"the result is: {result}")
    
    CreateAndUpdate.updatePower("6784559cdb5ebfa5ad8cc780","charger", False)
    CreateAndUpdate.updatePower("6784559cdb5ebfa5ad8cc780","waterleak", False)
    CreateAndUpdate.updatePower("6784559cdb5ebfa5ad8cc780","temp_humid", False)
    CreateAndUpdate.updatePower("6784559cdb5ebfa5ad8cc780","human_motion", False)
    CreateAndUpdate.updatePower("6784559cdb5ebfa5ad8cc780","speaker", False)
"""

"""testing connection
    #makeJSON.buildAcharger()

    try:
        client = MongoClient("mongodb+srv://IoTadmin:admin888@maincluster.xh201.mongodb.net/")
        database  = client.get_database("TestDatabase")
        collection = database.get_collection("TestCollection")
        print("Connected successfully")

        insertResult = collection.insert_one(makeJSON.speaker("new data",True))
        print(f"speaker inserted with id: {insertResult.inserted_id}")#insert
        print(insertResult.acknowledged)

        updateResult = collection.update_one({"soundtrack": "updated"}) 
        print(f"Documents updated: {updateResult.modified_count}")#update

        deleteResult = collection.delete_one({"name": "new data"}) 
        print(f"Documents deleted: {deleteResult.deleted_count}")#delete

        documents = collection.find() 
        for doc in documents: print(doc)

        #making a charger with linkage to IOT device

        client.close()
        print("close connection")

    except Exception as e:
        raise Exception("The following error occurred: ", e)
"""