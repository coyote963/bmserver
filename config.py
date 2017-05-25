playertable = ""
matchuptable = ""
ipaddress = ""
port = 0
def initiate():
	global playertable
	global matchuptable
	global ipaddress
	global port
	global database
	global password
	filename = raw_input('Enter a filename: ') or 'config.txt'
	with open(filename) as configfile:
		configs = configfile.readlines()
		playertable = configs[0][:-1]
		matchuptable = configs[1][:-1]
		ipaddress = configs[2][:-1]
		port = int(configs[3])
		password = configs[4][:-1]
		database = configs[5][:-1]
def instantinitiate(inputplayertable, inputmatchuptable, inputipaddress, inputport, databasecred):
	global playertable
	global matchuptable
	global ipaddress
	global port
	global database
	playertable = inputplayertable
	matchuptable = inputmatchuptable
	ipaddress = inputipaddress
	port = int(inputport)
	database = databasecred