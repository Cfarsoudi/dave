''' 
daveApp.py

Generates screenplay using Markov models of a genre-separated 
screenplay corpus.
'''

from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from PIL import Image, ImageTk
from imageLabels import ImageLabels
from buttonList import ButtonList
from enum import Enum
from random import randint

import argparse, nltk, random, pickle
from collections import defaultdict
from HAL import sentGenerator as gen
from Stanley import director

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

# Each genre has a number associated to it given by its position
# I.e. Action: 0, Adventure: 1, etc.
genres = GenreList('Action', 'Adventure', 'Comedy', 'Crime',
                   'Drama', 'Film-Noir', 'Fantasy', 'Horror',
                   'Mystery', 'Romance', 'Sci-Fi', 
                   'War',)

# Initialize outputMode to a random genre
# so that if the user wants to auto generate,
# a genre will be chosen for them.
global outputMode
outputMode = genres.list[0]

# Set up some variables
genreNames = genres.getNameList()
numGenres = genres.length

class DaveApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'DAVE')

        # self.attributes('-fullscreen', True) # This may not work on windows

        # Sets up the frame that holds all others
        self.container = tk.Frame(self)
        container = self.container
        container.pack(side=TOP, fill=BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Sets up a primary frame for each class
        self.frames = self.constructFrames(container, HomePage, CharacterPage)
        self.showFrame(HomePage)

    def constructFrames(self, parent, page1, page2):
        frames = {}
        pages = (page1, page2)
        for Page in pages:
            frame = Page(parent=parent, controller=self) # Constructs the class
            frames[Page] = frame
            frame.grid(row=0, column=0, sticky='NSEW')
        return frames

    def showFrame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        # Setting up frames for organization of UI
        topFrame = tk.Frame(self)
        topFrame.pack(side=TOP, fill=X)
        
        topRow = tk.Frame(self)
        topRow.pack(side=TOP, fill=BOTH)
        
        botFrame = tk.Frame(self)
        botFrame.pack(side=BOTTOM, fill=X)

        botRow = tk.Frame(self)
        botRow.pack(side=BOTTOM, fill=BOTH)

        k = int(numGenres/2)
        n = numGenres

        # Half of the frames for each genre & movie poster in top row
        horizontalFrames = []
        for i in range(0,k):
            horizontalFrames.append(tk.Frame(topRow))
            horizontalFrames[i].pack(side=LEFT, fill=X, expand=1)

        # Half of the frames for each genre & movie poster in bottom row
        for i in range(k,n):
            horizontalFrames.append(tk.Frame(botRow))
            horizontalFrames[i].pack(side=LEFT, fill=X, expand=1)

        label1 = tk.Label(topFrame, text="Hi, I'm DAVE.", font=DAVE_FONT)
        label1.pack(fill=X, side=TOP)
        label2 = tk.Label(topFrame, text='What genre do you prefer?', 
                          font=SMALL_DAVE)
        label2.pack(pady=10)

        # Button Creation
        btnNames = genreNames # Btns have same names as genreNames
        btnList = ButtonList(controller)
        for i in range(0,n):
            btnList.make_button(horizontalFrames[i], btnNames[i])
            btnList.config_button(i, lambda i=i:
                                  runSpecificGenre(i, controller, CharacterPage))
            btnList.show_button(BOTTOM, i)

        bottomButton = tk.Button(botFrame, text='Surprise Me', 
                                 command=lambda: runRandomGenre())
        bottomButton.pack(side=BOTTOM, pady=5)

        labels = ImageLabels('diehard.jpg','indiana_jones.jpg',
                             'pineapple.jpg', 'godfather.jpg', 'titanic.jpg',
                             'double.jpg', 'panslab.jpg', 'shining.jpg',
                             'maltese.jpg', 'casablanca.jpg',
                             'exmachina.jpg', 'zero.jpg')

        for index in range(labels.length()):
            labels.labelImage(horizontalFrames[index], index)
        labels.displayImages(BOTTOM)

def runRandomGenre():
    global outputMode
    outputMode = setOutputMode(randint(0,numGenres-1)) # Sets a random genre

    print('Output name: ',outputMode.name)
    print('Output number: ',outputMode.number)
    generateScript(outputMode)
    
def runSpecificGenre(flag, controller, cls):
    global outputMode
    outputMode = setOutputMode(flag)
    # controller.showFrame(cls)
    print('Output name: ',outputMode.name)
    print('Output number: ',outputMode.number)
    generateScript(outputMode)

def setOutputMode(flag):
    for Genre in genres.list:
        if flag == Genre.number: # If the index matches the number,
            mode = Genre         # we want to run that genre
    return mode



# Ideally this begins all script generation.
# It takes in the outputMode flag (type Genre) and generates text based
# on the genre given by the flag
def generateScript(outputMode):

    genre = outputMode.name
    # iterate through all the files in the genre's directory
    scriptFormat = {}
    filenames = [('headings', genre + '.Headings'),
                 ('characters', genre + '.Characters'),
                 ('parentheticals', genre + '.Parentheticals'),
                 ('transitions', genre + '.Transitions'),
                 ('actions', genre + '.Actions.pickle'),
                 ('dialogue', genre + '.Dialogue.pickle')]

    for (var, filename) in filenames:
        if filename.endswith('.pickle'):
            loadfile = pickle.load(open(filename, 'rb'))
        else:
            loadfile = open(filename, 'rU', encoding='utf-8').readlines()
            for line in range(len(loadfile)):
                loadfile[line] = loadfile[line].strip()
        scriptFormat[var] = loadfile

    headings = scriptFormat['headings']
    characters = scriptFormat['characters']
    parentheticals = scriptFormat['parentheticals']
    transitions = scriptFormat['transitions']
    actions = scriptFormat['actions']
    dialogue = scriptFormat['dialogue']

    actGen = gen(actions)
    diaGen = gen(dialogue)
    output = open('test.txt', 'w', encoding="utf-8")
    stan = director(headings, characters, parentheticals, transitions,
                    actGen, diaGen, output)
    stan()

def popUpSaveWindow():
    # Generate popup window widget.
    # print("Saved as a PDF.")
    pass

class CharacterPage(tk.Frame):
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
    app = DaveApp()
    app.mainloop()