"""
This program that outputs screenplays with the correct format could not be 
tested with traditional unit testing. Of all the methods I wrote to ouput text
to the pdf, none returned anything, so it's hard to use unit testing. Instead,
I wrote a sample script and tested the corner cases like around the page 
break. The acceptance criteria for this test includes: headings, characters, 
action, dialogue, parantheticals, and transitions formatted correctly, no 
awkward page breaks, spacing and indentation is consistent, no text runs off
the page, page numbers are formatted correctly, correct capitalization
"""
from reportlab.pdfgen import canvas # needed for PDF output

class textC: # class to define text and type of text
    def __init__(self, str, typ):
        self.txt = str
        self.type = typ

c = canvas.Canvas("movescript.pdf") # create a PDF
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

def write(str, type): # helper function to write text according to text type
    if type == 'heading':
        writeHeading(str)
    elif type == 'action':
        writeAction(str)
    elif type == 'character':
        writeCharacter(str)
    elif type == 'paranthetical':
        writeParanthetical(str)
    elif type == 'dialog':
        writeDialog(str)
    elif type == 'transition':
        writeTransition(str)

def moveDownLine(): # function to move down a line in the PDF
    global pdfszv
    global pdfszh
    pdfszv = pdfszv - 15 # go units down
    pdfszh = 40 # reposition on the left side of the page

def writeHeading(string): # function to write scene headings
    global pdfszv
    global pdfszh
    global sceneheading
    sceneheading = sceneheading + 1 # keep track of the scene headings
    sch = str(sceneheading) # cast the int to a string
    sch = sch + "."
    if(pdfszv<40): # if the x-coordiante goes below 40
        newPage() # start a new page
    else: # otherwise
        moveDownLine() # move down two lines
        moveDownLine()
    strn = string.upper() # make the string all caps
    c.drawString(pdfszh-30, pdfszv, sch) # print the scene number
    c.drawString(pdfszh, pdfszv, strn) # print the scene heading
    moveDownLine() 

def writeAction(str): # function to write action lines
    global pdfszv
    global pdfszh
    if(pdfszv<30): # if the x-coordiante goes below 30
        newPage() # start a new page
    else: 
        moveDownLine()
    printAction(str) # use helper function to write the actionline
    moveDownLine()

def writeCharacter(str): # function to write character headings
    global pdfszv
    global pdfszh
    if(pdfszv<60): # if the x-coordiante goes below 40
        newPage() # start a new page
    else:
        moveDownLine() # move down two lines
        moveDownLine()
    strn = str.upper() # make the string all caps
    c.drawCentredString(297.635, pdfszv, strn) # print the character

def writeParanthetical(str): # function to write parantheticals
    global pdfszv
    global pdfszh
    if(pdfszv<30): # if the x-coordiante goes below 30
        newPage() # start a new page
    else:
        moveDownLine() # move down a line
    c.drawCentredString(265,pdfszv,str) # print the paranthetical 

def writeDialog(str): # function to write dialog
    global pdfszv
    global pdfszh
    if(pdfszv<30): # if the x-coordiante goes below 30
        newPage() # start a new page
    else:
        moveDownLine()
    printDialog(str) # use the helper function to print the dialog
    moveDownLine()

def writeTransition(str): # function to write transitions
    global pdfszv
    global pdfszh
    if(pdfszv<40): # if the x-coordiante goes below 40
        newPage() # start a new page
    else:
        moveDownLine() # go down two lines
        moveDownLine()
    strn = str.upper() # make the string all caps
    c.drawRightString(575,pdfszv,strn)
    moveDownLine() # move down a line

def printAction(str): # helper function to print action lines
    global pdfszv
    global pdfszh
    sentence = str
    while(True): # loops until break statement is reached
        if(pdfszv<30): 
            newPage()
        if len(sentence) > 75: # if the sentence is longer than the width of the page
            p = 75 # set p to 75 (width of the page)
            while(True): # loop until break statement is reached
                if not sentence[p].isspace(): # if the char at the pth position is not a space
                    p = p-1 # decrement p by one and loop back
                else: # if the char at the pth position is a space
                    break # finish the loop
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
            break # finish the loop

def printDialog(str):
    global pdfszv
    global pdfszh
    sentence = str
    while(True): # loops until break statement is reached
        if(pdfszv<30): # if the x-coordiante goes below 10
            c.drawCentredString(297.635,20,"(MORE)")
            newPage()
            c.drawCentredString(297.635,800,"(CONT'D)")
        if len(sentence) > 42: # if the sentence is longer than the width of the page
            p = 42 # set p to 75 (width of the page)
            while(True): # loop until break statement is reached
                if not sentence[p].isspace(): # if the char at the pth position is not a space
                    p = p - 1 # decrement p by one and loop back
                else: # if the char at the pth position is a space
                    break # finish the loop
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
            break # finish the loop

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

a = textC("on top of mount everest", 'heading')
b = textC("Superman hovers over 21 dead bodies as he yells and fires his heat vision through the Himalayas. He comes to a brief stop.", 'action')
cc = textC("superman", 'character')
d = textC("(scared)", 'paranthetical')
e = textC("I hate tacos! I’m going to put an end to whoever invented those tortillas filled with evil. Just wait and see", 'dialog')
f = textC("dissolve to:", 'transition')
g = textC("on top of the empire state building", 'heading')
h = textC("You can see an atomic bomb dropping in the distance. The screen slows as the nuke gets closer to the ground. A beam of light comes toward the camera", 'action')
i = textC("fade to white:", 'transition')
j = textC("central park", 'heading')
k = textC("Kids are playing on the playground and jumping off the swings", 'action')
l = textC("sarah", 'character')
m = textC("I just don't know what to do anymore. I have no idea where he is. Ever", 'dialog')
n = textC("Hannah looks up with a slight look of disgust", 'action')
o = textC("hannah", 'character')
p = textC("What do you mean? He's just out being Superman", 'dialog')
q = textC("sarah", 'character')
r = textC("Yea I know but that's just not what I want. I wish he would just go to circus school. He'd make his family really proud if he did that. But I don't think he'll ever amount to anaything. I mean fighting bad guys and all, he's just going to get himself killed.", 'dialog')
s = textC("hannah", 'character')
t = textC("You're being ridiculous sarah, I wish you could see yourself right now", 'dialog')

write("FADE IN:", 'action')
write(a.txt, a.type)
write(b.txt, b.type)
write(cc.txt, cc.type)
write(d.txt, d.type)
write(e.txt, e.type)
write(f.txt, f.type)
write(g.txt, g.type)
write(h.txt, h.type)
write(i.txt, i.type)
write(j.txt, j.type)
write(k.txt, k.type)
write(l.txt, l.type)
write(m.txt, m.type)
write(n.txt, n.type)
write(o.txt, o.type)
write(p.txt, p.type)
write(q.txt, q.type)
write(r.txt, r.type)
write(s.txt, s.type)
write(t.txt, t.type)
write(f.txt, f.type)
write(g.txt, g.type)
write(o.txt, o.type)
write(p.txt, p.type)
write(q.txt, q.type)
write(r.txt, r.type)
c.save()



