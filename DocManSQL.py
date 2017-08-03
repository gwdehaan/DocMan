import sqlite3 as lite

"""
DocManSql - wrapper om SQLite
Exceptions : moeten door de UI worden afgehandeld.

"""
class DocManSql:
	# Phytonista : BasisClass voor database van DocMan.
	con=None
	cur=None
	
	
	def __init__(self):
		self.con = lite.connect('DocMan.db')
		# Gebruik de dictionary om velden te selecteren
		self.con.row_factory = lite.Row
		self.cur =self.con.cursor()	
		
	def __del__(self):
		if self.con:
			self.con.close()
			print 'DB Closed'
	
	def CreateTable(self):
		# 9-8-2014
		try:
			sql="DROP TABLE IF EXISTS DocMan"
			self.cur.execute(sql)
		except lite.Error, e:
			print e.args[0] # dit is de letterlijke tekst van de fout.
		sql="""CREATE TABLE DocMan
		 (Category TEXT
		  ,Bron TEXT
		  ,Pad TEXT
		  ,Filenaam TEXT
		  ,Omschrijvng TEXT
		  ,Datum DATETIME
		  ,Boek TEXT
		  ,Bladzijde INTEGER
		  ,PRIMARY KEY(Pad, Filenaam)
		  )
		 """
		try:
			self.cur.execute(sql)
		except lite.Error, e:
			print e.args[0]

# Change - SQL's kunnen INSERTS of UPDATES zijn.
# Exceptions door fouten in de primary key; melden via de UI
def Change(self, CSQL)	:
	self.cur.execute(CSQL)
	self.con.commit()
#  Query - return een dictionary met veldnamen en waarden
def Query(self, QSQL) :
	self.cur.execute(QSQL)
# Uitzoeken hoe het row object is opgebouwd (tuple ?) return een list of rows?
		
# *************************************************************************************		
t=DocManSql()
t.CreateTable()
del t

