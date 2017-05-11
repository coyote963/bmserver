from databaseaccesslayer import top_player

def request_leaderboard(packet,socket, **kwargs):
	if packet['option'] == "Chat":
		if "!topten" in packet['content']:
			conn = kwargs['dbcursor']
			bmstream = kwargs['bms']
			print "leaderboard requested"
			playerlist = ""
			playerarray = top_player(conn.cursor())
			i = 1
			for  player, ranking in playerarray:
				playerlist = playerlist + str(i) + player + '=' + str(ranking) + ' '
				i = int(i) + 1
			socket.send(playerlist +'\n')