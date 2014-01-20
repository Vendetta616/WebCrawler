
class crawler:

	depth = 2

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
		print("indexing %s",%url)

	#Extraction text from HTML which has not tags
	def gettextonly(self,soup):
		return None

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
	def cwawl(self,pages,depth):
		pass

	#creating database table
	def createindextables(self):
		pass
