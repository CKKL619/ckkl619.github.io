1. for soundcondition.py

#   iswelcome() returns True if it is the situation of welcome
#   iserror()   returns True if it is the situation of error happened
#   isleave()   returns True if it is the situation of telling someone to leave
#   isputback() returns True if it is the situation of unproper placement of charger

"""example of calling function:

import soundcondition

while true:
    if soundcondition.iswelcome():
        playwelcome()
    
    if soundcondition.iserror():
        playerror()

    if soundcondition.isleave():
        playleave()

    if soundcondition.isputback():
        playputback()
    
    time.sleep(2.5)

"""
______________________________________________________________________________________________________
2. for getpower.py

#   getchargerpower()   returns True/False of charger power should be
#   getmotionpower()    returns True/False of motion sensor power should be
#   gettemphumidpower() returns True/False of temperature & humidity sensor power should be
#   getwaterleakpower() returns True/False of waterleak sensor power should be
#   getspeakerpower()   returns True/False of speaker power should be

"""example of calling function:

import getpower

power = getpower.getchargerpower()

if power == False:
    turnOffCharger()

"""
______________________________________________________________________________________________________
3. for updated flaskServer.py
# new variable "records" is added to data monitoring pages.
# "records" is a list with 20 json data in it. 
# "records" is the past 20 records 

# need to use a loop to retrieve data in html
    for record in records:
        print(record)

#example:

one record in charger records:
{'_id': ObjectId('6784559bdb5ebfa5ad8cc77e'), 'datetime': '2025-02-20 20:36:02', 'chargingStatus': 'unknown', 'energyConsumption': 'unknown', 'chargingTime': 'unknown', 'powerOutput': 'unknown', 'batteryLevel': 'unknown', 'gridImpact': 'unknown', 'power': True}

one record in human motion records:
{'_id': ObjectId('6784559cdb5ebfa5ad8cc77f'), 'datetime': '2025-03-22 09:18:12', 'ispresence': 'unknown', 'power': False}

one record in waterleak records:
{'_id': ObjectId('6784559cdb5ebfa5ad8cc784'), 'datetime': '2025-03-22 09:18:12', 'isleak': 'unknown', 'power': False}

one record in temperature and humidity records:
{'_id': ObjectId('6784559cdb5ebfa5ad8cc782'), 'datetime': '2025-03-22 09:18:12', 'temperature': 'unknown', 'humidity': 'unknown', 'power': False}
