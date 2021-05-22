#!/usr/bin/env python2
import requests
import json
import telegram
from telegram import ParseMode
from datetime import datetime
import urllib.parse
import sys
import os
url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict"

now = datetime.now()
today = now.strftime("%d-%m-%Y")
logtime = now.strftime("%d-%m-%Y %H:%M:%S")
print("Logging@", logtime)
my_token = '<BOT TOKEN GOES HERE>'
chatids = {"581":"@vaccineFinderHyderabad18","571":"@vaccineFinderChennai18","305":"-1001176270354","265":"@vaccineFinderBangalore18"}
districts = ["581","571","305","265"]
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Ch$ko) Chrome/90.0.4430.93 Safari/537.36"}
for dist in districts:
    PARAMS = {'district_id':dist,'date':today}
    response = requests.get(url, params = PARAMS, headers = headers)
    print(response.reason)
    responseData = response.json()
    y = json.dumps(responseData)
    serviceData = json.loads(y)
    count = 0
    print("Chat ID: "+chatids[dist])
    for center in serviceData["centers"]:
        for session in center["sessions"]:
            if session['available_capacity'] > 0 and session['min_age_limit'] == 18:
                centerName = center["name"]
                stateName = center["state_name"]
                centerAddress = center["address"]
                availableDate = session["date"]
                vaccineType = session["vaccine"]
                noofslotsdose1 = str(session["available_capacity_dose1"])
                noofslotsdose2 = str(session["available_capacity_dose2"])
                link = 'https://selfregistration.cowin.gov.in/'
                #googlemap = 'https://www.google.com/maps/search/?api=1&query='+urllib.parse.quote_plus(centerAddress)
                #message = "Hi, I Found a Slot for "+stateName+",\n Available Date: "+availableDate+",\n No. of Slots Available: "+noofslots+",\n Vaccine Type: "+ vaccineType+",\n Center Name: "+centerName+",\n Center Address: "+ centerAddress
                count = count+1
                botemoji = u'\U0001F916' 
                linkemoji = u'\U0001F517'
                mess = '<b>Available Date: </b>'+availableDate+'\n<b>Slots Available (Dose1): </b>'+noofslotsdose1+'\n<b>Slots Available (Dose2): </b>'+noofslotsdose2+'\n<b>Vaccine Type: </b>'+vaccineType+'\n<b>Center Name: </b>'+centerName+'\n<b>Center Address: </b>'+ centerAddress+'\n\n'+linkemoji+'\n\n'+ link
                directory = '/home/pi/vaccineFinder/data/'+today+'/'
                try:
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    with open(directory+session["session_id"]+'_data.txt') as json_file:
                        data = json.load(json_file)
                        print(data)
                    a, b = json.dumps(session, sort_keys=True), json.dumps(data, sort_keys=True)
                    print("session_id => "+session["session_id"])
                    print("a => "+a)
                    print("***************")
                    print("b => "+b)
                    if a == b:
                        print("Same response, skipping send message")
                        continue
                except OSError as e:
                    print(e.errno)

                

                with open(directory+session["session_id"]+'_data.txt', 'w') as outfile:
                    json.dump(session, outfile)
                if count >= 1:
                    print("Message is:"+mess)
                    bot = telegram.Bot(token=my_token)
                    bot.sendMessage(chat_id=chatids[dist], text=mess, parse_mode=ParseMode.HTML)
                    

