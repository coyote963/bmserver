from collections import deque
from matchupdb import read_and_write
from databaseaccesslayer import find_player, player_rating, add_player, matchupdate

def request_balance(packet,socket, **kwargs):
	if packet['option'] == "Chat":
		if "!balance" in packet['content']:
			conn = kwargs['dbcursor']
			bmstream = kwargs['bms']

			packet['content'] = "has joined"
			is_balanced(packet,socket,**kwargs)
def is_balanced(packet, socket, **kwargs):
	if packet['option'] == "Chat":
		if "has joined" in packet['content']:
			conn = kwargs['dbcursor']
			bmstream = kwargs['bms']

			print "someone has joined"
			cur = conn.cursor()
			uscteamroster  = deque()
			manteamroster = deque()
			uscteamratings = []
			manteamratings = []
			
			socket.send('/scoreboard\n')
			bmstream.read()
			manaverage = 0
			uscaverage = 0
			while bmstream.isEmpty():
				bmdict = bmstream.pop()
				if bmdict['option'] == "Scoreboard" :
					print bmdict
					if bmdict['team'] == '1':
						uscteamroster.append(bmdict['name'])
					elif bmdict['team'] == '2':
						manteamroster.append(bmdict['name'])
			
			uscteamsize = len(uscteamroster)
	
			if uscteamsize > 0:
				while uscteamroster:
					message = '/steam '+ uscteamroster.pop() + '\n'
					socket.send(bytes(message))
					bmstream.read()
					steamdict =  bmstream.pop()
					if steamdict['option'] != 'Steam ID':
						uscaverage = uscaverage + 1000
					else:
						uscaverage = uscaverage + player_rating(find_player(steamdict['player'],steamdict['steamid'], cur), cur)
				uscaverage = uscaverage/uscteamsize
				
			manteamsize = len(manteamroster)
			if manteamsize > 0:
				while manteamroster:
					message = '/steam '+ manteamroster.pop() + '\n'
					socket.send(bytes(message))
					bmstream.read()
					steamdict =  bmstream.pop()
					if steamdict['option'] != 'Steam ID':
						manaverage = manaverage + 1000
					else:
						manaverage = manaverage + player_rating(find_player(steamdict['player'],steamdict['steamid'], cur), cur)
				manaverage = manaverage/manteamsize
				
			if abs(manaverage - uscaverage) > 75:
				socket.send(bytes("Teams are very unbalanced\n"))
				r1 = 10**(float(manaverage)/400)
				r2 = 10**(float(uscaverage)/400)
				e1 = r1 / (r1 + r2)
				e2 = r2 / (r1 + r2)
				socket.send(bytes("Man" + str(int(e1* 100))+ "% USC "+ str(int(e2 * 100)) + '%\n'))
				
			socket.send(bytes("man "+ str( int(manaverage)) + " usc " + str(int(uscaverage))+ '\n'))