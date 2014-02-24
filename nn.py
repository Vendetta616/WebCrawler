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

	def getallhiddenids(self,wordids,urlids):
		l1 = {}
		for wordid in wordids:
			cur = self.con.execute("select toid from wordhidden where fromid = {}".format(wordid))
			for row in cur:
				l1[row[0]]=1
		for urlid in urlids:
			cur=self.con.execute("select fromid from hiddenurl where toid ={}".format(urlid))
			for row in cur:
				l1[row[0]]=1
		return l1.keys()

	def setupnetwork(self,wordids,urlids):
		#list of values
		self.wordids = wordids
		self.hiddenids = self.getallhiddenids(wordids,urlids)
		self.urlids=urlids

		#output nodes
		self.ai = [1.0]*len(self.wordids)
		self.ah = [1.0]*len(self.hiddenids)
		self.ao = [1.0]*len(self.urlids)

		#create weighting vector
		self.wi = [[self.getstrength(wordid,hiddenid,0) for hiddenid in self.hiddenids] for wordid in self.wordids]
		self.wo = [[self.getstrength(hiddenid,urlid,1) for urlid in self.urlids] for hiddenid in self.hiddenids]

	def feedfoward(self):
		#input query wordids
		for i in range(len(self.wordids)):
			self.ai[i]=1.0

		#ignition of hiddenlayer
		for j in range(len(self.hiddenids)):
			sum = 0.0
			for i in range(len(self.hiddenids)):
				sum = sum+self.ai[i] * self.wi[i][j]
			self.ah[j] = tanh(sum)

		#ignition of output layer
		for k in range(len(self.urlids)):
			sum = 0.0
			for j in range(len(self.hiddenids)):
				sum = sum+self.ah[j] * self.wo[j][k]
			self.ao[k] = tanh(sum)
		return self.ao[:]

	def getresult(self,wordids,urlids):
		self.setupnetwork(wordids,urlids)
		return self.feedfoward()

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

def trainquery(self,wordids,urlids,selectedurl):
	#generate hidden node if its needs
	self.generatehiddennode(wordids,urlids)
	self.setupnetwork(wordids,urlids)
	self.feedfoward()
	targets = [0.0]*len(urlids)
	targets[urlids.index(selectedurl)] = 1.0
	error = self.backpropagate(targets)
	self.updatedatabase()

def updatedatabase(self):
	#setting to values form database
	for i in range(len(self.wordids)):
		for j in range(len(self.hiddenids)):
			self.setstrength(self.wordids[i],self.hiddenids[j],0,self.wi[i][j])
		for j in range(len(self.hiddenids)):
			for k in range(len(self.self.urlids)):
				self.setstrength(self.hiddenids[j],self.urlids[k],1,self.wo[j][k])
		self.con.commit()
