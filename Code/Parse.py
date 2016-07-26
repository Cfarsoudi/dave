"""
Parse.py 
Parses screenplays into subsections.
Returns a compilation of all headings, characters, transitions, actions,
parentheticals, and dialogue as separate files.
"""
import argparse

# Parser for command line arguments
# This module takes one filename
# an input file which will have its
# contents parsed
# and one genre name which describes
# the content of the input file
parser = argparse.ArgumentParser()
parser.add_argument('i')
parser.add_argument('o')
args = parser.parse_args()

if __name__ == '__main__':

    # here we open up our input and output files 
    # our input file should contain a movie script or series of scripts
    # we will set up output files for each type of text format
    # (ie: scene headings, action, transitions, etc.)
    # and setup the booleans that will control our parsing

    genre = args.o + '_'
    inputFile = open(args.i, 'rU', encoding="UTF-8")
    outHead = open("%sHeadings" % genre,"w", encoding='UTF-8')
    outAct = open("%sActions" % genre,"w", encoding='UTF-8')
    outChar = open("%sCharacters" % genre, "w", encoding='UTF-8')
    outDia = open("%sDialogue" % genre,"w", encoding='UTF-8')
    outParen = open("%sParentheticals" % genre,"w", encoding='UTF-8')
    outTrans = open("%sTransitions" % genre,"w", encoding='UTF-8')

    char = False
    paren = False
    Dialog = False

    #lists for storing lines of text
    heading = []
    character = []
    action = []
    dialog = []
    parenthetical = []
    transitions = []

    # convert the given spreadsheet into a list, containing 
    # each of its lines as a single line
    listFile = inputFile.readlines()

    #holding variables for multi-line chunks of dialog or action direction
    MLdialog=''
    MLaction=""

    # split each item in listFile (line from the spreadsheet) on 'tab' characters
    # so that each line is now a list of answers to the survey questions
    # this will make accessing individual elements that we judge for 
    # clustering each respondent easier
    for c in range(len(listFile)):
        line = listFile[c]
        if len(line) > 1:
            if(len(line.split())==0):
                continue
            first = line.split()[0]
            if (first.upper() == 'INT.' 
                    or first.upper() == 'EXT.'):
                char = False
                paren = False
                heading.append(line)
            elif line.isupper():
                deline = line.lstrip(' ')
                if(deline == 'CUT TO:\n' or deline == 'FADE IN:\n' 
                        or deline == 'FADE OUT:\n' or deline == 'DISSOLVE TO:\n' 
                        or deline == 'SMASH CUT:\n' or deline == 'END CREDITS\n'
                        or deline == 'CUT TO BLACK.\n'  or deline == 'CONTINUED:\n'
                        or deline == '(CONTINUED)\n'):
                    transitions.append(line)
                elif char and deline[0] == '(':
                    char = False
                    paren = True
                    parenthetical.append(line)
                else:
                    character.append(line)
                    char = True
            elif char and first[0] == '(':
                char = False
                paren = True
                parenthetical.append(line)
            elif char or paren:
                d = c
                if(d < len(listFile)):
                    nextIndent=(len(listFile[d+1])-len(listFile[d+1].lstrip(' ')))
                    currIndent=(len(listFile[d])-len(listFile[d].lstrip(" ")))
                    if(currIndent>nextIndent):
                        MLdialog=MLdialog+line
                        char = False
                        paren = False
                        if(len(MLdialog)!=0):
                            dialog.append(MLdialog)
                        MLdialog=''
                    elif(currIndent==nextIndent):
                        MLdialog=MLdialog+line
                        if(d+1==len(listFile)):
                            dialog.append(MLdialog)
                    d=d+1
                c=d
            else:
                if(c<len(listFile)):
                    if(c+1!=len(listFile)):
                        nextIndent = len(listFile[c+1]) - len(listFile[c+1].lstrip(" "))
                    else:
                        nextIndent = len(listFile[c]) - len(listFile[c].lstrip(" "))
                    currIndent = len(listFile[c]) - len(listFile[c].lstrip(" "))
                    if(currIndent != nextIndent):
                        char = False
                        paren = False
                        if(len(MLaction) != 0):
                            action.append(MLaction)
                        MLaction = ''
                    elif(currIndent == nextIndent):
                        MLaction = MLaction + line
                        if(c+1==len(listFile)):
                            action.append(MLaction)
                    c=c+1

    # write the contents from the text format lists
    # to the appropriate output files
    outHead.write(' '.join(heading))
    outChar.write(' '.join(character))
    outAct.write(' '.join(action))
    outDia.write(' '.join(dialog))
    outParen.write(' '.join(parenthetical))
    outTrans.write(' '.join(transitions))
