import networkhelper
conn = networkhelper.dbconnect("host='ec2-54-243-52-211.compute-1.amazonaws.com' dbname='d4inae708paere' user='sdsduckhtwkkzl' password='s2YO_0haa9M-0PHuiT3q0D3a7w'")
from databaseaccesslayer import most_recent_steam
cur = conn.cursor()
cur.execute("""
	UPDATE player
	SET primaryaccount = False
	""")
cur.execute("""
	SELECT DISTINCT steamid FROM player""")
steamlist = cur.fetchall()
progress = 0

#function that gets the latest steam given a steamid
def most_recent_steam(steamid, cur):
	if steamid != -1: #not an anonymous player
		query = """SELECT player_id 
			FROM player
			WHERE steamid = (%s)
			ORDER BY lastplayed DESC LIMIT 1;"""
		cur.execute(
			query,
			(steamid,))
		return cur.fetchone()

for i in steamlist:
	print str(i[0])
	progress = progress + 1
	print str(progress) + " of " + str(len(steamlist))
	x = most_recent_steam(i[0], cur)
	cur.execute("""
		UPDATE player
		SET primaryaccount = True
		WHERE player_id = (%s);""", x)

conn.commit()
cur.close()
conn.close()