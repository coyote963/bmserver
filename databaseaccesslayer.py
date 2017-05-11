from datetime import datetime
import config
#takes a name and a steamid and returns a player_id
def find_player(name, steamid, cur):
	query = """SELECT player_id FROM {}
		WHERE ingamename = (%s) AND steamid = (%s);""".format(config.playertable)
	cur.execute(
		query,
		(name, str(steamid))
	)
	return cur.fetchone()

def top_player(cur):
	query = """SELECT ingamename,rating
				FROM {}
				WHERE active = True
				ORDER BY rating DESC LIMIT 10;""".format(config.playertable)
	cur.execute(query)
	return cur.fetchall()
#returns the rating given a playerid
def player_rating(playerid, cur):
	query = """SELECT rating FROM {} 
		WHERE player_id = (%s);""".format(config.playertable)
	cur.execute(
		query,
		(playerid,)
	)
	try:
		rating = cur.fetchone()[0]
		return rating
	except TypeError:
		return 1000

#returns the rating given a playerid
def player_floor(playerid, cur):
	query = """SELECT ratingfloor FROM {} 
		WHERE player_id = (%s);""".format(config.playertable)
	cur.execute(
		query,
		(playerid,)
	)
	try:
		rating = cur.fetchone()[0]
		return rating
	except TypeError:
		return 1000

#adds a player to the player database table
def add_player(name, steamid,date,cur,rating = 1000, ratingfloor = 750, timesplayed = 1):
	query = """INSERT INTO {} (ingamename, steamid, rating, datecreated, ratingfloor,lastplayed, timesplayed,active)
			VALUES(%s, %s, %s, %s, %s, %s, %s, %s);""".format(config.playertable)
	cur.execute(
		query,
		(name, steamid, rating, date,ratingfloor,date, timesplayed,True)
		)
	return find_player(name, str(steamid), cur)

#given two ids, uses the elo function to adjust ratings
def apply_elo(victimid, killerid, cur):
	victim_rating = player_rating(victimid, cur)
	print "victim " + str(victim_rating)
	
	killer_rating = player_rating(killerid, cur)
	print "killer" + str(killer_rating)
	victimnewrating = elo(victim_rating, killer_rating)[0]
	killernewrating = elo(victim_rating, killer_rating)[1]
	dt = datetime.now()
	query = """
		UPDATE {} SET rating = (%s), lastplayed = (%s)
		WHERE player_id = (%s);""".format(config.playertable)
	cur.execute(
		query,
		(victimnewrating, dt, victimid))
	cur.execute(
		query,
		(killernewrating, dt, killerid))
	return [victimnewrating, killernewrating]

#inserts a new matchup entry in the matchup table
def matchupdate(victimrating, killerrating, victimname, killername, victimid, killerid, weaponused, cur):
	query = """INSERT INTO {} (weapon, victimrating, killerrating,victim_name, killer_name, victim_id, killer_id,dateoccurred)
			VALUES(%s, %s, %s, %s,%s, %s, %s, %s);""".format(config.matchuptable)
	print query
	cur.execute(
		query,
		(weaponused, victimrating, killerrating, victimname, killername, victimid, killerid, datetime.now())
	)
def update_activity(playerid,cur):
	query = """
		UPDATE {}
		SET lastplayed = (%s)
		WHERE player_id = (%s);
		""".format(config.playertable)
	cur.execute(
		query, (datetime.now(), playerid))
def apply_floor(playerid, cur):
	query = """
		SELECT timesplayed
		FROM {}
		WHERE player_id = (%s);
		""".format(config.playertable)
	cur.execute(
		query, (playerid,))

	numplays = cur.fetchone()
	if numplays[0] is not None:
		query = """
			UPDATE {}
			SET timesplayed = (%s)
			WHERE player_id = (%s);""".format(config.playertable)
		cur.execute(
			query,
			(numplays[0]+1,playerid))
		if numplays[0] % 75 == 0:
			print "UPDATING TIME"
			query = """
				SELECT killerrating
				FROM {}
				WHERE killer_id = (%s)
				ORDER BY dateoccurred DESC LIMIT 75;
				""".format(config.matchuptable)
			cur.execute(
				query,(playerid,))
			ratinghistory = cur.fetchall()
			total = 0
			for rating in ratinghistory:
				total = total + rating[0]
			newfloor = total/len(ratinghistory)
			query = """
				UPDATE {}
				SET ratingfloor = (%s) 
				WHERE player_id = (%s);
				""".format(config.playertable)
			cur.execute(
				query,(newfloor-100, playerid))
			print "updated floor"
	else:
		query = """
			UPDATE {}
			SET timesplayed = (%s)
			WHERE player_id = (%s);""".format(config.playertable)
		cur.execute(
			query,
			(1,playerid))
def enforce_floor(playerid, cur):
	query = """
		SELECT rating, ratingfloor
		FROM {}
		WHERE player_id = (%s);""".format(config.playertable)
	cur.execute(
		query, (playerid,))
	comp = cur.fetchone()
	if comp[0] < comp[1]:
		query = """
			UPDATE {}
			SET rating = (%s)
			WHERE player_id = (%s);
			""".format(config.playertable)
		cur.execute(
			query,(comp[1],playerid))



#function that gets the latest steam given a steamid
def most_recent_steam(steamid, cur):
	if steamid != -1: #not an anonymous player
		query = """SELECT player_id 
			FROM {}
			WHERE steamid = (%s)
			ORDER BY lastplayed DESC LIMIT 1;""".format(config.playertable)
		cur.execute(
			query,
			(str(steamid),))
		return cur.fetchone()
		
#Elo rating adjustment
def elo(victimrating,killerrating):
	r1 = 10**(float(victimrating)/400)
	r2 = 10**(float(killerrating)/400)
	e1 = r1 / (r1 + r2)
	e2 = r2 / (r1 + r2)
	print e1
	print e2
	r1 = victimrating - 16*e1
	r2 = killerrating + 16*(1 - e2)
	return [r1,r2]
