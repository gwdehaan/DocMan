import sqlite3 as lite

def MergeDocMan():
	'''
	Voeg records uit een andere Db toe aan de productie Db
	- voer een query uit - resulaat is een list of lists
	wordt via executemany ingelezen in de productie Db, unieke sleutel op pad.
	DocMan.db bevat de laatste bestanden
	DocMan(Laatste) bevat is een restore.
	'''
	con = lite.connect('DocMan(Laatste).db')
	con2 = lite.connect('DocMan.db')
	# Gebruik de dictionary om velden te selecteren, daarmee kan de standaard print(row) niet werken. Geeft dan alleen de memory locatie.
	#con.row_factory = lite.Row
	cur = con.cursor()
	cur2 = con2.cursor()
	
	sql="""SELECT * FROM DocMan;"""
	try:
		cur.execute(sql)
		rows = cur.fetchall()
		print (rows)
		cur2.executemany("INSERT INTO DocMan VALUES(?, ?, ?, ?, ?, ?)", rows)
		con2.commit()
		for row in rows:
			print(row)
	#		for i in row:
	#			print(i)
	except lite.Error as e:
		print (e.args[0])

	if con:
		con.close()
		con2.close()
		print('DB Closed')
		
MergeDocMan()
