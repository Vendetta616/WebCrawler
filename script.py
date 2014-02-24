#coding : utf-8

def doscript():
	import crawler
	__doscript__crawler = crawler.crawler("searchindex.db")
	__doscript__crawler.createindextables()
	pages = ["http://en.wikipedia.org/wiki/Vincent_van_Gogh"]
	crawler.crawl(pages)

def search():
	import crawler
	__search__clawler = crawler.searcher("searchindex.db")
	__search__clawler.query("functional programming")


def calc():
	import crawler
	__doscript__crawler = crawler.crawler("searchindex.db")
	__doscript__crawler.calculatepagerank()

def nn():
	import nn
	mynet = nn.searchnet("nn.db")
	mynet.maketables()
	wWorld,wRiver,wBank = 101,102,103
	uWorldBank,uRiver,uEarth = 201,202,203
	mynet.generatehiddennode([wWorld,wBank],[uWorldBank,uRiver,uEarth])

	for c in mynet.con.execute("select * from wordhidden"):
		print(c)

	for c in mynet.con.execute("select * from hiddenurl"):
		print(c)

def nn2():
	import nn

	wWorld,wRiver,wBank = 101,102,103
	uWorldBank,uRiver,uEarth = 201,202,203
	mynet = nn.searchnet("nn.db")
	print(mynet.getresult([wWorld,wBank],[uWorldBank,uRiver,uEarth]))

def dtanh(y):
	return 1.0-y*y

def backpropagate(self,targets,N=0.5):
	#calculate error of output
	output_deltas = [0.0] *len(self.urlids)
	for k in range(len(self.urlids)):
		error = targets[k]-self.ao[k]
		output_deltas[k] = dtanh(self.ao[k])*error

	#calculate error of hiddenlayer
	hidden_deltas = [0.0] * len(self.hiddenids)
	for j in range(len(self.hiddenids)):
		error = 0.0
		for k in range(len(self.urlids)):
			error = error + output_deltas[k]*self.wo[j][k]
		hidden_deltas[j] = dtanh(self.ah[j])*error

	#calculate weight of output
	for j in range(len(self.hiddenids)):
		for k in range(len(self.urlids)):
			change = output_deltas[k]*self.ah[j]
			self.wo[j][k] = self.wo[j][k] + N*change

	#Update weight of input
	for i in range(len(self.wordids)):
		for j in range(len(self.hiddenids)):
			change = hidden_deltas[j]*self.ai[i]
			self.wi[i][j] = self[i][j]+N*change

def __init__(self):
	doscript()
