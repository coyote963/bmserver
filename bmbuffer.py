import re
from collections import deque

infotypes = {1:"Chat", 2:"Match End", 3:"Scoreboard", 4:"Info", 5:"Vote", 6:"Killfeed", \
             7:"Steam ID", 8:"ID"}
gamemodes = {1:"CTF",2:"DM",3:"CLB",4:"ZMB",5:"TDM",6:"WD",7:"SVL",8:"TO"}
voteinfotypes = {0:"Change Map", 1:"Ban Player"}

def chatiter(index):
	return index + 3
def matchiter(index):
	return index + 3
def scoreboarditer(index):
	return index + 7
def infoiter(index):
	return index + 8
def voteiter(index):
	return index + 3
def killiter(index):
	return index + 4
def steamiter(index):
	return index + 3
def iditer(index):
	return index + 3


def infotype(identifier):
	return infotypes[int(identifier)]
def voteinfotype(identifier):
	return voteinfotypes[int(identifier)]
def gamemode(identifier):
	return gamemodes[int(identifier)]
def blocksplit(block):

	i = 0
	blockq = deque()
	blocklist = re.split('\n', block)
	print blocklist
	while i < len(blocklist)-1:
		if infotype(blocklist[i]) == "Chat":
			blockq.append({
				'option':infotype(blocklist[i]),
				'content':blocklist[i+1],
				'name':re.split(': ',blocklist[i+1])[0],
				'infotype':int(blocklist[i+2])
			})
			i = chatiter(i)
		
		elif infotype(blocklist[i]) == "Match End":
			blockq.append({
				'option':infotype(blocklist[i]),
				'winner':blocklist[i+1],
				'next_map':blocklist[i+2]
				 })
			i = matchiter(i)
		
		elif infotype(blocklist[i]) == "Scoreboard":
			blockq.append({
				'option':infotype(blocklist[i]),
				'gamemode': gamemode(blocklist[i+1]), 
				'team':blocklist[i+2], 
				'name':blocklist[i+3], 
				'kills':blocklist[i+4], 
				'deaths':blocklist[i+5]
				})
			i = scoreboarditer(i)
		
		elif infotype(blocklist[i]) == "Info":
			blockq.append({
				'option':infotype(blocklist[i]),
				'server_name' : blocklist[i+1], 
				'connected' : int(blocklist[i+2]), 
				'capacity' : int(blocklist[i+3]), 
				'gamemode' : blocklist[i+4], 
				'mapname' :blocklist[i+5], 
				'minutes' : blocklist[i+6], 
				'seconds' : blocklist[i+7]
				})
			i =infoiter(i)
		
		elif infotype(blocklist[i]) == "Vote":
			if voteinfotype(blocklist[i+2]) == "Change Map":
				blockq.append({
					'option': infotype(blocklist[i]),
					'map' : blocklist[i+1]})
			else:
				blockq.append({
					'option':infotype(blocklist[i]),
					'player':blocklist[i+1]
					})
			i = voteiter(i)
		
		elif infotype(blocklist[i]) == "Killfeed":

			blockq.append({
				'option' : infotype(blocklist[i]),
				'killer' : blocklist[i+1],
				'victim' : blocklist[i+2], 
				'cause' : blocklist[i+3]
				})
			i = killiter(i)
		elif infotype(blocklist[i]) == "ID":
			blockq.append({
				'option' : infotype(blocklist[i]),
				'id' : int(blocklist[i+1]), 
				'player' : blocklist[i+2]
				})
			i = iditer(i)


		elif infotype(blocklist[i]) == "Steam ID":
			try: 
				blockq.append({
					'option' :infotype(blocklist[i]),
					'steamid' : int(blocklist[i+1]), 
					'player' : blocklist[i+2]
					})
			except:
				blockq.append({
					'option' :infotype(blocklist[i]),
					'steamid' : -1,
					'player' : blocklist[i+2]
					})
			i = steamiter(i)

	return blockq
