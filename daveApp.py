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

class Genre():
    def __init__(self, name, number):
        self.name = name
        self.number = number

class GenreList():
    def __init__(self, *args):
        self.list = []
        for index, arg in enumerate(args):
            self.list.append(Genre(arg, index))
        self.length = len(self.list)

    def getNameList(self):
        nameList = []
        for Genre in self.list:
            nameList.append(Genre.name)
        return nameList

# Create a list of Genres
# Each genre has a number associated to it given by its position
# I.e. SciFi: 0, Comedy: 1, etc.
genres = GenreList('SciFi', 'Comedy', 'Thriller', 'Drama')

# Set up some variables
genreNames = genres.getNameList()
numGenres = genres.length

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

    print('Output name: ',outputMode.name)
    print('Output number: ',outputMode.number)
    # Should output a script after calling this function
    
def runSpecificGenre(flag, controller, cls):
    global outputMode
    outputMode = setOutputMode(flag)
    controller.showFrame(cls)
    print('Output name: ',outputMode.name)
    print('Output number: ',outputMode.number)

def setOutputMode(flag):
    for Genre in genres.list:
        if flag == Genre.number: # If the index matches the number,
            mode = Genre         # we want to run that genre
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