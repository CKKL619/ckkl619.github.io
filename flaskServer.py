from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import makeJSON, time,json
from bson.objectid import ObjectId
from pymongo import MongoClient
import Motion_sensor, Temp_Hum_sensor, Water_leak_sensor#, charger_data
import threading
from datetime import datetime

databaseConnection = MongoClient("mongodb+srv://IoTadmin:admin888@maincluster.xh201.mongodb.net/")
database = databaseConnection.get_database("TestDatabase")
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

historydatabase = databaseConnection.get_database("TestHistory")#connect to database history
chargerhis = historydatabase.get_collection("charger")#reach collections
human_motionhis = historydatabase.get_collection("human_motion")
panelhis = historydatabase.get_collection("panel")
#speaker = testdatabase.get_collection("speaker")
temp_humidhis = historydatabase.get_collection("temp_humid")
#user = testdatabase.get_collection("user")
waterleakhis =historydatabase.get_collection("waterleak")
linkagehis = historydatabase.get_collection("linkage")
#print("Connected database history successfully")

def autoUpdate():#set time limit for one loop, save cpu power
    while True:
        try:
            human_motion = testdatabase.get_collection("human_motion")
            raw_motion_data = Motion_sensor.getMotion()
            motion_data = makeJSON.makeJSON.hm(raw_motion_data,True)
            themotion = human_motion.find_one_and_update({'_id': themotionid},{'$set': motion_data})##record to current database
            thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set': {'ishmsensor': True}})

            motion_data["deviceid"] = themotionid
            themotionhis = human_motionhis.insert_one(motion_data)##record to history database
            #print(f"motion history:{themotionhis} motion:{themotion}")
        except Exception as e:
            motion_data = makeJSON.makeJSON.hm("unknown",False)
            themotion = human_motion.find_one_and_update({'_id': themotionid},{'$set': motion_data})
            thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set': {'ishmsensor': False}})
            
            motion_data["deviceid"] = themotionid
            themotionhis = human_motionhis.insert_one(motion_data)
            #print(f"motion history:{themotionhis} motion:{themotion}")

        try:
            temp_humid = testdatabase.get_collection("temp_humid")
            raw_temperature_data = Temp_Hum_sensor.getTemperature()
            raw_humidity_data = Temp_Hum_sensor.getHumidity()
            temp_humid_data = makeJSON.makeJSON.th(raw_temperature_data,raw_humidity_data,True)
            thetemphumid = temp_humid.find_one_and_update({'_id': thetemphumidid},{'$set': temp_humid_data})
            thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set': {'isthsensor': True}})

            temp_humid_data["deviceid"] = thetemphumidid
            thetemphumidhis = temp_humidhis.insert_one(temp_humid_data)
            #print(f"temp humid:{thetemphumid}panel{thepanel}")
        except Exception as e:
            temp_humid_data = makeJSON.makeJSON.th("unknown","unknown",False)
            thetemphumid = temp_humid.find_one_and_update({'_id': thetemphumidid},{'$set': temp_humid_data})
            thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set': {'isthsensor': False}})

            temp_humid_data["deviceid"] = thetemphumidid
            thetemphumidhis = temp_humidhis.insert_one(temp_humid_data)
            #print(f"update temperature humidity failed:{thetemphumid}panel{thepanel}")

        try:
            waterleak =testdatabase.get_collection("waterleak")
            raw_waterleak_data = Water_leak_sensor.getWaterleak()
            waterleak_data = makeJSON.makeJSON.wl(raw_waterleak_data,True)
            thewaterleak = waterleak.find_one_and_update({'_id': thewaterleakid},{'$set': waterleak_data})
            thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set': {'iswlsensor': True}})
            
            waterleak_data["deviceid"] = thewaterleakid
            thewaterleakhis = waterleakhis.insert_one(waterleak_data)
            #print(f"waterleak:{thewaterleak}panel{thepanel}")
            
        except Exception as e:
            waterleak_data = makeJSON.makeJSON.wl("unknown",False)
            thewaterleak = waterleak.find_one_and_update({'_id': thewaterleakid},{'$set': waterleak_data})
            thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set': {'iswlsensor': False}})

            waterleak_data["deviceid"] = thewaterleakid
            thewaterleakhis = waterleakhis.insert_one(waterleak_data)
            #print(f"update waterleak failed:{thewaterleak}panel{thepanel}")
    
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
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S") 
            data_dict["deviceid"] = thechargerid
            data_dict["datetime"] = current_time
            #print(data_dict)
            #updated_chargerjson = json.dumps(data_dict)
            #print(updated_chargerjson)

            #chargerjson["deviceid"] = thechargerid
            thechargerhis = chargerhis.insert_one(data_dict)##record to history database
            #print(thechargerhis)

        except Exception as e:
            chargerData = makeJSON.makeJSON.charger("unknown", "unknown", "unknown", "unknown", "unknown", "unknown", False)
            thecharger = charger.find_one_and_update({'_id': thechargerid},{'$set': chargerData})
            thepanel = panel.find_one_and_update({'_id': thepanelid},{'$set':{'ischarger': False}})

            thechargerhis = chargerhis.insert_one(chargerData)

        #print("Complete one loop")
        time.sleep(5)

