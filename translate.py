from mtranslate import translate
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def trans(packet, socket, **kwargs):
	if packet['option'] == 'Chat':
		if '!translate' in packet['content']:
			translate_from = re.split('!translate', packet['content'])[1]
			translate_to = translate(translate_from, 'en')
			socket.send(translate_to+'\n')
		if '!traducir' in packet['content']:
			translate_from = re.split('!traducir', packet['content'])[1]
			translate_to = translate(translate_from, 'es')
			socket.send(str(translate_to)+'\n')