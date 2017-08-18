#!/usr/bin/env python
#
# GdH - DocTREE (16-7-2017)
# Doel : Rubriceren van archief aan pdf's opgebouwd vanaf 2011. Documenten worden in een boom
# opgenomen op basis van een categorie.
# Datum, Documentsoort en een vrij referentieveld worden opgeslagen in een database.
# Het is mogelijk om de bestandsnaam aan te passen in de form.
# Het oorspronkelijke document wordt bewaard in een ./DocTreeBackup subdir van de brondir.
# Deze versie maakt geen gebruik van classes, daarom wordt gebruik gemaakt van globals.
#
#
# DocTreeRoot- root voor doctree archief
# Sourcedir - t.b.v. openfilenamebox
#
# 3-8-2017 - Issue - Bij verwijderen van pdf wordt het bestand gelockt
# doordat Edge deze nog in gebruik heeft : 
# Om het verwijderen van de pdf mogelijk te maken kan met KillEdge de browser
# worden afgesloten.
#
# copy2 gebruikt, hiermee blijven datum en tijd bewaard.
# 4-8-2018 
#- SQLITE Db toegevoegd. Tabellen worden gemaakt via sqldocman.py
#- RELFile toegevoegd om relatief pad op te slaan in Db
# ****************************************************************************************
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import webbrowser as web
import time
import os
import shutil
import psutil
from datetime import datetime
import sqlite3 as lite

def hello():
	pass
	
def DateValidate(year, month, day):
    this_date = '%s/%s/%s' % (month, day, year)
    try:
        time.strptime(this_date, '%m/%d/%Y')
    except ValueError:
        return False
    else:
        return True

def KillEdge():
    '''
    Functie om Lopende Edge processen te killen
    '''
    for proc in psutil.process_iter():
        if str(proc.name).find('Edge.exe') > 0:
            proc.kill()

def NewPDF():
    #Intitialiseren van de formvelden   
    DayCB.set('')
    MnthCB.set('')
    YearCB.set('')
    CatCB.set('')
    DocCB.set('')
    RefEnt.delete(0, END)
    RefEnt.insert(0, '')
    FNameEnt.delete(0, END)
    FNameEnt.insert(0, '')
    SaveBt['state']=DISABLED
    # Open de file-open dialog
    # vul de filenaam in FnameEnt, 
    global FullPath
    global filenmExt
    FullPath = askopenfilename(filetypes=[("pdf Docs","*.pdf")])
 	# Toon de pdf in de default browser
    web.open(FullPath)
    #Poging om de form on top te krijgen
    window.lift()
    # Toon de filename in de Entrybox
    path, filenm=os.path.split(FullPath)
    filenmBase, filenmExt = os.path.splitext(filenm)
    FNameEnt.delete(0, END)
    FNameEnt.insert(0, filenmBase)
   
 
def FormValidate(event):
    # Wordt aangeroepen bij elke wijziging van een combobox
    dag=DayCB.get()
    maand=MnthCB.get()
    jaar=YearCB.get()
    cat=CatCB.get()
    doc=DocCB.get()
    #ref=RefEnt.get()
    
    # Datum, Categorie, Document moeten gevuld zijn
    # datumvalidatie en check op filename hoort bij de SaveBt_do() (SaveButton)
    if maand != "" and jaar !="" and cat != "" and doc != "":
        SaveBt['state']="normal"
    else:
        SaveBt['state']=DISABLED
    
def insDbDocMan(DocCat, DocSoort, Pad, Filenaam, Referentie, Datum):
    con = lite.connect('D:\\Bestanden\\OneDrive\\Archief\\DocMan.db')
	# Gebruik de dictionary om velden te selecteren
    con.row_factory = lite.Row
    cur =con.cursor()	
    # Toevoegen record
    sql = """INSERT INTO DOCMAN Values('""" + DocCat + \
	"""','""" + DocSoort + \
	"""','""" + Pad + \
	"""','""" + Filenaam + \
	"""','""" + Referentie + \
	"""','""" + Datum +  \
	"""');"""
    try:
        cur.execute(sql)
        con.commit()
    except lite.Error as e:
        # Om de SQL interactie in een class onder te brengen zou een methode voor 
        # het weergeven van de foutmelding (standaard via printcommando's) voor
        # gebruik met bijv. TKinter kunnen worden overruled. (GdH - 12-8-2017) 
        messagebox.showerror("Error DocMan Database", e.args[0])
    finally:
    # Afsluiten
        con.close()

