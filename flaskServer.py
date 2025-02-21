from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import makeJSON, time
from bson.objectid import ObjectId
from pymongo import MongoClient
import Motion_sensor, Temp_Hum_sensor, Water_leak_sensor, charger_data
import threading

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
print("Connected successfully")

thelinkage = linkage.find_one({'ownerid': ObjectId("6784559cdb5ebfa5ad8cc783")})
thechargerid = thelinkage["chargerid"]
themotionid = thelinkage["human_motionid"]
thepanelid = thelinkage["panelid"]
thetemphumidid = thelinkage["temp_humidid"]
thewaterleakid = thelinkage["waterleakid"]

def autoUpdate():
    while True:
        try:
            human_motion = testdatabase.get_collection("human_motion")
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
            temp_humid = testdatabase.get_collection("temp_humid")
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
            waterleak =testdatabase.get_collection("waterleak")
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
            charger = testdatabase.get_collection("charger")
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

# Create and start the database update
update_thread = threading.Thread(target=autoUpdate)
update_thread.daemon = True  # Ensure the thread will exit when the main program exits
update_thread.start()

app = Flask(__name__)
sio = SocketIO(app)

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
    })

@app.route('/index.html') 
def index(): 
    return render_template('index.html')

@app.route('/home.html') 
def home(): 
    return render_template('home.html')

@app.route('/') 
def login(): 
    return render_template('login.html')

@app.route('/charger.html') 
def charger(): 
    charger = testdatabase.get_collection("charger")#reach collections
    thechargerid = thelinkage["chargerid"]
    thecharger = charger.find_one(thechargerid)
    print(thecharger["power"])
    power = thecharger["power"] if thecharger["power"] else False
    chargingStatus = thecharger["connectorStatus"] if thecharger["connectorStatus"] else "No Status"
    chargingTime = thecharger["chargingTime"] if thecharger["chargingTime"] else 0
    raw_chargerid = thecharger["_id"]
    chargerid = str(raw_chargerid) if raw_chargerid else "Can not fetch"
    return render_template('charger.html', power = power, chargingStatus=chargingStatus, chargingTime=chargingTime, chargerid = chargerid)

@app.route('/human_motion.html') 
def human_motion(): 
    human_motion = testdatabase.get_collection("human_motion")
    themotionid = thelinkage["human_motionid"]
    thesensor = human_motion.find_one(themotionid)

    power = thesensor["power"] if thesensor["power"] else False
    ispresence = thesensor["ispresence"] if thesensor["ispresence"] else "No Status"
    time = thesensor["datetime"] if thesensor["datetime"] else "No Status"
    return render_template('human_motion.html', power = power, ispresence = ispresence, time = time)

@app.route('/water.html') 
def water(): 
    waterleak =testdatabase.get_collection("waterleak")
    thewaterleakid = thelinkage["waterleakid"]
    thesensor = waterleak.find_one(thewaterleakid)

    power = thesensor["power"] if thesensor["power"] else False
    isleak = thesensor["isleak"] if thesensor["isleak"] else "No Status"
    time = thesensor["datetime"] if thesensor["datetime"] else "No Status"
    return render_template('water.html',power = power, isleak = isleak, time = time)

@app.route('/temp_humid.html') 
def temp_humid(): 
    temp_humid = testdatabase.get_collection("temp_humid")
    thesensor = temp_humid.find_one(thetemphumidid)
    power = thesensor["power"] if thesensor["power"] else False
    temperature = thesensor["temperature"] if thesensor["temperature"] else "unknown"
    humidity = thesensor["humidity"] if thesensor["humidity"] else "unknown"
    chargerid = thesensor["_id"] if thesensor["_id"] else "unknown"
    time = thesensor["datetime"] if thesensor["datetime"] else "unknown"
    return render_template('temp_humid.html',power = power, temperature = temperature, humidity =humidity, chargerid = chargerid,time=time)

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
    return jsonify(status="success")

if __name__ == '__main__': 
    #sio.start_background_task(target=updates_for_charger)
    sio.run(app, debug=True)