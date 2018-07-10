import sys, getopt
import requests
import json
import sqlite3
import datetime
import time
import os

API_URL = 'https://public-api.blablacar.com/api/v2/trips'
DB_PATH = os.path.join(os.path.dirname(__file__), 'bla.db')

def getTripsData(apiKey, fromName, toName, dateBegin = None):
	headers = {'accept': 'application/json', 'key': apiKey}	
	params = {'fields': 'trips,seats,seats_left,departure_date,permanent_id,price', 'locale': 'en_GB', 'cur': 'EUR', 'fn': fromName, 'tn': toName}

	if dateBegin:
		params["db"] = str(dateBegin)

	r = requests.get(API_URL, params=params, headers=headers)

	try:
		data  = r.json()
	except ValueError as err:
		print str(err)
		sys.exit(2)

	return data["trips"]

def storeDataToSql(cityFrom, cityTo, trips):
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
# search_city_from text, search_city_to text, trip_id text, modify_date integer, total_seats integer, seats_left integer, departure_date integer, price real
	for trip in trips:
		departureDate = int(time.mktime(datetime.datetime.strptime(trip["departure_date"], "%d/%m/%Y %H:%M:%S").timetuple()))
		data = (cityFrom, cityTo, trip["permanent_id"], int(time.time()), trip["seats"], trip["seats_left"], departureDate, trip["price"]["value"])
  		c.execute('insert into trips values (?,?,?,?,?,?,?,?)', data)

	conn.commit()
	conn.close()

def main(argv):
	apiKey = ''
	fromName = ''
	toName = ''

	dateBegin = time.strftime("%Y-%m-%d") 
	try:
		opts, args = getopt.getopt(argv, "d:")
		if len(args) < 3:
			raise ValueError('Please, specify blabla car ApiKey,  city-from-name and city-to-name')

		apiKey = args[0]
		fromName = args[1]
		toName = args[2]
	except getopt.GetoptError as err:
		print str(err)
		sys.exit(2)
	except ValueError as err:
		print str(err)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-d':
			dateBegin = arg
	tripsData = getTripsData(apiKey, fromName, toName, dateBegin)	
	storeDataToSql(fromName, toName, tripsData)
	print time.strftime("%Y-%m-%d %H:%M:%S -"), 'added %d entries' % len(tripsData), 'from %s to %s' % (fromName, toName)
main(sys.argv[1:])
