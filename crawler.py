#!/usr/bin/env python
#coding: utf-8


import urllib.request
import sqlite3
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

ignorewrods = set(["the","of","to","and","a","in","is","it"])

class crawler:

	#init class as database name
	def __init__(self,dbname):
		self.con = sqlite3.connect(dbname)

	def __del__(self):
		self.con.close()

	def dbcommit(self):
		self.con.commit()

	#Supporting method that getting entry ID or adding if its not exists 
	def getentryid(self,table,field,value,createnew=True):

		cur = self.con.execute("SELECT rowid FROM {} WHERE {} = (?) ".format(table,field),(value,)) 
		res = cur.fetchone()

		if res == None:
			cur = self.con.execute("insert into {} ({}) values (?)".format(table,field) ,(value,))
			return cur.lastrowid
		else:
			return res[0]

	#indexing each pages
	def addtoindex(self,url,soup):
		if self.isindexed(url):return
		print ("Intexing "+url)

		#get indivisual words index
		text = self.gettextonly(soup)
		words = self.separatewords(text)

		#URL getting id
		urlid = self.getentryid("urllist","url",url)

		#each words and this url link
		for i in range(len(words)):
			word = words[i]
			if word in ignorewrods:continue
			wordid = self.getentryid("wordlist","word",word)
			self.con.execute("insert into wordlocation(urlid,wordid,location) values({},{},{})".format(urlid,wordid,i) )


	#Extraction text from HTML which has not tags
	def gettextonly(self,soup):
		v = soup.string
		if v==None:
			c=soup.contents
			resulttext=""
			for t in c:
				subtext=self.gettextonly(t)
				resulttext+=subtext+"¥n"
			return resulttext
		else:
			return v.strip()

	#separate words except white space
	def separatewords(self,text):
		splitter = re.compile("¥¥W*")
		return [s.lower() for s in splitter.split(text) if s!=""]

	#retrun True if URLs is indexed 
	def isindexed(self,url):
		u = self.con.execute("select rowid from urllist where url=(?)" , url).fetchone()
		if u!=None:
			#checking actually crawled URL
			v=self.con.execute("select * from wordlocation where urlid={}".format(u[0]) ).fetchone()
			if v!=None: return True
		return False


	#adding links between 2 pages
	def addlinkref(self,urlFrom,urlTo,linkText):
		words = self.separatewords(linkText)
		fromid = self.getentryid("urllist","url",urlFrom)
		toid = self.getentryid("urllist","url",urlTo)
		if fromid == toid : return
		cur = self.con.execute("insert into link(fromid,toid) values ({},{})".format(fromid,toid))
		linkid = cur.lastrowid
		for word in words:
			if word in ignorewrods: continue
			wordid = self.getentryid("wordlist","word",word)
			self.con.execute("insert into linkwords(linkid,wordid) values({},{})".format(linkid,wordid) )

	def calculatepagerank(self,iterations = 20):
		#delete current pagerank table
		self.con.execute("drop table if exists pagerank")
		self.con.execute("create table pagerank(urlid primary key,score)")

		#all urls initialize by 1
		self.con.execute("insert into pagerank select rowid, 1.0 from urllist")
		self.dbcommit()

		for i in range(iterations):
			print("Iteration {}".format(i))
			for (urlid,) in self.con.execute("select rowid from urllist"):
				pr = 0.15

				#roop all pages which linked this page
				for (linker,) in self.con.execute("select distinct fromid from link where toid = {}".format(urlid)):
					#get linker's pagerank
					linkingpr = self.con.execute("select score from pagerank where urlid = {}".format(linker)).fetchone()[0]
					#get total link from linker
					linkingcount = self.con.execute("select count(*) from link where fromid = {}".format(linker)).fetchone()[0]

					pr+=0.85*(linkingpr/linkingcount)

				self.con.execute("update pagerank set score ={} where urlid = {}".format(pr,urlid))

				self.dbcommit



	#accept pagelist,and crawling at giving depth by breadth first search
	#then indexing pages
	def crawl(self,pages,depth=2):
		for i in range(depth):
			newpages=set()
			for page in pages:
				try:
					response = urllib.request.urlopen(page)
				except:
					print("could not open ",page)
					continue
				soup = BeautifulSoup(response.read())
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

	def createindextables(self):
		self.con.execute("create table urllist(url)")
		self.con.execute("create table wordlist(word)")
		self.con.execute("create table wordlocation(urlid,wordid,location)")
		self.con.execute("create table link(fromid integer,toid integer)")
		self.con.execute("create table linkwords(wordid,linkid)")
		self.con.execute("create index wordidx on wordlist(word)")
		self.con.execute("create index urlidx on urllist(url)")
		self.con.execute("create index wordurlidx on wordlocation(wordid)")
		self.con.execute("create index urltoidx on link(toid)")
		self.con.execute("create index urlformidx on ()link(fromid)")
		self.dbcommit


