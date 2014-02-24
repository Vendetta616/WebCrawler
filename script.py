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



def __init__(self):
	doscript()
