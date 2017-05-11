import psycopg2
from datetime import datetime
def matchupdb(packet, socket, **kwargs):
	if (packet['option'] == '6'):		
		cur = conn.cursor()
		cur.execute(
			"""INSERT INTO matchup (weapon, dateoccurred, victim_name, killer_name)
				VALUES (%s, %s);""",
			(packet['cause'],datetime.now(), packet['victim'], packet['killer'])
			