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
	e=__search__clawler.getmatchrows("Programming")

def __init__(self):
	doscript()
