from matchupdb import most_recent_steam
from databaseaccesslayer import player_rating,player_floor, find_player
import re
#Displays the player's rating when !rating is typed into chat
def request_rating(packet, socket, **kwargs):
	if (packet['option'] == 'Chat'):
		if ": !rating" in packet['content']:
			conn = kwargs['dbcursor']
			bmstream = kwargs['bms']
			cur = conn.cursor()
			socket.send('/steam '+packet['name'] +'\n')
			bmstream.read()
			playerdict = bmstream.pop()
			if playerdict['option'] != "Steam ID":
				return 
			print playerdict
			if playerdict['steamid'] == -1:
				playerid = find_player(packet['name'], playerdict['steamid'],cur)
			else:
				playerid = most_recent_steam( playerdict['steamid'], cur)
			rating = player_rating(playerid, cur)
			floor = player_floor(playerid, cur)

			if rating and floor:
				print rating
				socket.send(bytes(packet['name'] + ': ' + str(rating) +' floor: ' +str(floor) + '\n'))
				if playerid:
					socket.send(bytes("Your rank: "+ getrank(floor+150).upper()+" see more @ bmladder.com\n"))

def getrank(rating):
	if rating > 1450:
		return "god_slayer"
	elif rating > 1400:
		return "elite"
	elif rating > 1350:
		return "platinum"
	elif rating > 1275:
		return "diamond"
	elif rating > 1200:
		return "gold"
	elif rating > 1100:
		return "silver"
	elif rating > 1000:
		return "bronze"
	else:
		return "stone" 