# Create and start the database update
update_thread = threading.Thread(target=autoUpdate)
update_thread.daemon = True  # Ensure the thread will exit when the main program exits
update_thread.start()

app = Flask(__name__)

sio = SocketIO(app)
"""
@sio.on('connect', namespace='/charger.html')
def connect():
    print('connect')

@sio.on('disconnect')
def disconnect():
    databaseConnection.client.close()
    print('disconnect')

def on_charger_update(charger_id, new_status):
    sio.emit('status_update', 
        {'id': charger_id, 'status': new_status}, 
        namespace='/chargers')

def updates_for_charger():
    while True:
        time.sleep(2)
        chargercollection = database.get_collection("charger")
        linkagecollection = database.get_collection("linkage")

        thelinkage = linkagecollection.find_one({'ownerid': ObjectId("6784559cdb5ebfa5ad8cc783")})
        thechargerid = thelinkage["chargerid"]
        thecharger = chargercollection.find_one(thechargerid)
        print(thecharger["power"])
        state = thecharger["power"] if thecharger["power"] else False
        chargingStatus = thecharger["chargingStatus"] if thecharger["chargingStatus"] else 0
        energyConsumption = thecharger["energyConsumption"] if thecharger["energyConsumption"] else False

        sio.emit('update_data', {
                'state': state,
                'chargingStatus': chargingStatus,
                'energyConsumption': energyConsumption
            })

def send_update(state, chargingStatus, energyConsumption):
    sio.emit('update_data', {
        'state': state,
        'chargingStatus': chargingStatus,
        'energyConsumption': energyConsumption
    })"""

@app.route('/index.html') 
def index(): 
    return render_template('index.html')

