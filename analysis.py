import re
import json
from urllib.parse import parse_qs

def true_startswith(string, query):
	patt = re.compile("\[CQ:.*?\]")
	text = re.sub( patt,'', string ).lstrip()
	return text.startswith(query)

class Message( str ):
	def __init__(self,message):
		super(str,self).__init__()
		patt = re.compile("\[CQ:.*?\]")
		self.text = re.sub( patt,'', message ).lstrip()
		cqs = re.findall( r'\[CQ:(.*?),(.*?)\]', message )
		cqs_text = re.findall( r'(\[CQ:.*?,.*?\])', message )
		self.cqs = list()
		for cq,cq_text in zip(cqs,cqs_text):
			tmpcq = CQ()
			tmpcq.type = cq[0]
			tmpcq.content = parse_qs( cq[1], separator=',' )
			tmpcq.raw = cq_text
			self.cqs.append( tmpcq )

class CQ:
	def __init__(self):
		self.type=''
		self.content=''
		self.raw=''


# m = '/+bga [CQ:at,qq=937404959] zyyzxyz'
# m = Message(m)
# print(m.cqs[0].type)
# print(m.cqs[0].content)
# print(m.cqs[0].raw)