def SaveBt_do():
    # Valideer de datum
    dag=DayCB.get()
    maand=MnthCB.get()
    jaar=YearCB.get()
    cat=CatCB.get()
    doc=DocCB.get()
    ref=RefEnt.get()
    fn=FNameEnt.get()
    if DateValidate(jaar, maand, dag) == False :    
        messagebox.showerror("Datum", "Datum fout")
        return
    if fn=='':
        messagebox.showerror("Filename", "Filename is leeg")
        return
    # Datum format aanpassen :
    DocDate = '{:%Y-%m-%d}'.format(datetime(int(jaar),int(maand),int(dag)))
    # Edge afsluiten om te voorkomen dat er locking optreedt bij het verwijderen.
    KillEdge()
    # ************* Backup maken :
    # FullPath is een global met volledig pad en filename naar de inputfile
    path, filenm=os.path.split(FullPath)
    filenmBase, filenmExt = os.path.splitext(filenm)
    BUDir = os.path.join(path, 'DocTreeBackup')
    if os.path.isdir(BUDir) == False:
        os.mkdir(BUDir)
        
    BUFile = os.path.join(BUDir, filenm)
    try:
    	shutil.copy2(FullPath, BUFile)
    except:
    	messagebox.showerror("Backup", "Backupfile bestaat reeds")
    	return
	# ************** Kopieer het bestand naar de juiste subir
    CATDir = os.path.join(DocTreeRoot, cat)
    CATDir = os.path.join(CATDir, jaar)
    RELDir = os.path.join(cat, jaar)
    try:
        os.makedirs(CATDir)
    except OSError:
        pass
    CATFile = os.path.join(CATDir, fn)
    RELFile = os.path.join(RELDir, fn)
    CATFile = CATFile+ filenmExt
    RELFile = RELFile+ filenmExt
    try:
        shutil.copy2(FullPath, CATFile)
        try:
            os.remove(FullPath)
        except:
            messagebox.showerror("Delete from sourcedir", "Verwijderen mislukt_")
            return
    except:
        messagebox.showerror("Copy naar DocTreeRoot", "Bestand bestaat reeds")
        return
    # Bewaar in de database 
    insDbDocMan(cat,doc, RELFile, fn, ref, DocDate)
    # Alle acties zijn succesvol afgerond, volgende
    NewPDF()

    
    # Uitvoeren van de acties :
    # Bepaal de DestDir
    # 1 - kopieer het bestand naar de BackupDir
    # 2 - Kopieer het bestand naar de DestDir met de naam volgens de FNameEnt + ".pdf"
    # os.makedirs(path)
    # os.exists
    # shutil.copy(src, dst)
    # os.rename(src,dst)
    # 3 - Verwijder het bestand uit de SourceDir 

def DumpDbDocMan():
    '''
    maak een volledige dump naar een csv file.
    DocManDb<timestamp>.csv
    '''
    con = lite.connect('D:\\Bestanden\\OneDrive\\Archief\\DocMan.db')

    cur = con.cursor()

    sql="""SELECT * FROM DocMan;"""
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        # ToDo Nu rows aanbieden aan de CSV module voor export
    except lite.Error as e:
        messagebox.showerror("Dump naar CSV", e.args[0])
        return

    if con:
        con.close()


#
# MAIN()
# 
DocTreeRoot="D:\\Bestanden\\OneDrive\\Archief\\DocTree"

window =Tk()
window.title("DocTree")

menubar = Menu(window)

# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=NewPDF)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)

# create more pulldown menus
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=hello)
editmenu.add_command(label="Copy", command=hello)
editmenu.add_command(label="Paste", command=hello)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=hello)
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
window.config(menu=menubar)
#window.geometry("300x300")
#
# ttk combobox voor Dagdeel van de datum
#
DatumFrame=Frame(window, bd=2, width=30, relief=SUNKEN)
DatumFrame.pack(ipady=10, fill = X)
DatumLabel=Label(DatumFrame, text="Datum     ")
DatumLabel.pack(side = LEFT)

#
#
#