@app.route('/home.html') 
def home(): 
    charger = testdatabase.get_collection("charger")#reach collections and find current data
    thechargerid = thelinkage["chargerid"]
    thecharger = charger.find_one(thechargerid)
    #print(thecharger["power"])
    chpower = thecharger["power"] if thecharger["power"] else False
    chargingStatus = thecharger["connectorStatus"] if thecharger["connectorStatus"] else "No Status"
    chargingTime = thecharger["chargingTime"] if thecharger["chargingTime"] else 0
    raw_chargerid = thecharger["_id"]
    chargerid = str(raw_chargerid) if raw_chargerid else "Can not fetch"

    chargernum = thecharger["chargeBoxId"]
    
    
    chargercollection = historydatabase.get_collection("charger")#getting the history data
    chrecords = chargercollection.find({"deviceid": thechargerid }).skip(0).limit(20)
    #charger end

    human_motion = testdatabase.get_collection("human_motion")
    themotionid = thelinkage["human_motionid"]
    thesensor = human_motion.find_one(themotionid)

    hmpower = thesensor["power"] if thesensor["power"] else False
    ispresence = thesensor["ispresence"] if thesensor["ispresence"] else "No Status"
    hmtime = thesensor["datetime"] if thesensor["datetime"] else "No Status"

    human_motioncollection = historydatabase.get_collection("human_motion")
    hmrecords = human_motioncollection.find({"deviceid": themotionid }).skip(0).limit(20)
    #human_motion end

    waterleak =testdatabase.get_collection("waterleak")
    thewaterleakid = thelinkage["waterleakid"]
    thesensor = waterleak.find_one(thewaterleakid)

    wlpower = thesensor["power"] if thesensor["power"] else False
    isleak = thesensor["isleak"] if thesensor["isleak"] else "No Status"
    wltime = thesensor["datetime"] if thesensor["datetime"] else "No Status"

    waterleakcollection = historydatabase.get_collection("waterleak")
    wlrecords = waterleakcollection.find({"deviceid": thewaterleakid }).skip(0).limit(20)
    #waterleak end


    temp_humid = testdatabase.get_collection("temp_humid")
    thesensor = temp_humid.find_one(thetemphumidid)
    thpower = thesensor["power"] if thesensor["power"] else False
    temperature = thesensor["temperature"] if thesensor["temperature"] else "unknown"
    humidity = thesensor["humidity"] if thesensor["humidity"] else "unknown"
    chargerid = thesensor["_id"] if thesensor["_id"] else "unknown"
    thtime = thesensor["datetime"] if thesensor["datetime"] else "unknown"

    temphumidcollection = historydatabase.get_collection("temp_humid")
    threcords = temphumidcollection.find({"deviceid": thetemphumidid }).skip(0).limit(20)
    #get data for excel

    times_list = [record["datetime"] for record in chrecords]
    chrecords = chargercollection.find({"deviceid": thechargerid }).skip(0).limit(20)
    chargingStatus_list = [record["connectorStatus"] for record in chrecords]
    chrecords = chargercollection.find({"deviceid": thechargerid }).skip(0).limit(20)
    chargingTime_list = [record["chargingTime"] for record in chrecords]
    chrecords = chargercollection.find({"deviceid": thechargerid }).skip(0).limit(20)
    current_list = [record.get("meterValues", {}).get("values", {}).get("current.import", {}).get("value", None) for record in chrecords]

    ispresence_list = ["present" if record['ispresence'] == 'pir' else "normal" for record in hmrecords]
    isleak_list = ["No" if record['isleak'] == 'unknown' or 'normal' else "Alert" for record in wlrecords]
    temperature_list = [record['temperature'] for record in threcords]
    threcords = temphumidcollection.find({"deviceid": thetemphumidid }).skip(0).limit(20)
    humidity_list = [record['humidity'] for record in threcords]

    
    return render_template('home.html',chpower = chpower, chargingStatus=chargingStatus, chargingTime=chargingTime, chargernum = chargernum, chrecords=chrecords,hmpower = hmpower, ispresence = ispresence, hmtime = hmtime, hmrecords=hmrecords,wlpower = wlpower, isleak = isleak, wltime = wltime, wlrecords=wlrecords,thpower = thpower, temperature = temperature, humidity =humidity, thtime=thtime, threcords=threcords,times_list=times_list,chargingStatus_list=chargingStatus_list,chargingTime_list=chargingTime_list,current_list=current_list,ispresence_list=ispresence_list,isleak_list=isleak_list,temperature_list=temperature_list,humidity_list=humidity_list)

@app.route('/') 
def login(): 
    return render_template('login.html')

