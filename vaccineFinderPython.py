#!/usr/bin/env python2
import requests
import json
import telegram
from telegram import ParseMode
from datetime import datetime
import urllib.parse
url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
today = now.strftime("%d-%m-%Y")
logtime = now.strftime("%d-%m-%Y %H:%M:%S")
print("Logging@", logtime)
my_token = 'BOT TOKEN HERE'
chatids = {"581":"@vaccineFinderHyderabad18","571":"@vaccineFinderChennai18","305":"-1001176270354","265":"@vaccineFinderBangalore18"}
districts = ["581","571","305","265"]
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Ch$ko) Chrome/90.0.4430.93 Safari/537.36"}
for dist in districts:
    PARAMS = {'district_id':dist,'date':today}
    respone = requests.get(url, params = PARAMS, headers = headers)
    responseData = respone.json()
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
                noofslots = str(session["available_capacity"])
                link = '<a href="https://selfregistration.cowin.gov.in/"><b><i>Click to Register</i></b></a>'
                googlemap = 'https://www.google.com/maps/search/?api=1&query='+urllib.parse.quote_plus(centerAddress)
                #message = "Hi, I Found a Slot for "+stateName+",\n Available Date: "+availableDate+",\n No. of Slots Available: "+noofslots+",\n Vaccine Type: "+ vaccineType+",\n Center Name: "+centerName+",\n Center Address: "+ centerAddress
                count = count+1
                botemoji = u'\U0001F916' 
                linkemoji = u'\U0001F517'
                mess = botemoji+' Hi, I Found a Slot\n\n<b>Available Date: </b>'+availableDate+'\n<b>No. of Slots Available: </b>'+noofslots+'\n<b>Vaccine Type: </b>'+vaccineType+'\n<b>Center Name: </b>'+centerName+'\n<b>Center Address: </b>'+ centerAddress+'\n\n'+linkemoji+ link+'\n\n'+googlemap
                if count == 1:
                    print("Message is:"+mess)
                    bot = telegram.Bot(token=my_token)
                    bot.sendMessage(chat_id=chatids[dist], text=mess, parse_mode=ParseMode.HTML)
                    
