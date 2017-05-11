playertable = ""
matchuptable = ""
ipaddress = ""
port = 0
def initiate():
	global playertable
	global matchuptable
	global ipaddress
	global port
	filename = raw_input('Enter a filename: ') or 'config.txt'
	with open(filename) as configfile:
		configs = configfile.readlines()
		playertable = configs[0][:-1]
		matchuptable = configs[1][:-1]
		ipaddress = configs[2][:-1]
		port = int(configs[3])
def instantinitiate(inputplayertable, inputmatchuptable, inputipaddress, inputport):
	global playertable
	global matchuptable
	global ipaddress
	global port
	playertable = inputplayertable
	matchuptable = inputmatchuptable
	ipaddress = inputipaddress
	port = int(inputport)