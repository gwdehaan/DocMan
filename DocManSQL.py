import sqlite3 as lite
import csv
import os
from datetime import datetime
"""
DocManSql - wrapper om SQLite
Exceptions : moeten door de UI worden afgehandeld.

"""
class DocManSql:
	# Phytonista : BasisClass voor database van DocMan.
	con=None
	cur=None
	
	
	def __init__(self):
		# >>> if platform.uname().node == 'GdH-Surface':
		# ...     print(platform.uname())
		# ...
		# uname_result(system='Windows', node='GdH-Surface', release='10', version='10.0.15063', machine='AMD64', processor='Intel64 Family 6 Model 78 Stepping 3, GenuineIntel')
		# >>>
		# GreyHound ******************************************************************
		# self.con = lite.connect('D:\\Bestanden\\OneDrive\\Archief\\DocMan.db')
		# Surface ********************************************************************
		# self.con = lite.connect('C:\\Users\\Geert\\OneDrive\\Archief\\DocMan.db')
		# Test ***********************************************************************
		self.con = lite.connect('DocMan.db')
		# C:\Users\Geert\OneDrive\Archief
		# Gebruik de dictionary om velden te selecteren
		# (GdH - Niet) self.con.row_factory = lite.Row
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

	def DumpDbDocMan(self):
		'''
		maak een volledige dump naar een csv file.
		DocManDb<timestamp>.csv
		print(datetime.now().strftime('%Y%m%d%H%M%S'))
		'''

		sql="""SELECT * FROM DocMan;"""
		try:
			self.cur.execute(sql)
			rows = self.cur.fetchall()
			for row in rows:
				print(row)
        	# ToDo Nu rows aanbieden aan de CSV module voor export
		except lite.Error as e:
			print("Dump naar CSV", e.args[0])
			exit()

		fname = 'DocMan' + datetime.now().strftime('%Y%m%d%H%M%S') + '.csv'
		print(fname)
		header=['DocCat' ,'DocSoort','Pad','Filenaam','Referentie' ,'Datum']
		with open(fname, 'wt') as csvout:
			file_writer = csv.writer(csvout, dialect='unix')
			file_writer.writerow(header)
			file_writer.writerows(rows)

		if self.con:
			self.con.close()
		
	def insDocMan(self, DocCat, DocSoort, Pad, Filenaam, Referentie, Datum):
	
		try:
			#self.cur.execute(sql)
			self.cur.execute("INSERT INTO DocMan Values(?,?,?,?,?,?)", (DocCat, DocSoort, Pad, Filenaam, Referentie, Datum)) 
			self.con.commit()
		except lite.Error as e:
			print (e.args[0])		
		
		
	def DbRecordMissingHandler(self, FilePad):
		'''
		Handler voor het geval de integriteitscheck tussen Db en filesysteem mislukt.
		standaard wordt deze geprint, maar kan door bijvoorbeeld TKinter worden overruled
		'''
		print(Filepad, " bestaat in Db, niet op deze bestandsloctie.")
		
	def IntCheckFilesFromDb(self, DocTreeRoot):
		'''
		integriteitscheck : loop door de Db en controleer of de file aanwezig is volgens het pad.
		Het pad wordt samemgesteld op basis van de rubriek en jaar informatie.
		- select * from DocMan.
		- loop door cursor
		- haal variabelen op (datum, categorie, fname)
		- maak en test het pad
		- try /except
		- test NOK: door naar handler
		- standaard handler : print de betreffende file op de standaard output.
		- handler kan worden overruled in TKinter bijvoorbeeld om files in een listboc te tonen
		
		'''
		sql="""SELECT DocCat, Filenaam, Datum FROM DocMan ORDER BY DocCat, datum;"""
		try:
			self.cur.execute(sql)
			rows = self.cur.fetchall()
			for row in rows:
				print(row)
				# Ophalen van de velden
				DocCat = row[0]
				Filenaam = row[1]
				Datum = row[2]
				jaar=Datum[:4]
				# pad samenstellen
				FullPath = os.path.join(DocTreeRoot, DocCat)
				FullPath = os.path.join(FullPath, jaar)
				FullPath = os.path.join(FullPath, Filenaam)
				if os.path.isfile(FullPath) == False:
					# Db record bestaat niet op schijf.
					DbRecordMissingHandler(FullPath)
				
		except lite.Error as e:
			print("Integriteitscheck op Db", e.args[0])
			exit()



			
	def IntCheckDbFromFiles(self, DocRoot):
		'''
		'''
		for root, dirs, files in os.walk(DocRoot, topdown=False):

			for name in files:
				zk=name.find('.pdf')
				if zk != -1:
					Process(os.path.join(root, name))
		
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
#5t.CreateTables()
#t.insDocCat('Software')
t.insDocMan('Software','Factuur','c:\\mijn documenten\\test\\6556449.pdf', '6556449', 'ANS784448', '2009-01-12')
t.DumpDbDocMan()
del t
# insert into DocMan Values ('Software','Factuur','c:\mijn documenten\test\6556447.pdf', '6556447', 'ANS784448', '2009-01-12');