@app.route('/charger.html')
def charger():
    charger = testdatabase.get_collection("charger")#reach collections and find current data
    thechargerid = thelinkage["chargerid"]
    thecharger = charger.find_one(thechargerid)
    #print(thecharger["power"])
    power = thecharger["power"] if thecharger["power"] else False
    connectorStatus = thecharger["connectorStatus"] if thecharger["connectorStatus"] else "No Status"
    chargingTime = thecharger["chargingTime"] if thecharger["chargingTime"] else 0
    raw_chargerid = thecharger["_id"]
    chargerid = str(raw_chargerid) if raw_chargerid else "Can not fetch"
    chargernum = thecharger["chargeBoxId"]

    chargercollection = historydatabase.get_collection("charger")#getting the history data
    records = list(chargercollection.find({"deviceid": thechargerid }).sort([("datetime", -1)]).limit(80))

    # Prepare data for line graph
    #time
    rawtimes = [record['datetime'] for record in records]
    times = [rawtimes[i] for i in range(0, 80, 4)][:20]
    #status
    rawchargingStatus_values = [record['connectorStatus'] for record in records]  # Convert presence to binary
    chargingStatus_values = [rawchargingStatus_values[i] for i in range(0, 80, 4)][:20]
    #charging time
    rawchargingTime_values = [record['chargingTime'] for record in records]
    chargingTime_values = [rawchargingTime_values[i] for i in range(0, 80, 4)][:20]
    #current
    rawcurrent = [record["meterValues"]["values"]["voltage"]["value"] for record in records]
    current = [rawcurrent[i] for i in range(0, 80, 4)][:20]
    """
    # need to use a loop to retrieve data in html, maximum 20 records can be read
    #example one record of records in a charger:
    # {'_id': ObjectId('67de0fdfe874ecbc00b5779c'), 'datetime': '2025-03-22 09:18:23', 'chargingStatus': 'unknown', 'energyConsumption': 'unknown', 'chargingTime': 'unknown', 'powerOutput': 'unknown', 'batteryLevel': 'unknown', 'gridImpact': 'unknown', 'power': False, 'deviceid': ObjectId('67b4821e8f08dba277e9fed6')}
    #expected usage in html

    for record in records:
        print(record)
    """
    return render_template('charger.html', power = power, connectorStatus=connectorStatus, chargingTime=chargingTime, chargernum = chargernum, records=records, chargingStatus_values = chargingStatus_values, chargingTime_values = chargingTime_values,times=times,current=current)

@app.route('/human_motion.html')
def human_motion():
    human_motion = testdatabase.get_collection("human_motion")
    themotionid = thelinkage["human_motionid"]
    thesensor = human_motion.find_one(themotionid)

    power = thesensor["power"] if thesensor["power"] else False
    ispresence = thesensor["ispresence"] if thesensor["ispresence"] else "No Status"
    time = thesensor["datetime"] if thesensor["datetime"] else "No Status"

    human_motioncollection = historydatabase.get_collection("human_motion")
    records = list(human_motioncollection.find({"deviceid": themotionid}).skip(0).limit(20))

    # Prepare data for line graph
    #time
    timesrecords = list(human_motioncollection.find({"deviceid": themotionid }).sort([("datetime", -1)]).limit(80))
    rawtimes = [record['datetime'] for record in timesrecords]
    times = [rawtimes[i] for i in range(0, 80, 4)][:20]
    #ispresence
    ispresencerecords = list(human_motioncollection.find({"deviceid": themotionid }).sort([("datetime", -1)]).limit(80))
    rawispresence_values = [1 if record['ispresence'] == 'pir' else 0 for record in ispresencerecords]
    ispresence_values = [rawispresence_values[i] for i in range(0, 80, 4)][:20]

    charger = testdatabase.get_collection("charger")#read charger number
    thecharger = charger.find_one(thechargerid)
    chargernum = thecharger["chargeBoxId"]
    chargerid = thechargerid
    """
    # example one record of records in a human motion sensor: ispresence could be "pir" or "unknown"
    #{'_id': ObjectId('6784559cdb5ebfa5ad8cc77f'), 'datetime': '2025-03-22 09:18:12', 'ispresence': 'unknown', 'power': False}
    for record in records:
        print(record)

    """
    return render_template('human_motion.html', power = power, ispresence = ispresence, time = time, records=records, times=times, ispresence_values=ispresence_values,chargernum = chargernum)