class searcher:
	def __init__(self,dbname):
		self.con =sqlite3.connect(dbname)

	def __del__(self):
		self.con.close()

	def getmatchrows(self,q):
		#Strings to creating query
		fieldlist="w0.urlid"
		tablelist=""
		clauselist=""
		wordids=[]

		#separate words by white space
		words=q.split(' ')
		tablenumber = 0

		for word in words:
			wordrow = self.con.execute("select rowid from wordlist where word = (?) ",(word,)).fetchone()
			
			if wordrow != None:
				wordid = wordrow[0]
				wordids.append(wordid)
				if tablenumber >0:
					tablelist+=","
					clauselist+=" and "
					clauselist+="w{}.urlid=w{}.urlid and ".format(tablenumber-1,tablenumber)
				fieldlist+=",w{}.location ".format(tablenumber)
				tablelist+="wordlocation w{} ".format(tablenumber)
				clauselist+="w{}.wordid = {} ".format(tablenumber,wordid)
				tablenumber+=1

		#create query by separated words

		fullquery = "select {} from {} where {}".format(fieldlist,tablelist,clauselist)

		cur = self.con.execute(fullquery)
		rows = [row for row in cur]

		return rows,wordids

	def getscoredlist(self,rows,wordids):
		totalscores = dict([(row[0],0) for row in rows])

		#Scorering function here
		weights = [(1.0,self.frequencyscore(rows))]

		for(weight,scores) in weights:
			for url in totalscores:
				totalscores[url]+= weight*scores[url]

		return totalscores

	def geturlname(self,id):
		return self.con.execute("select url from urllist where rowid = (?)",(id,)).fetchone()[0]

	def query(self,q):
		rows,wordids = self.getmatchrows(q)
		scores = self.getscoredlist(rows,wordids)
		rankedscores = sorted([(score,url) for (url,score) in scores.items()],reverse = 1)
		for (score,urlid) in rankedscores[0:10]:
			print('{:f}:{}'.format(score,self.geturlname(urlid)))

	def normalizescores(self,scores,smallIsBetter=0):
		#avoiding error that devived by zero
		vsmall = 0.00001

		if smallIsBetter:
			ninscore = min(scores.values())
			return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) in scores.items()])

		else:
			maxscore=max(scores.values())
			if maxscore ==0:
				maxscore = vsmall
			return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])


	def frequencyscore(self,rows):
		counts = dict([(row[0],0) for row in rows])
		for row in rows:
			counts[row[0]]+=1
		return self.normalizescores(counts)

	def distancescore(self,rows):
		#if given only 1 word ,everyone wins!
		if len(rows[0]<=2): return dict([(row[0],0.1) for row in rows])

		#initialize dictionaly by big number
		mindistance = dict([(row[0],1000000) for row in rows])

		for row in rows:
			dist = sum([abs(row[i]-row[i-1])])
			if dist<mindistance[row[0]]:
				mindistance[row[0]] = dist

		return self.normalizescores(mindistance,smallIsBetter=1)

	def inboundlinkscore(self,rows):
		uniqueurls = set([row[0] for row in rows ])
		inboundcount = dict([(u,self.con.execute("select count(*) from link where  toid ={}".format(u)).fetchone()[0]) for u in uniqueruls])
		return self.normalizescores(inboundcount)