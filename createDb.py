import sqlite3

conn = sqlite3.connect('bla.db')

c = conn.cursor()

c.execute('''CREATE TABLE trips 
		(search_city_from text, search_city_to text, trip_id text, modify_date integer, total_seats integer, seats_left integer, departure_date integer, price real) ''')

conn.commit()
conn.close()
