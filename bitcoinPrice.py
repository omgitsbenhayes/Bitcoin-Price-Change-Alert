import sys
import os
import re
import urllib
import json
import smtplib
from email.MIMEText import MIMEText


# Get bitcoin price from Bitcoinity.org
page = urllib.urlopen('http://bitcoinity.org/markets')
data = page.read()
beginloc = data.find("<span id='last_buy'>")
startloc = beginloc + 20
endloc = startloc + 6
price = data[startloc:endloc]

#Get bitcoin price from BTC-e.com Web API
#data = urllib.urlopen('https://btc-e.com/api/2/btc_usd/ticker')
#j = json.load(data)
#price = j["ticker"]["last"]

#Open file and read in previous price
prevPriceFile = open('', 'r') #open file to get previous price
prevPrice = prevPriceFile.readline() #read in first line (previous price)
prevPriceFile.close()

#Handle variable types, prepare for evaluation
price = float(price)
prevPrice = float(prevPrice)
sendPrice = False
diffPrice = price - prevPrice

#Check previous price for significant change
if price > (prevPrice + 25.00):
	sendPrice = True
elif price < (prevPrice - 25.00):
	sendPrice = True
else:
	#print "Price has not changed by $4.25 or more"
	sys.exit()


#Write new price to file
def writePrice(b):
	a = str(b)
	prevPriceFileWrite = open('', 'w')
	prevPriceFileWrite.write(a)
	prevPriceFileWrite.close()
	
#Send price
def sendMessage():
	#! /usr/local/bin/python
	SMTPserver = ''
	sender =     ''
	destination = ['']
	USERNAME = ""
	PASSWORD = ""
	text_subtype = 'plain'
	subject = ""
	content = 'BTC Price Alert: $%s (%s)' % (str(price), str(diffPrice))
	content = content.rstrip()

	try:
    		msg = MIMEText(content, text_subtype)
    		msg['Subject'] = subject
	    	msg['From'] = sender

		conn = smtplib.SMTP(SMTPserver, 587)
		conn.set_debuglevel(False)
		conn.login(USERNAME, PASSWORD)
		
		try:
        		conn.sendmail(sender, destination, msg.as_string())
			#print "message sent"
    		finally:
        		conn.close()

	except Exception, exc:
    		sys.exit( "Failed to deliver message; %s" % str(exc) ) # give an error message

if sendPrice:
	writePrice(price)
	sendMessage()
