import psycopg2
from datetime import datetime
conn=psycopg2.connect("host='ec2-50-17-212-238.compute-1.amazonaws.com' dbname='d4iqpn1cgf40o0' user='kempajfufvpvkk' password='xg8y1RVgUfLdnqeBmzsbi6aPc6'")

cur = conn.cursor()

cur.execute("""SELECT killer_name FROM matchup
	WHERE WEAPON = 'SNIPER RIFLE'"""	)
playerlist = cur.fetchall()
print len(playerlist)
conn.commit()
cur.close()
conn.close()