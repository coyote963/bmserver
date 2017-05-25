import networkhelper
conn = networkhelper.dbconnect("host='ec2-54-243-52-211.compute-1.amazonaws.com' dbname='d4inae708paere' user='sdsduckhtwkkzl' password='s2YO_0haa9M-0PHuiT3q0D3a7w'")

cur = conn.cursor()
cur.execute("""
	UPDATE player
	SET mu = (%s), sigma = (%s)
	""",(25, 25.0/3))

conn.commit()
cur.close()
conn.close()