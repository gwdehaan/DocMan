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
			print('DB Closed')
	
	def CreateTables(self):
		# 9-8-2014
		# 3-8-2017 - uitgebreid met Categorie en DocSoort
		try:
			sql="DROP TABLE IF EXISTS DocMan"
			self.cur.execute(sql)
		except lite.Error as e:
			print (e.args[0]) # dit is de letterlijke tekst van de fout.
		sql="""CREATE TABLE DocMan
		 (DocCat TEXT
		  ,DocSoort TEXT
		  ,Pad TEXT
		  ,Filenaam TEXT
		  ,Referentie TEXT
		  ,Datum DATETIME
		  ,PRIMARY KEY(Pad)
		  )
		 """
		try:
			self.cur.execute(sql)
		except lite.Error as e:
			print (e.args[0])
			# Categorie
		try:
			sql="DROP TABLE IF EXISTS DocCat"
			self.cur.execute(sql)
		except lite.Error as e:
			print (e.args[0]) # dit is de letterlijke tekst van de fout.
		sql="""CREATE TABLE DocCat
		 (DocCat TEXT
		  ,PRIMARY KEY(DocCat)
		  )
		 """
		try:
			self.cur.execute(sql)
		except lite.Error as e:
			print (e.args[0])
		#DocSoort
		try:
			sql="DROP TABLE IF EXISTS DocSoort"
			self.cur.execute(sql)
		except lite.Error as e:
			print (e.args[0]) # dit is de letterlijke tekst van de fout.
		sql="""CREATE TABLE DocSoort
		 (DocSoort TEXT
		  ,PRIMARY KEY(DocSoort)
		  )
		 """
		try:
			self.cur.execute(sql)
		except lite.Error as e:
			print (e.args[0])
			
	def insDocCat(self, Categorie):
		sql="""INSERT INTO DocCat Values('""" + Categorie + """');"""
		try:
			self.cur.execute(sql)
			self.con.commit()
		except lite.Error as e:
			print (e.args[0])
			
	def insDocMan(self, DocCat, DocSoort, Pad, Filenaam, Referentie, Datum):
		sql = """INSERT INTO DOCMAN Values('""" + DocCat + \
		"""','""" + DocSoort + \
		"""','""" + Pad + \
		"""','""" + Filenaam + \
		"""','""" + Referentie + \
		"""','""" + Datum +  \
		"""');"""
		try:
			self.cur.execute(sql)
			self.con.commit()
		except lite.Error as e:
			print (e.args[0])		
		
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
t.CreateTables()
t.insDocCat('Software')
t.insDocMan('Software','Factuur','c:\\mijn documenten\\test\\6556449.pdf', '6556449', 'ANS784448', '2009-01-12')
del t
# insert into DocMan Values ('Software','Factuur','c:\mijn documenten\test\6556447.pdf', '6556447', 'ANS784448', '2009-01-12');

