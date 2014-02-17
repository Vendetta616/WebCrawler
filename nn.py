from math import tanh
import sqlite3

class searchnet:
	def __init__(self,dbname):
		self.con = sqlite3.connect(dbname)

	def __del__(self):
		self.con.close()

	def maketables(self):
		self.con.execute("create table hiddennode(create_key)")
		self.con.execute("create table wordhidden(fromid,toid,strength)")
		self.con.execute("create table hiddenurl(fromid,toid,strength)")
		self.con.commit()

	def getstrength(self,fromid,toid,layer):
		if layer == 0:
			table = "wordhidden"
		else:
			table = "hiddenurl"
		res = self.con.execute("select strength from {} where fromid = {} and toid ={}".format(table,fromid,toid)).fetchone()

		if res ==None:
			if layer ==0:
				return -0.2
			if layer ==1:
				return 0
		return res[0]


	def setstrength(self,fromid,toid,layer,strength):
		if layer ==0:
			table = "wordhidden"
		else:
			table ="hiddenurl"

		res =self.con.execute("select rowid from {} where fromid = {} and toid ={}".format(table,fromid,toid)).fetchone()

		if res ==None:
			self.con.execute("insert into {} (fromid,toid,strength) values ({},{},{:f})".format(table,fromid,toid,strength))
		else:
			rowid = res[0]
			self.con.execute("update {} set strength = {:f} where rowid = {}".format(table,strength,rowid))

	def generatehiddennode(self,wordids,urls):
		if len(wordids)>3:
			return None

		#check Node has already created with this word set
		createkey = "_".join(sorted([str(wi) for wi in wordids]))
		res = self.con.execute("select rowid from hiddennode where create_key = '{}'".format(createkey)).fetchone()

		#if not exits node, create node
		if res == None:
			cur= self.con.execute("insert into hiddennode (create_key) values ('{}')".format(createkey))
			hiddenid = cur.lastrowid
			#set default value
			for wordid in wordids:
				self.setstrength(wordid,hiddenid,0,1.0/len(wordids))
			for urlid in urls:
				self.setstrength(hiddenid,urlid,1,0.1)
			self.con.commit()

	def gethiddenids(self,wordids,urlids):
		l1 = {}
		for wordid in wordids:
			cur = self.con.execute("select toid from wordhidden where fromid = {}".format(wordid))
			for row in cur:
				l1[row[0]]=1
		for urlid in urlids:
			cur self.con.execute("select fromid from hiddenurl where toid ={}".format(urlid))
			for row in cur:
				l1[row[0]]=1
		return l1.keys

	