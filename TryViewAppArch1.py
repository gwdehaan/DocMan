''''POC DocView GdH 19-11-2017

POC architectuur Docview 
doel App op basis van tk.Tk() met twee frames :
- Frame met QBE selecties
- Frame met output van de Query's met scrollbars

POC
- App
- TopFrame met label
- BottomFrame met label
- App.init()
    frame
''''

import tkinter as tk

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.label = tk.Label(self, text="Hello World", padx=5, pady=5)

        self.label.pack()

if __name__ == "__main__":
    root = Root()
    root.mainloop()
    

import tkinter as tk

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.label = tk.Label(self, text="Hello World", padx=5, pady=5)

        self.label.pack()

class TopFrame(frame):
    def 
if __name__ == "__main__":
    root = Root()
    root.mainloop()