# 1. Create a database table in RAM named  Roster  that includes the fields
#     Name , Species  and  IQ
# 2. Populate your new table with the following values:
#     Jean-Baptiste Zorg,    Human,    122
#     Korben Dallas,     Meat Popsicle,    100
#     Ak'not,    Mangalore,    -5
# 3. Update the Species of Korben Dallas to be Human
# 4. Display the names and IQs of everyone in the table who is classified as Human
# GdH - 21-1-2017
#
import sqllite3

connection = sqlite3.connect(´:memory:´)

c = connection.cursor()

c.execute(´CREATE TABLE roster
c.execute("CREATE TABLE roster(Name TEXT, Species TEXT, IQ INT)")

#2 populate the table
people_values = (           

('Jean-Baptiste Zorg', 'Human', 122),           
('Korben Dallas', 'Meat Popsicle', 100),           
('Ak'not', 'Mangalore', -5)

)
c.executemany("INSERT INTO roster VALUES(?, ?, ?)", people_values)

# select all first and last names from
# Check of alle records er zijn
c.execute("SELECT * FROM roster ")    
for row in c.fetchall():        
	print(row)

# 3. Update the Species of Korben Dallas to be Human
c.execute("UPDATE roster SET species=? WHERE Name=?",('Human', 'Korben Dallas'))

# 4. Display the names and IQs of everyone in the table who is classified as Human

c.execute("SELECT * FROM roster WHERE species='Human'")    
for row in c.fetchall():        
	print(row)