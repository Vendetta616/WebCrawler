#coding : utf-8

def doscript():
	import crawler
	crawler = crawler.crawler("searchindex.db")
	crawler.createindextables()
	pages = ["http://en.wikipedia.org/wiki/Perl"]
	crawler.crawl(pages)
