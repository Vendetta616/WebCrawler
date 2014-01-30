#coding : utf-8

def doscript():
	import crawler
	crawler = crawler.crawler("searchindex.db")
	crawler.createindextables()
	pages = ["http://en.wikipedia.org/wiki/Vincent_van_Gogh"]
	crawler.crawl(pages)

def __init__(self):
	doscript()