@app.route('/water.html')
def water():
    waterleak =testdatabase.get_collection("waterleak")
    thewaterleakid = thelinkage["waterleakid"]
    thesensor = waterleak.find_one(thewaterleakid)

    power = thesensor["power"] if thesensor["power"] else False
    isleak = thesensor["isleak"] if thesensor["isleak"] else "No Status"
    time = thesensor["datetime"] if thesensor["datetime"] else "No Status"

    waterleakcollection = historydatabase.get_collection("waterleak")

    # Prepare data for line graph
    #time
    timesrecords = list(waterleakcollection.find({"deviceid": thewaterleakid }).sort([("datetime", -1)]).limit(80))
    rawtimes = [record['datetime'] for record in timesrecords]
    times = [rawtimes[i] for i in range(0, 80, 4)][:20]
    #isleak value
    isleakrecords = list(waterleakcollection.find({"deviceid": thewaterleakid }).sort([("datetime", -1)]).limit(80))
    rawisleak_values = [0 if record['isleak'] == 'unknown' or 'normal' else 1 for record in isleakrecords]
    isleak_values = [rawisleak_values[i] for i in range(0, 80, 4)][:20]

    charger = testdatabase.get_collection("charger")#read charger number
    thecharger = charger.find_one(thechargerid)
    chargernum = thecharger["chargeBoxId"]
    chargerid = thechargerid
    """
    # example one record of records in a waterleak sensor:
    #{'_id': ObjectId('6784559cdb5ebfa5ad8cc784'), 'datetime': '2025-03-22 09:18:12', 'isleak': 'unknown', 'power': False}
    for record in records:
        print(record)

    """
    return render_template('water.html',power = power, isleak = isleak, time = time, times=times, isleak_values=isleak_values,chargernum = chargernum)

@app.route('/temp_humid.html')
def temp_humid():
    temp_humid = testdatabase.get_collection("temp_humid")
    thesensor = temp_humid.find_one(thetemphumidid)
    power = thesensor["power"] if thesensor["power"] else False
    temperature = thesensor["temperature"] if thesensor["temperature"] else "unknown"
    humidity = thesensor["humidity"] if thesensor["humidity"] else "unknown"
    time = thesensor["datetime"] if thesensor["datetime"] else "unknown"

    temp_humidcollection = historydatabase.get_collection("temp_humid")

    # Prepare data for line graph
    #time data
    timesrecords = list(temp_humidcollection.find({"deviceid": thetemphumidid }).sort([("datetime", -1)]).limit(80))
    rawtimes = [record['datetime'] for record in timesrecords]
    times = [rawtimes[i] for i in range(0, 80, 4)][:20]
    #humidity data
    humidrecords = list(temp_humidcollection.find({"deviceid": thetemphumidid }).sort([("datetime", -1)]).limit(80))
    rawhumidity_values = [record['humidity'] for record in humidrecords]
    humidity_values = [rawhumidity_values[i] for i in range(0, 80, 4)][:20]
    #temperature data
    temprecords = list(temp_humidcollection.find({"deviceid": thetemphumidid }).sort([("datetime", -1)]).limit(80))
    rawtemperature_list = [record['temperature'] for record in temprecords]
    temperature_values = [rawtemperature_list[i] for i in range(0, 80, 4)][:20]

    chargerid = thechargerid
    charger = testdatabase.get_collection("charger")#read charger number
    thecharger = charger.find_one(thechargerid)
    chargernum = thecharger["chargeBoxId"]
    """
    # example one record of records in a temp humid sensor:
    #{'_id': ObjectId('6784559cdb5ebfa5ad8cc782'), 'datetime': '2025-03-22 09:18:12', 'temperature': 'unknown', 'humidity': 'unknown', 'power': False}
    for record in records:
        print(record)

    """
    return render_template('temp_humid.html',power = power, temperature = temperature, humidity =humidity, chargernum = chargernum,time=time, times=times, temperature_values = temperature_values, humidity_values = humidity_values)

