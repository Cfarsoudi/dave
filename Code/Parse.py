import random

#helper function to print because Python 3.4 doesn't just print strings 
#normally.
#this function prints output to a given output file as a string
def outPrint(words,out):
    out.write(words)#.decode('UTF-8'))

#print to output file, followed by a newline character
def outPrintln(words,out):
    outprint(words,out)
    out.write('\n')

#returns true if a list is empty
def empty(lis):
    return (len(lis)==0)

#pops and removes a random item from a list
def randomPop(lis):
    rand = int(random.random()*len(lis))
    if(rand == len(lis) and not empty(lis)):
        rand=rand-1
    elif(empty(lis)):
        print('empty')
    obj = lis[rand]
    lis.remove(obj)
    return obj

#the director decides what to print out next
def stanley(head, act, char, paren, dia, trans,out):
    needHeader = True
    needAction = False
    needCharacter = False
    needDialog = False
    needTransition = False
    needParanthetical = False
    while(not (empty(head) and empty(act) and empty(char) 
            and empty(paren) and empty (dia) and empty(trans))):
        if(needCharacter and needTransition and needAction and needHeader):
            rand = random.random()*(len(head)+len(act)+len(char)+len(trans))
            if(rand <=len(head) and not empty(head)):
                currentScene = randomPop(head)
                outputFile.write('location: ')
                outPrint(currentScene,out)
                needHeader = False
                needAction = True
            elif(rand <= len(act)+len(head) and not empty(act)):
                nextAction = randomPop(act)
                outputFile.write('action:')
                outPrint(nextAction,out)
                needCharacter = True
                needTransition = True
                needHeader = True
            elif(rand <= len(char)+len(act)+len(head) and not empty(char)):
                nextChar = randomPop(char)
                outputFile.write('character:')
                outPrint(nextChar, out)
                needDialog = True
                needParanthetical = True
            elif(rand <= len(trans)+len(act)+len(char)+len(head) 
                    and not empty(trans)):
                nexttrans = randomPop(trans)
                outputFile.write('transition:')
                outPrint(nexttrans,out)
                needHeader = True
                needTransition = False
        if(needDialog):
            if(needParanthetical 
                   and random.random()*(len(dia)+len(paren))<=len(paren) 
                   and not empty(paren)):
                nextPara = randomPop(paren)
                outputFile.write('paranthetical:')
                outPrint(nextPara, out)
                needParanthetical = False
                nextPhrase = randomPop(dia)
                outputFile.write('dialog:')
                outPrint(nextPhrase, out)
                needDialog = False
                needHeader = True
                needAction = True
                needTransition = True
                needCharacter = True
            elif(not empty(dia)):
                nextPhrase = randomPop(dia)
                outputFile.write('dialog:')
                outPrint(nextPhrase, out)
                needDialog = False
                needHeader = True
                needAction = True
                needTransition = True
                needCharacter = True
        elif(needAction and not empty(act)):
            nextAction = randomPop(act)
            outputFile.write('Action:')
            outPrint(nextAction,out)
            needCharacter = True
            needTransition = True
            needHeader = True
        elif(needHeader and not empty(head)):
            currentScene = randomPop(head)
            outputFile.write('Location:')
            outPrint(currentScene,out)
            needHeader = False
            needAction = True
        else:
            return#print('unaccounted for')#return
    return

#here we open up our input and output files 
#and setup the booleans that will control our parsing
inputFile = open('input', 'rU', encoding="utf-8")
outputFile = open("output","w")
char = False
paren = False
Dialog = False

#lists for storing lines of text
action = []
character = []
heading = []
transitions = []
dialog = []
paranthetical = []

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
    line = listFile[c]#.decode('UTF-8')
    if len(line) > 1:
        #print(line.split())
        #print(len(line.split()))
        if(len(line.split())==0):
            continue
        first = line.split()[0]
        #print (first)
        if (first.upper() == 'INT.' 
                or first.upper() == 'EXT.'):
            char = False
            paren = False
            heading.append(line)
        elif line.isupper():
            deline = line.lstrip(' ')
            #print (deline[0])
            if(deline == 'CUT TO:\n' or deline == 'FADE IN:\n' 
                    or deline == 'FADE OUT:\n' or deline == 'DISSOLVE TO:\n' 
                    or deline == 'SMASH CUT:\n' or deline == 'END CREDITS\n'
                    or deline == 'CUT TO BLACK.\n'  or deline == 'CONTINUED:\n'
                    or deline == '(CONTINUED)\n'):
                transitions.append(line)
            elif char and deline[0] == '(': # and first[len(first)-1] == 41:
                # if(deline[len(deline)-1] != ')'):
                #     while(deline[len(deline)-1] != ')' and c+1<len(listFile)):
                #         line = line + listFile[c+1].decode('UTF-8')
                #         c= c+1
                char = False
                paren = True
                paranthetical.append(line)
            else:
                character.append(line)
                char = True
        elif char and first[0] == 40 and first[len(first)-1] == 41:
            char = False
            paren = True
            paranthetical.append(line)
        elif char or paren:
            char = False
            paren = False
            dialog.append(line)
            d = c
            if(d < len(listFile)):
            #for d in range(c, len(listFile)-1):
                nextIndent=(len(listFile[d+1])-len(listFile[d+1].lstrip(' ')))#.decode('UTF-8').lstrip(' ')))
                currIndent=(len(listFile[d])-len(listFile[d].lstrip(" ")))#.decode('UTF-8').lstrip(' ')))
                print(currIndent)
                print(nextIndent)
                if(currIndent>nextIndent):
                    print("finished"+ MLdialog)
                    char = False
                    paren = False
                    dialog.append(MLdialog)
                    MLdialog=''
                elif(currIndent==nextIndent):
                    print(MLdialog)
                    MLdialog=MLdialog+line
                d=d+1
        else:
            char = False
            paren = False
            action.append(line)

print(action)
print(dialog)
print(paranthetical)
print(character)
print(heading)
print(transitions)

stanley(heading,action,character,paranthetical,dialog,transitions,outputFile)

#print('=====================================================================')

#print(action)
#print(dialog)
#print(paranthetical)
#print(character)
#print(heading)
#print(transitions)
