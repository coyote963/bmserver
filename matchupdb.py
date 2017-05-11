from datetime import datetime
from databaseaccesslayer import find_player,add_player, matchupdate, most_recent_steam,player_rating, apply_elo, apply_floor, enforce_floor,update_activity
import winsound

#deprecated. Do not use under any circumstances. Favors data loss.
def read_and_write(string,comparator,bmstream, socket):
	while True:
		print string
		socket.send(bytes(string))
		bmstream.read()
		try:	
			print bmstream.isEmpty()
			while bmstream.isEmpty():
				bmdict = bmstream.pop()
				if bmdict['option'] == comparator:
					return bmdict
				else: 
					print bmdict
		except KeyboardInterrupt:
			print "was in read and write phase"

#deprecated. Its too annoying
def is_running(packet, socket, **kwargs):
	if packet['option'] == 'Chat':
		if "commandlist" in packet['content']:
			socket.send(bytes("translate,traducir,rating,topten,balance,coyote\n"))
def coyote(packet,socket,**kwargs):
	if packet['option'] == 'Chat' and '!coyote' in packet['content']:
		Freq = 392 # Set Frequency To 2500 Hertz
		Dur = 333 # Set Duration To 1000 ms == 1 second
		winsound.Beep(Freq,Dur)
		socket.send('coyote notified\n')
def matchupdb(packet, socket, **kwargs):
	if packet['option'] == 'Killfeed':		
		conn = kwargs['dbcursor']
		bmstream = kwargs['bms']

		cur = conn.cursor()
		dt = datetime.now()

		socket.send(bytes('/steam '+packet['victim']+'\n'))
		bmstream.read()
		victimdict = bmstream.pop()

		socket.send(bytes('/steam '+packet['killer']+'\n'))
		bmstream.read()
		killerdict = bmstream.pop()
		
		victimid = locate_player(victimdict,dt,cur)
		killerid = locate_player(killerdict,dt,cur)
		newrating = apply_elo(victimid, killerid, cur)
		try:	
			matchupdate(newrating[0],newrating[1], 
				victimdict['player'], killerdict['player'],
				victimid, killerid,
				packet['cause'], cur)
		except KeyError:
			return
		apply_floor(victimid, cur)
		enforce_floor(victimid, cur)
		update_activity(victimid,cur)
		apply_floor(killerid, cur)
		update_activity(killerid,cur)
		conn.commit()
#locates the player, and returns his id. If this is a new player, add the new player's ID.
def locate_player(steamdict,dt, cur):
	try:
		#attempt to access the player naive
		playerid = find_player(steamdict['player'], steamdict['steamid'], cur) 
	except KeyError:
		#mismatch occurred. The packet accessed was not a player, occurs when there is a game kill.
		print "mismatch"
		return
	if playerid is None:
		#there is no row existing that has this. We need to add one row.
		#if the player is not using steam
		if steamdict['steamid'] == '-1':
			playerid = add_player(steamdict['player'], steamdict['steamid'], dt, cur)[0]
		else:
			#get the most recently played steam
			player_id = most_recent_steam(steamdict['steamid'], cur)
			if not player_id:
				#this is the first time on server, therefore no most recent steam
				playerid = add_player(steamdict['player'], steamdict['steamid'], dt, cur)[0]
			else:
				#this is not first time on server. add a new row from the most recent steam
				playerid = add_player(steamdict['player'], steamdict['steamid'], dt, cur, player_rating(player_id, cur))
	return playerid
