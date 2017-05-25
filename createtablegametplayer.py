import psycopg2
import networkhelper
conn = networkhelper.dbconnect("host='ec2-54-243-52-211.compute-1.amazonaws.com' dbname='d4inae708paere' user='sdsduckhtwkkzl' password='s2YO_0haa9M-0PHuiT3q0D3a7w'")
cur = conn.cursor()

cur.execute("""CREATE TABLE game (
	game_id SERIAL PRIMARY KEY,
	datecreated timestamp)
	""")
cur.execute("""CREATE TABLE tplayer (
	tplayer_id SERIAL PRIMARY KEY,
	mu int,
	sigma int,
	team VARCHAR(4),
	game_id integer REFERENCES game )
	""")
conn.commit()
cur.close()
conn.close()