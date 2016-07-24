from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from PIL import Image, ImageTk
from imageLabels import ImageLabels
from buttonList import ButtonList
from enum import Enum
from random import randint

global outputMode

# Constant fonts
LARGE_FONT = ('Verdana', 30)
SMALL_FONT = ('Verdana', 15)
DAVE_FONT = ('American Typewriter', 30)
SMALL_DAVE = ('American Typewriter', 20)

# Name the genres here
genreNames = ['SciFi', 'Comedy', 'Thriller', 'Drama']
numGenres = len(genreNames)

# Flags to signal different genres for script output
class Genre(Enum):  
        
        SciFi = 0
        Comedy = 1
        Thriller = 2
        Drama = 3

class DAVEapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'DAVE')
        # self.minsize(width=1000, height=600)
        # self.maxsize(width=1000, height=600)

        # Sets up the main frame that hold all others
        container = tk.Frame(self)
        container.pack(side=TOP, fill=BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Sets up a main frame for each class
        self.frames = {}
        pages = (HomePage, Page)
        for P in pages:
            frame = P(container, self) # Constructs the class
            self.frames[P] = frame
            frame.grid(row=0, column=0, sticky='NSEW')
            self.showFrame(HomePage)

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        # Setting up frames for organization of UI
        topFrame = tk.Frame(self)
        topFrame.pack(side=TOP, fill=X)
        botFrame = tk.Frame(self)
        botFrame.pack(side=BOTTOM, fill=X)

        # Frames for each genre & movie poster
        frames = []
        for i in range(numGenres):
            frames.append(tk.Frame(self))
            frames[i].pack(side=LEFT, fill=X, expand=1)

        label1 = tk.Label(topFrame, text="Hi, I'm DAVE.", font=DAVE_FONT)
        label1.pack(fill=X, side=TOP)
        label2 = tk.Label(topFrame, text='What genre do you prefer?', 
                          font=SMALL_DAVE)
        label2.pack(pady=10)

        # Button Creation
        btnNames = genreNames # Btns have same names as genreNames
        btnList = ButtonList(controller)
        for i in range(numGenres):
            btnList.make_button(frames[i], btnNames[i])
            btnList.config_button(i, lambda i=i: 
                                  runSpecificGenre(i, controller, Page))
            btnList.show_button(BOTTOM, i)
        bottomButton = tk.Button(botFrame, text='Surprise Me', 
                                 command=lambda: runRandomGenre())
        bottomButton.pack(side=BOTTOM, pady=10)

        labels = ImageLabels('exmachina.jpg', 'pineapple.jpg', 
                             'pulpfiction.jpg', 'titanic.jpg')
        for index in range(labels.length()):
            labels.labelImage(frames[index], index)
        labels.displayImages(BOTTOM)

def runRandomGenre():
    global outputMode
    outputMode = setOutputMode(randint(0,numGenres-1)) # Sets a random genre
    print('Execute main program...')
    print('Random global mode enum: ',outputMode)
    # Should output a script after calling this function
    
def runSpecificGenre(index, controller, cls):
    global outputMode
    outputMode = setOutputMode(index)
    controller.showFrame(cls)
    print('Global mode enum: ',outputMode)

def setOutputMode(index):
    for genre in Genre:
        if index == genre.value: # If the index matches the enum,
            mode = genre         # set the correct mode
    return mode

class Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        topFrame = tk.Frame(self)
        topFrame.pack(side=TOP, fill=X)

        label = tk.Label(topFrame, text='Characters', font=LARGE_FONT)
        label.pack(fill=X, pady=10, padx=10)
        label1 = tk.Label(self, text='Would you like to name your characters?',
                          font=SMALL_FONT)
        label1.pack(pady=40, padx=10)
        add_btn = tk.Button(self, text='Add')
        add_btn.pack(pady=50)
        button1 = tk.Button(self, text='Home',
                            command=lambda: controller.showFrame(HomePage))
        button1.pack()

if __name__ == '__main__':
    app = DAVEapp()
    app.mainloop()