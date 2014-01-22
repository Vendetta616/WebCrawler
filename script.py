
def doscript():
	import crawler
	crawler = crawler.crawler("searchindex.db")
	crawler.createindextables()