@app.route("/toggleChargerTrue", methods=['POST'])
def togglechargertrue():
    print("toggled c true")
    try:
        panel = testdatabase.get_collection("panel")
        updatepanel = panel.update_one({"_id":thepanelid},{"$set": {"ischarger":True} })#update panel
        #log and debug
        print(f"Charger updated: {updatepanel.modified_count}")

        charger = testdatabase.get_collection("charger")
        updateResult = charger.update_one({"_id":thechargerid},{"$set": {"power":True} })#update charger
        print(f"Charger updated: {updateResult.modified_count}")
    except Exception as e:
        return jsonify(status="error", message=str(e))
                
    return jsonify(status="success")

@app.route("/toggleChargerFalse", methods=['POST'])
def togglechargerfalse():
    print("toggled c false")
    try:
        panel = testdatabase.get_collection("panel")
        updatepanel = panel.update_one({"_id":thepanelid},{"$set": {"ischarger":False} })#update panel
        #log and debug
        print(f"Charger updated: {updatepanel.modified_count}")

        charger = testdatabase.get_collection("charger")
        updateResult = charger.update_one({"_id":thechargerid},{"$set": {"power":False} })#update charger
        print(f"Charger updated: {updateResult.modified_count}")
    except Exception as e:
        return jsonify(status="error", message=str(e))
                
    return jsonify(status="success")
"""
@app.route("/toggleWaterleakTrue", methods=['POST'])
def toggleWaterleakTrue():
    print("toggled wl true")
    try:
        panel = testdatabase.get_collection("panel")
        updatepanel = panel.update_one({"_id":thepanelid},{"$set": {"iswlsensor":True} })#update panel
        #log and debug
        print(f"wl updated: {updatepanel.modified_count}")

        waterleak =testdatabase.get_collection("waterleak")
        updateResult = waterleak.update_one({"_id":thewaterleakid},{"$set": {"power":True} })#update charger
        print(f"wl updated: {updateResult.modified_count}")
    except Exception as e:
        return jsonify(status="error", message=str(e))
    return jsonify(status="success")

@app.route("/toggleWaterleakFalse", methods=['POST'])
def toggleWaterleakFalse():
    print("toggled wl false")
    try:
        panel = testdatabase.get_collection("panel")
        updatepanel = panel.update_one({"_id":thepanelid},{"$set": {"iswlsensor":False} })#update panel
        #log and debug
        print(f"wl updated: {updatepanel.modified_count}")

        waterleak =testdatabase.get_collection("waterleak")
        updateResult = waterleak.update_one({"_id":thewaterleakid },{"$set": {"power":False} })#update charger
        print(f"wl updated: {updateResult.modified_count}")
    except Exception as e:
        return jsonify(status="error", message=str(e))
    return jsonify(status="success")
    
@app.route("/toggleHuman_motionTrue", methods=['POST'])
def toggleHuman_motionTrue():
    try:
        panel = testdatabase.get_collection("panel")
        updatepanel = panel.update_one({"_id":thepanelid},{"$set": {"ishmsensor":True} })#update panel
        #log and debug
        print(f"hm updated: {updatepanel.modified_count}")

        human_motion = testdatabase.get_collection("human_motion")
        updateResult = human_motion.update_one({"_id":themotionid},{"$set": {"power":True} })#update charger
        print(f"hm updated: {updateResult.modified_count}")
    except Exception as e:
        return jsonify(status="error", message=str(e))
    return jsonify(status="success")

@app.route("/toggleHuman_motionFalse", methods=['POST'])
def toggleHuman_motionFalse():
    try:
        panel = testdatabase.get_collection("panel")
        updatepanel = panel.update_one({"_id":thepanelid},{"$set": {"ishmsensor":False} })#update panel
        #log and debug
        print(f"hm updated: {updatepanel.modified_count}")

        human_motion = testdatabase.get_collection("human_motion")
        updateResult = human_motion.update_one({"_id":themotionid},{"$set": {"power":False} })#update charger
        print(f"hm updated: {updateResult.modified_count}")
    except Exception as e:
        return jsonify(status="error", message=str(e))
    return jsonify(status="success")

@app.route("/toggleTemp_humidTrue", methods=['POST'])
def toggleTemp_humidTrue():
    try:
        panel = testdatabase.get_collection("panel")
        updatepanel = panel.update_one({"_id":thepanelid},{"$set": {"isthsensor":True} })#update panel
        #log and debug
        print(f"Charger updated: {updatepanel.modified_count}")

        temp_humid = testdatabase.get_collection("temp_humid")
        updateResult = temp_humid.update_one({"_id":thetemphumidid},{"$set": {"power":True} })#update charger
        print(f"Charger updated: {updateResult.modified_count}")
    except Exception as e:
        return jsonify(status="error", message=str(e))
    return jsonify(status="success")

@app.route("/toggleTemp_humidFalse", methods=['POST'])
def toggleTemp_humidFalse():
    try:
        panel = testdatabase.get_collection("panel")
        updatepanel = panel.update_one({"_id":thepanelid},{"$set": {"isthsensor":False} })#update panel
        #log and debug
        print(f"Charger updated: {updatepanel.modified_count}")

        temp_humid = testdatabase.get_collection("temp_humid")
        updateResult = temp_humid.update_one({"_id":thetemphumidid},{"$set": {"power":False} })#update charger
        print(f"Charger updated: {updateResult.modified_count}")
    except Exception as e:
        return jsonify(status="error", message=str(e))
    return jsonify(status="success")"""

