import sqlite3

conn = sqlite3.connect('bla.db')

c = conn.cursor()

c.execute('''CREATE TABLE trips 
		(trip_id text, modify_date integer, total_seats integer, seats_left integer, departure_date integer, price real) ''')

conn.commit()
conn.close()
