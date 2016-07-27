'''
Stanley.py
'''

import random, time
from HAL import sentGenerator as gen
from reportlab.pdfgen import canvas # needed for PDF output

class textC: # class to define text and type of text
    def __init__(self, str, typ):
        self.txt = str
        self.type = typ

c = canvas.Canvas("moviescript.pdf") # create a new PDF
count = 0

def initPdf():
    global page, pdfszv, pdfszh, sceneheading, count, c
    c = canvas.Canvas("moviescript.pdf") # create a PDF
    c.setFont('Courier', 16) # change the font 
    c.drawCentredString(297.635,420.945,"Movie Title")
    c.drawCentredString(297.635,375.945,"Written by: D.A.V.E")
    c.showPage() # new page
    c.setFont('Courier', 12) # 
    c.drawString(580, 5, "2") # print the page number
    page = 2 # keep track of the page
    pdfszv = 785 # y-coordinate for printing text
    pdfszh = 40 # x-coordinate for printing text
    sceneheading = 0
    count = 0

def write(str, type): # helper function to write text according to text type
    if type == 'heading':
        writeHeading(str)
    elif type == 'action':
        writeAction(str)
    elif type == 'character':
        writeCharacter(str)
    elif type == 'parenthetical':
        writeParenthetical(str)
    elif type == 'dialog':
        writeDialog(str)
    elif type == 'transition':
        writeTransition(str)

def moveDownLine(): # down a line in the PDF
    global pdfszv
    global pdfszh
    pdfszv = pdfszv - 15 # go units down
    pdfszh = 40 # reposition on the left side of the page

def writeHeading(string): # write scene headings
    global pdfszv
    global pdfszh
    global sceneheading
    sceneheading = sceneheading + 1 # keep track of the scene headings
    sch = str(sceneheading)
    sch = sch + "."
    if(pdfszv<40): # if the x-coordiante goes below 40
        newPage() # start a new page
    else:
        moveDownLine() # otherwise move down two lines
        moveDownLine()
    strn = string.upper() # make the string all caps
    c.drawString(pdfszh-30, pdfszv, sch) # print the scene number
    c.drawString(pdfszh, pdfszv, strn)   # and scene heading
    moveDownLine() 

def writeAction(str): # write action lines
    global pdfszv
    global pdfszh
    if(pdfszv<30): # if the x-coordiante goes below 30
        newPage() # start a new page
    else: 
        moveDownLine()
    printAction(str) # helper function to write the actionline
    moveDownLine()

def writeCharacter(str): # write character headings
    global pdfszv
    global pdfszh
    if(pdfszv<60): # if the x-coordiante goes below 40
        newPage() # start a new page
    else:
        moveDownLine() # move down two lines
        moveDownLine()
    strn = str.upper()
    c.drawCentredString(297.635, pdfszv, strn) # print the character

def writeParenthetical(str): # function to write parentheticals
    global pdfszv
    global pdfszh
    if(pdfszv<30): # if the x-coordiante goes below 30
        newPage()
    else:
        moveDownLine() # move down a line
    c.drawCentredString(265,pdfszv,str) # print the parenthetical 

def writeDialog(str): # function to write dialog
    global pdfszv
    global pdfszh
    if(pdfszv<30): # if the x-coordiante goes below 30
        newPage()
    else:
        moveDownLine()
    printDialog(str) # use the helper function to print the dialog
    moveDownLine()

def writeTransition(str): # function to write transitions
    global pdfszv
    global pdfszh
    if(pdfszv<40): # if the x-coordiante goes below 40
        newPage()
    else:
        moveDownLine() # go down two lines
        moveDownLine()
    strn = str.upper() 
    c.drawRightString(575,pdfszv,strn)
    moveDownLine()

def printAction(str): # helper function to print action lines
    global pdfszv
    global pdfszh
    sentence = str
    pageWidth = 75
    while(True): # loops until break statement is reached
        if(pdfszv<30): 
            newPage()
        if len(sentence) > pageWidth: # if the sentence is longer than the width of the page
            p = pageWidth # set p to width of the page
            while(True):
                if not sentence[p].isspace(): # if the char at the pth position is not a space
                    p = p-1 # continue decrementing p
                else: # if the char at the pth position is a space
                    break
            first = sentence[:p] # break the sentence up by where the space is
            second = sentence[-(len(sentence)-p)+1:] # the second sentence is the rest without the space
            if sentence[len(sentence)-1].isspace(): # if the last character on the line is a space
                sentence = sentence[:len(sentence)-1] # delete the space
            sentence = sentence[:len(sentence)] # delete the last character 
            c.drawString(40,pdfszv,first) # print the first part of the sentence
            pdfszv = pdfszv - 15 # move down the y-coordinate down by one line
            sentence = second # rename the second part as sentence so we can loop back and print the rest
        else: 
            if sentence[len(sentence)-1].isspace(): # if the last character is a space
                sentence = sentence[:len(sentence)-1] # delete the space
            sentence = sentence[:len(sentence)] # delete the last character
            c.drawString(40,pdfszv,sentence) # print the sentence
            break

