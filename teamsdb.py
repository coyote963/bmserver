from databaseaccesslayer import *
import psycopg2.extras
from trueskill import Rating,rate
class Team:
	def __init__(self):
		self.teamlist = {}
		self.hits = 0
   	def incrementSeen(self, packet):
   		if not self.existingUser(packet):
   			self.addUser(packet)
   		else:
   			if packet['team'] == '1':
   				self.teamlist[packet['name']][1] += 1
   			if packet['team'] == '2':
   				self.teamlist[packet['name']][0] += 1
   	def incrementHits(self):
   		self.hits += 1;
   	def addUser(self, packet):
   		if packet['team'] == '1':
   			self.teamlist[packet['name']] = [1,0]
   		if packet['team'] == '2':
   			self.teamlist[packet['name']] = [0,1]
   	def existingUser(self, packet):
   		return packet['name'] in self.teamlist 
   	def clearTeamList(self):
   		self.teamlist.clear()
   		self.hits = 0
   	def logTeam(self):
   		file_object = open("logging.txt", "w")
   		stringbuilder = ""
   		for playername in self.teamlist:
   			stringbuilder += playername + str(self.teamlist[playername][0]) + str(self.teamlist[playername][1])
   		file_object.write(stringbuilder)
   		file_object.close
   	def printTeam(self):
   		print "printing list"
   		for playername in self.teamlist:
   			print playername + str(self.teamlist[playername])
   	def returnEntry(self, name):
   		return self.teamlist[name]

def infoIncrement(packet,socket, **kwargs):
	if packet['option'] == 'Info':
		kwargs['teamlist'].incrementHits()

def teamsdb(packet, socket, **kwargs):
	if packet['option'] == 'Scoreboard':
		kwargs['teamlist'].incrementSeen(packet)


def clearTeam(packet, socket, **kwargs):
	if packet['option'] == 'Match End':
		print "!!!!!!!!!!!!!!!!!"
		
		manid = uscid  = []
		uscplayer = manplayer  = manweight = uscweight = ()
		conn = kwargs['dbcursor']
		dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		createMatch(packet['winner'],dict_cur)
		conn.commit()
		game_id = latestMatch(dict_cur)['game_id']
		team = kwargs['teamlist'].teamlist
		for playername in team:
			pdict = getDictName(playername,dict_cur)
			if pdict is not None:
				if mainteam(team[playername]) == 'man':
					manplayer = manplayer + (Rating(pdict['mu'],pdict['sigma']),)
					manweight = manweight + (measureweight(
						team[playername],
						kwargs['teamlist'].hits),)
					manid.append(pdict['player_id'])
				else:
					uscplayer = uscplayer + (Rating(pdict['mu'],pdict['sigma']),)
					uscweight = uscweight + (measureweight(
						team[playername],
						kwargs['teamlist'].hits),)
					uscid.append(pdict['player_id'])
		import pdb; pdb.set_trace()
		if packet['winner'] == 'man':
			myranks=[0,1]
		if packet['winner'] == 'usc':
			myranks = [1,0]
		else:
			myranks = [0,0]

		newmanteam, newuscteam = rate([manplayer,uscplayer], ranks = myranks, weights = [manweight,uscweight])
		recordTeamStats(newmanteam , manid, game_id, dict_cur, currentteam = "man")
		recordTeamStats(newuscteam , uscid, game_id,dict_cur,currentteam = "usc")
		kwargs['teamlist'].clearTeamList()
		conn.commit()
		
def mainteam(frequencylist):
	if frequencylist[0] > frequencylist[1]:
		return 'man'
	else:
		return 'usc'
def measureweight(teamtimes, total):
	return (teamtimes[0] + teamtimes[1])*(1.0 - min(teamtimes)/ float(max(teamtimes))) / float(total)

def recordTeamStats(team, teamid, game_id, dict_cur,currentteam):
	for newplayer, playerid in zip(team,teamid):
		updateMu(newplayer.mu, newplayer.sigma,
			playerid, dict_cur)
		insert_tplayer(newplayer.mu, newplayer.sigma, 
			currentteam,
			 playerid , game_id,
			dict_cur)

