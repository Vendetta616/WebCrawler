import urllib2
from BeautifulSoup import *
from urlparse import urljoin

ignorewrods = set(["the","of","to","and","a","in","is","it"])


class crawler:

	#init class as database name
	def __init__(self,dbname):
		pass

	def __del__(self):
		pass

	def dbcommit(self):
		pass

	#Supporting method that getting entry ID or adding if its not exists 
	def getentryid(self,table,field,value,createnew=True):
		return None

	#indexing each pages
	def addtoindex(self,url,soup):
		print("indexing ",url)

	#Extraction text from HTML which has not tags
	def gettextonly(self,soup):
		return ""

	#separate words except white space
	def saparatewords(self,text):
		return None

	#retrun True if URLs is indexed 
	def isindexed(self,rul):
		return False

	#adding links between 2 pages
	def addlinkref(self,urlFrom,urlTo,linkText):
		pass

	#accept pagelist,and crawling at giving depth by breadth first search
	#then indexing pages
	def crawl(self,pages,depth=2):
		for i in range(depth):
			newpages=set()
			for page in pages:
				try:
					c = urllib2.urlopen(page)
				except:
					print("could not open ",page)
					continue
				soup = BeautifulSoup(c.read())
				self.addtoindex(page,soup)

			links = soup('a')
			for link in links:
				if("href" in dict(link.attrs)):
					url = urljoin(page,link["href"])
					if url.find("'")!=-1:continue
					url = url.split("#")[0] #removing ankor
					if url[0:4] == "http" and not self.isindexed(url):
						newpages.add(url)
					linkText=self.gettextonly(link)
					self.addlinkref(page,url,linkText)

				self.dbcommit()
			pages = newpages

	#creating database table
	def createindextables(self):
		pass
