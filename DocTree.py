# GdH - 16-7-2017 
# Doel : Geef een datum in en valideer deze
# 3 separate comboboxen voor dag, maand, jaar
# Kunnen eventueel worden samengevoegd in 1 class.
# *****************************************************************
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import webbrowser as web
import time
import os



def DateValidate(year, month, day):
    this_date = '%s/%s/%s' % (month, day, year)
    try:
        time.strptime(this_date, '%m/%d/%Y')
    except ValueError:
        return False
    else:
        return True

def NewPDF():
    #Intitialiseren van de formvelden
    # Open de file-open dialog
    # vul de filenaam in FnameEnt
    FullPath = askopenfilename(filetypes=[("pdf Docs","*.pdf")])
 
    web.open(FullPath)
    window.lift()
    path, filenm=os.path.split(FullPath)
    filenmBase, filenmExt = os.path.splitext(filenm)
    FNameEnt.insert(0, filenmBase)
    # Toon de pdf in een browser
 
def FormValidate(event):
    # print(MnthCB.get())
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
    # Backup maken :
    if os.path.isfile(filenm) == True:
        pass
        #Fout Backupbestand bestaat reeds
    # Uitvoeren van de acties :
    # Bepaal de DestDir
    # 1 - kopieer het bestand naar de BackupDir
    # 2 - Kopieer het bestand naar de DestDir met de naam volgens de FNameEnt + ".pdf"
    # os.makedirs(path)
    # os.exists
    # shutil.copy(src, dst)
    # os.rename(src,dst)
    # 3 - Verwijder het bestand uit de SourceDir 

def hello():
    pass
#
# MAIN()
# 
SourceDir="D:\\mijn documenten\\archief"
importdir = "c:\\users\\Documents"
backupdir = os.path.join(importdir,"DocTreeBackup")
print (backupdir)
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

DayCB = ttk.Combobox(DatumFrame,height=12, width=2, state='readonly')
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

MnthCB = ttk.Combobox(DatumFrame,height=12, width=2, state='readonly')
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

YearCB = ttk.Combobox(DatumFrame,height=12, width=4, state='readonly')
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
CatCBVal=["Hypotheek", "Elektronica", "Sparen", "Verzekering", "Auto", "Werk" 
, "BMN", "Pensioen","Willy","Fokke","Recept"]
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
DocCBVal=["Factuur", "Tijdschrift", "Overzicht", "Brief", "Recept", "Salaris" 
, "Pakbon", "Gebruiksaanwijzing","Nostalgie"]
DocCBVal.sort()
#MnthCB['values']=maand
DocCB.config(values=DocCBVal)
#MnthCB.set('Pipo') 
DocCB.bind('<<ComboboxSelected>>', FormValidate)


RefFrame= Frame(window, relief=SUNKEN, bd=2)
RefFrame.pack(ipady=10, fill = X)
RefEntLabel=Label(RefFrame, text="Referentie")
RefEnt = Entry(RefFrame, width=40)
RefEntLabel.pack(side = LEFT)
RefEnt.pack(side = LEFT)

FNameFrame= Frame(window, relief=SUNKEN, bd=2)
FNameFrame.pack(ipady=10, fill = X)
FNameEntLabel=Label(FNameFrame, text="Filename")
FNameEnt = Entry(FNameFrame, width=40)
FNameEntLabel.pack(side = LEFT)
FNameEnt.pack(side = LEFT)

SaveBtFrame= Frame(window, relief=SUNKEN, bd=2)
SaveBtFrame.pack(ipady=20, fill=BOTH)
SaveBt = Button(SaveBtFrame, text="Save", font=('Comic Sans MS', 20) ,command=SaveBt_do)
SaveBt.pack(fill=BOTH,expand=1)
SaveBt['state']=DISABLED
#SaveBt['state']=ENABLED

window.mainloop()
