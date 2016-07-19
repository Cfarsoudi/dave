import zipfile, argparse, os, nltk, operator, re, sys, random
from collections import defaultdict
from nltk.text import ContextIndex
from nltk.parse.stanford import StanfordParser
from generator import sentGenerator
from reportlab.pdfgen import canvas # needed for PDF output

# Parser
parser = argparse.ArgumentParser()
parser.add_argument('i')
parser.add_argument('o')
args = parser.parse_args()

if __name__ == '__main__':

    c = canvas.Canvas(args.o) # create a PDF file with the name taken from the command line
    c.setFont('Courier', 16) # change the font settings
    c.drawCentredString(297.635,420.945,"Movie Title") # prints the movie title
    c.drawCentredString(297.635,375.945,"Written by: D.A.V.E") # prints the author
    c.showPage() # cover page is finsihed, move to new page
    c.setFont('Courier', 12) # change the font settings
    c.drawString(580, 5, "2") # print a '2' in the lower corner for the pg number
    page = 2 # keep track of the page
    pdfszv=810 # y-coordinate for printing text
    pdfszh=30 # x-coordinate for printing text
    base_text = open(args.i, 'rU', encoding='utf-8').read()
    base_sents = nltk.sent_tokenize(base_text)
    gen = sentGenerator(base_text)
    output = open(args.o, 'w', encoding="utf-8")
    sentence = gen()
    #output.write(sentence)
    while(True): # loops until break statement is reached
            if(pdfszv<10): # if the x-coordiante goes below 10
                c.showPage() # move to a new page
                page = page + 1 # increase total pages by one
                pgnum = str(page) # cast that variable to a string
                c.setFont('Courier', 12) # change the font
                c.drawString(580, 5, pgnum) # print the pg number in the corner
                pdfszv=810 # bring y-coordinate back to the top of the page
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
                c.drawString(30,pdfszv,first) # print the first part of the sentence
                pdfszv=pdfszv-15 # move down the y-coordinate down by one line
                sentence = second # rename the second part as sentence so we can loop back and print the rest

            else: 
                if sentence[len(sentence)-1].isspace(): # if the last character is a space
                    sentence = sentence[:len(sentence)-1] # delete the space
                sentence = sentence[:len(sentence)] # delete the last character
                c.drawString(30,pdfszv,sentence) # print the sentence
                pdfszv=pdfszv-15 # move the y-coordinate down by one line
                break # finish the loop

    c.save()

    # lines 109-111 and 117-119 fixes a font issue

    # text = nltk.Text(base_text)
    # text.generate()