##for real-time refresh
@app.route('/getChargerStatus/<charger_number>')
def get_charger_status(charger_number):
    # Get the current status of the charger
    # This is a placeholder - replace with your actual database query
    status = "OFF"  # Default status
    try:
        # Query your database for the current status
        # Example: status = db.query("SELECT status FROM chargers WHERE charger_number = %s", [charger_number])
        return jsonify({"status": status})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/getChargerHistory/<charger_number>/<count>')
def get_charger_history(charger_number, count):
    # Get the history records for the charger
    # This is a placeholder - replace with your actual database query
    try:
        # Query your database for the history records
        # Example: history = db.query("SELECT * FROM charger_history WHERE charger_number = %s ORDER BY timestamp DESC LIMIT %s", [charger_number, count])
        
        # Placeholder data
        history = [
            {"charger_number": charger_number, "power": "ON", "charging_status": "Charging", "charging_time": "10:00"},
            {"charger_number": charger_number, "power": "OFF", "charging_status": "Not Charging", "charging_time": "09:30"}
        ]
        
        return jsonify(history)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/getChargerGraphData/<charger_number>')
def get_charger_graph_data(charger_number):
    # Get the graph data for the charger
    # This is a placeholder - replace with your actual database query
    try:
        # Query your database for the graph data
        # Example: data = db.query("SELECT timestamp, current FROM charger_data WHERE charger_number = %s ORDER BY timestamp", [charger_number])
        
        # Placeholder data
        times = ["09:00", "09:15", "09:30", "09:45", "10:00"]
        values = [10, 15, 20, 25, 30]
        
        return jsonify({"labels": times, "values": values})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/getDashboardData')
def get_dashboard_data():
    # Get the dashboard data
    # This is a placeholder - replace with your actual database query
    try:
        # Query your database for the dashboard data
        # Example: data = db.query("SELECT * FROM dashboard_stats")
        
        # Placeholder data
        data = {
            "total_chargers": 10,
            "active_chargers": 5,
            "total_energy": "100 kWh",
            "average_charging_time": "45 min"
        }
        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/getCurrentTime')
def get_current_time():
    # Get the current time
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return jsonify({"time": current_time})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__': 
    #sio.start_background_task(target=updates_for_charger)
    sio.run(app, debug=True)
