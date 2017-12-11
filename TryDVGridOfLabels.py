# Bron : https://stackoverflow.com/questions/11047803/creating-a-table-look-a-like-tkinter/11049650
# GdH 30-10-2017
# met scrollbars :
# https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter

import tkinter as tk

# class die overerft van tk.Tk
# __init__ wordt overruled.
class ExampleApp(tk.Tk):
    def __init__(self):
        # initialisatie van Tk
        tk.Tk.__init__(self)
        # Maak een tabel 10 breed, 2 hoog
        t = SimpleTable(self, 10,2)
        # Layoutmanager
        t.pack(side="top", fill="x")
        # zet cel 0,0 op "Hello World"
        t.set(0,0,"Hello, world")

# Class die overerft van tk.frame

class SimpleTable(tk.Frame):
    # init van de simpletable
    def __init__(self, parent, rows=10, columns=2):
        # use black background so it "peeks through" to 
        # form grid lines
        # init van het frame
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tk.Label(self, text="%s/%s" % (row, column), 
                                 borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1) #padx en pady laten het zwart van het frame doorschijnen
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            # standaardfunctie binnen Tk, effect is niet duidelijk
            self.grid_columnconfigure(column, weight=1)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()