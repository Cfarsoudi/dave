"""
Parse.py 

Parses screenplays into subsections.
Returns a compilation of all headings, characters, transitions, actions,
parentheticals, and dialogue as separate files.
"""
import os

if __name__ == '__main__':

    #here we open up our input and output files 
    #and setup the booleans that will control our parsing
    dataset_dict = {}

    # iterate through all the files in the current directory
    for filename in os.listdir("."):
        dataset_dict[filename] = open(filename, 'rU', encoding='utf-8')

    for filename, infile in dataset_dict.items():
        genre = filename.split('data')[0]
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
        listFile = infile.readlines()

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
                elif char and first[0] == 40 and first[len(first)-1] == 41:
                    char = False
                    paren = True
                    parenthetical.append(line)
                elif char or paren:
                    d = c
                    if(d < len(listFile)-1):
                        nextIndent=(len(listFile[d+1])-len(listFile[d+1].lstrip(' ')))
                        currIndent=(len(listFile[d])-len(listFile[d].lstrip(" ")))
                        if(currIndent>nextIndent):
                            char = False
                            paren = False
                            if(len(MLdialog)!=0):
                                dialog.append(MLdialog)
                            MLdialog=''
                        elif(currIndent==nextIndent):
                            MLdialog=MLdialog+line
                        d=d+1
                    c=d
                else:
                    if(c<len(listFile)-1):
                        nextIndent = len(listFile[c+1]) - len(listFile[c+1].lstrip(" "))
                        currIndent = len(listFile[c]) - len(listFile[c].lstrip(" "))
                        if(currIndent != nextIndent):
                            char = False
                            paren = False
                            if(len(MLaction) != 0):
                                action.append(MLaction)
                            MLaction = ''
                        elif(currIndent == nextIndent):
                            MLaction = MLaction + line
                        c=c+1

        outHead.write(' '.join(heading))
        outChar.write(' '.join(character))
        outAct.write(' '.join(action))
        outDia.write(' '.join(dialog))
        outParen.write(' '.join(parenthetical))
        outTrans.write(' '.join(transitions))