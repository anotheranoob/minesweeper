import random
from tkinter import *
from tkinter import messagebox
import sys
class minesweeper_cell(Label):
    def __init__(self, master, text, row, column):
        Label.__init__(self, master, text="", relief=RAISED, width=2, bg="white")
        if isinstance(text, int):
            self.text=text
            self.fg=['black','blue','darkgreen','red','purple','maroon','cyan','black','gray'][text]
            self.isBomb=False
        elif text=="":
            self.text=text
            self.isBomb=False
            self.fg="black"
        else:
            self.text=text
            self.isBomb=True
            self.fg="black"
        self.isFrozen=False
        self.isClicked=False
        self.master=master
        self.row=row
        self.column=column
        self.bind('<Button-1>', self.expose)
        self.bind('<Button-3>', self.freeze)
    def expose(self, x):
        if not(self.isFrozen) and not(self.isClicked):
            self.config(relief=SUNKEN, text=self.text, fg=self.fg, bg="light gray")
            self.isClicked=True
            self.master.expose(self.isBomb, self.get_text(), self.row, self.column)
    def freeze(self, x):
        if self.isClicked==False:
            if self.isFrozen:
                self.config(text="")
                self.isFrozen=False
                self.master.freeze(False)
            else:
                self.config(text="*")
                self.isFrozen=True
                self.master.freeze(True)
    def get_text(self):
        return self.text
    def get_clicked(self):
        return self.isClicked


class minesweeper_grid(Frame):
    def __init__(self, master, string_grid, height, width, numBombs):
        Frame.__init__(self, master)
        self.pack()
        self.str_grid=string_grid
        self.height=height
        self.width=width
        self.numBombsleft=IntVar()
        self.numBombsleft.set(numBombs)
        self.tk_grid={}
        self.numBombLabel=Label(self,textvariable=self.numBombsleft, fg="white", bg="black").grid(row=height, columnspan=width)
        for i in range(height):
            for x in range(width):
                self.tk_grid[(i,x)]=minesweeper_cell(self,self.str_grid[(i,x)],i,x)
                self.tk_grid[(i,x)].grid(row=i, column=x)
    def freeze(self, positive):
        if positive:
            self.numBombsleft.set(self.numBombsleft.get()-1)
        else:
            self.numBombsleft.set(self.numBombsleft.get()+1)
    def expose(self, isBomb, text, row, column):
        if isBomb:
            self.gameLost()
            return
        if text=="":
            for a in [-1, 0, 1]:
                for b in [-1, 0, 1]:
                    try:
                        if self.str_grid[(row,column)]=="" and (a!=0 or b!=0):
                            self.tk_grid[(row+a,column+b)].expose(a)    
                    except KeyError:
                        pass
        for i in self.tk_grid:
            if self.tk_grid[i].get_clicked()==False and self.tk_grid[i].get_text()!="*":
                return
        self.gameWon()
        sys.exit()

    def gameLost(self):
        messagebox.showerror('Minesweeper','KABOOM! You lose.',parent=self)
        for i in self.tk_grid:
            if self.tk_grid[i].get_text()=="*":
                self.tk_grid[i].config(relief=RAISED, bg="red", text="*")
            self.tk_grid[i].isFrozen=True
    def gameWon(self):
        messagebox.showinfo('Minesweeper','Congratulations -- you won!',parent=self)

def play_minesweeper(width, height, numBombs):
    scells={}
    tkcells={}
    sys.setrecursionlimit(width*height*3)
    #this is to make sure it never has a recursion depth error.
    if numBombs<0:
        print("Please use a posiive number of bombs")
        return
    if width<0 or height<0:
        print("Please use a positive height and width")
        return
    if width*height<numBombs:
        print("Please do not put in more bombs then squares")
        return
    for i in range(height):
        for x in range(width):
            scells[(i,x)]=""
    for i in range(numBombs):
        while True:
            (x,y)=(random.randint(0, height-1), random.randint(0,width-1))
            if scells[(x,y)]=="":
                scells[(x,y)]="*"
                break
    for i in range(height):
        for x in range(width):
            if scells[(i,x)]!="*":
                counter = 0
                for a in [-1, 0, 1]:
                    for b in [-1, 0, 1]:
                        try:
                            if scells[(i+a,x+b)]=="*":
                                counter+=1
                        except KeyError:
                            pass
                if counter==0:
                    pass
                else:
                    scells[(i,x)]=counter
    root=Tk()
    game=minesweeper_grid(root, scells, height, width, numBombs)
    game.mainloop()