def printDialog(str):
    global pdfszv
    global pdfszh
    sentence = str
    dialogueWidth = 42
    while(True): # loops until break statement is reached
        if(pdfszv<30): # if the x-coordiante goes below 10
            c.drawCentredString(297.635,20,"(MORE)")
            newPage()
            c.drawCentredString(297.635,800,"(CONT'D)")
        if len(sentence) > dialogueWidth: # if the sentence is longer than the width of the page
            p = dialogueWidth # set p to 42 (width of the page)
            while(True): # loop until break statement is reached
                if not sentence[p].isspace(): # if the char at the pth position is not a space
                    p = p - 1 # decrement p by one and loop back
                else: # if the char at the pth position is a space
                    break
            first = sentence[:p] # break the sentence up by where the space is
            second = sentence[-(len(sentence)-p)+1:] # the second sentence is the rest without the space
            if sentence[len(sentence)-1].isspace(): # if the last character on the line is a space
                sentence = sentence[:len(sentence)-1] # delete the space
            sentence = sentence[:len(sentence)] # delete the last character 
            c.drawCentredString(297.635,pdfszv,first) # print the first part of the sentence
            pdfszv = pdfszv - 15 # move down the y-coordinate down by one line
            sentence = second # rename the second part as sentence so we can loop back and print the rest

        else: 
            if sentence[len(sentence)-1].isspace(): # if the last character is a space
                sentence = sentence[:len(sentence)-1] # delete the space
            sentence = sentence[:len(sentence)] # delete the last character
            c.drawCentredString(297.635,pdfszv,sentence) # print the sentence
            break

def newPage():
    global pdfszv
    global pdfszh
    global page
    c.showPage() # move to a new page
    page = page + 1 # increase total pages by one
    pgnum = str(page) # cast that variable to a string
    c.setFont('Courier', 12) # change the font
    c.drawString(580, 5, pgnum) # print the pg number in the corner
    pdfszv=785 # bring y-coordinate back to the top of the page

initPdf()
write("FADE IN:", 'action')

class Director(object):
    """
    The Director Stanley decides what to print out next.

    Param:
        head : list of header strings
        char : list of character strings
        paren : list of parenthetical strings
        trans : list of transition strings
        act : sentGenerator for action 
        dia : sentGenerator for dialogue

        ret: list of (formatType, string) for furture formatting
    """
    def __init__(self, headers, characters, parentheticals,
                 transitions, actions, dialogue, outfile):

        self.head = headers
        self.char = characters
        self.paren = parentheticals
        self.trans = transitions
        self.act = actions
        self.dia = dialogue
        self.out = outfile
    
    def __call__(self):
        global c, count
        if count > 0:
            initPdf()
        retScript = self.writeScript(5, self.out)
        for (flag, line) in retScript:
            write(line, flag)
        c.save()
        count = count + 1

    def writeScript(self, length, outfile):

        retScript = []

        needHeader = True
        needAction = False
        needCharacter = False
        needDialog = False
        needTransition = False
        needParenthetical = False

        for i in range(length):
            actlen = 1.8 * len(self.char)
            dialen = 2.2 * len(self.char)

            if (needCharacter and needTransition and needAction and needHeader):
                rand = random.random() * (len(self.head) + actlen +
                                          len(self.char) + len(self.trans))     
                if (rand < len(self.head) and len(self.head) > 0):
                    currentScene = self.__randomPop(self.head)
                    retScript.append(('heading', currentScene))
                    needHeader = False
                    needAction = True

                elif (rand < actlen + len(self.head) and actlen > 0):
                    nextAction = self.act(3)
                    retScript.append(('action', nextAction))
                    needCharacter = True
                    needTransition = True
                    needHeader = True

                elif (rand < len(self.char) + actlen + len(self.head) 
                        and len(self.char) > 0):
                    nextChar = self.__randomPop(self.char)
                    retScript.append(('character', nextChar))
                    needDialog = True
                    needParenthetical = True

                elif (rand < len(self.trans) + actlen + len(self.char) 
                           + len(self.head) and len(self.trans) > 0):       
                    nexttrans = self.__randomPop(self.trans)
                    retScript.append(('transition', nexttrans))
                    needHeader = True
                    needTransition = False

            if needDialog:
                rand = random.random() * (dialen + actlen + len(self.paren))

                if (needParenthetical and rand < len(self.paren) 
                                      and len(self.paren) > 0):
                    nextPara = self.__randomPop(self.paren)
                    retScript.append(('parenthetical', nextPara))
                    needParenthetical = False

                for i in range(random.randint(1, 10)):
                    nextPhrase = self.dia()
                    retScript.append(('dialog', nextPhrase))

                needDialog = False
                needHeader = True
                needAction = True
                needTransition = True
                needCharacter = True

            elif needAction and actlen > 0:

                for i in range(random.randint(0, 3)):
                    nextAction = self.act(3)
                    retScript.append(('action', nextAction))

                needCharacter = True
                needTransition = True
                needHeader = True

            elif (needHeader and len(self.head) > 0):
                    currentScene = self.__randomPop(self.head)
                    retScript.append(('heading', currentScene))
                    needHeader = False
                    needAction = True
            else:
                break

        return retScript

    def __randomPop(self, lis):
        """
        Pops off a random item from a list.
        """
        rand = int(random.random() * len(lis))
        if (rand == len(lis) and len(lis) > 0):
            rand -= 1
        obj = lis[rand]
        lis.remove(obj)
        return obj