DayCB = ttk.Combobox(DatumFrame,height=12, width=2)
DayCB.pack(side = LEFT)
Days=[]
for i in range(1,32):
    Days.append(i)
DayCB.config(values=Days)
DayCB.set('')
DayCB.bind('<<ComboboxSelected>>', FormValidate)
label_1=Label(DatumFrame, text="-")
label_1.pack(side=LEFT)
#
# ttk combobox voor Maanddeel van de datum
#

MnthCB = ttk.Combobox(DatumFrame,height=12, width=2)
MnthCB.pack(side = LEFT)
maand=[1,2,3,4,5,6,7,8,9,10,11,12]
#MnthCB['values']=maand
MnthCB.config(values=maand)
#MnthCB.set('Pipo') 
MnthCB.bind('<<ComboboxSelected>>', FormValidate)
label_2=Label(DatumFrame, text="-")
label_2.pack(side=LEFT)
#
# ttk combobox voor Maanddeel van de datum
#

YearCB = ttk.Combobox(DatumFrame,height=12, width=4)
YearCB.pack(side = LEFT)
Years=[]
for i in range(1961, 2018):
    Years.append(i)
Years.sort(reverse=TRUE)
#MnthCB['values']=maand
YearCB.config(values=Years)
#MnthCB.set('Pipo') 
YearCB.bind('<<ComboboxSelected>>', FormValidate)
#
# Categorie van de pdf.
#
CatFrame=Frame(window, relief=SUNKEN, bd=2)
CatFrame.pack(ipady=10, fill = X)
CatCBLabel= Label(CatFrame, text="Categorie")
CatCBLabel.pack(side=LEFT)
CatCB = ttk.Combobox(CatFrame,height=12, width=30, state='readonly')
CatCB.pack(side = LEFT)
CatCBVal=["Motor", "Belastingen","Hypotheek", "Hardware","Software","Elektronica", "Sparen", "Verzekering", "Auto", "Werk" 
, "BMN", "Pensioen","Willy","Fokke", "LG73", "Apparaat", "Familie", "Geert", "Gezondheid", "Nuts", "IT-Alg", "Vakantie"]
CatCBVal.sort()
#MnthCB['values']=maand
CatCB.config(values=CatCBVal)
#MnthCB.set('Pipo') 
CatCB.bind('<<ComboboxSelected>>', FormValidate)
#
# Documentsoort (GdH 20-7-2017)
#
DocFrame=Frame(window, relief=SUNKEN, bd=2)
DocFrame.pack(ipady=10, fill = X)
DocCBLabel= Label(DocFrame, text="Document")
DocCBLabel.pack(side=LEFT)
DocCB = ttk.Combobox(DocFrame,height=12, width=30, state='readonly')
DocCB.pack(side = LEFT)
DocCBVal=["Factuur", "Tijdschrift", "Artikel", "Aanmaning", "Overzicht", "Brief", "Recept", "Salaris" 
, "Pakbon", "Gebruiksaanwijzing", "Garantie", "Nostalgie", "Bevestiging", "Folder", "Schema",]
DocCBVal.sort()
#MnthCB['values']=maand
DocCB.config(values=DocCBVal)
#MnthCB.set('Pipo') 
DocCB.bind('<<ComboboxSelected>>', FormValidate)


RefFrame= Frame(window, relief=SUNKEN, bd=2)
RefFrame.pack(ipady=10, fill = X)
RefEntLabel=Label(RefFrame, text="Referentie")
RefEnt = Entry(RefFrame, width=50)
RefEntLabel.pack(side = LEFT)
RefEnt.pack(side = LEFT)

FNameFrame= Frame(window, relief=SUNKEN, bd=2)
FNameFrame.pack(ipady=10, fill = X)
FNameEntLabel=Label(FNameFrame, text="Filename")
FNameEnt = Entry(FNameFrame, width=50)
FNameEntLabel.pack(side = LEFT)
FNameEnt.pack(side = LEFT)

SaveBtFrame= Frame(window, relief=SUNKEN, bd=2)
SaveBtFrame.pack(ipady=20, fill=BOTH)
SaveBt = Button(SaveBtFrame, text="Save", font=('Comic Sans MS', 20) ,command=SaveBt_do)
SaveBt.pack(fill=BOTH,expand=1)
SaveBt['state']=DISABLED
#SaveBt['state']=ENABLED

window.mainloop()
