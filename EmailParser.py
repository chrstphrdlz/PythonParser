"""
Christopher Deleuze

"""
import re
import sys
#These feilds can be expanded to include more options

emailStrings = []


class fieldParser:
    
    #Takes in email files to parse through
    def __init__(self,emailStrings):
        self.fieldDictionary = {}
        self.email = emailStrings

    #Prints each associated email (dictionary key) and all the fields found
    def __str__(self):

        returningString = "\n\n\n"
        
        if len(self.fieldDictionary) == 0:
            returningString += "Did not find any fields."

        for email in self.fieldDictionary:

            returningString += "Email adress: " + email + "\n" +"\n"

            for field in self.fieldDictionary[email]:

                returningString += field + "\n"

            returningString += "\n"

        return returningString

    #Takes the index of the current email (for mapping) and the text to map it to
    def addEmailFeild(self, emailIndex, message):

        if self.email[emailIndex] in self.fieldDictionary:            
            self.fieldDictionary[self.email[emailIndex]].append(message)

        else:
            self.fieldDictionary[self.email[emailIndex]] = [message]

        


#The main parsing function       
def parseEmail(emailParser, text, index):

    #This is the list of fields to be searched for using the contained regular expressions
    listOfRegularExpressions = ['Subject.*?:.*[^\S]','Date.*?:.*[\n.]','To:.*[\n.]','From:.*[\n.]']

    for expression in listOfRegularExpressions:
        result = re.findall(expression, text, re.M)[0]
        emailParser.addEmailFeild(index, result)


def getTextFromFile(fileString):
    try:
        file = open(fileString,"r")

    except  IOError:
        print("Could not open " + fileString + ". File does not exist")
        return ""

    addToString = file.read()

    return addToString



#This is the main running function

#For improper usage and help
if len(sys.argv) < 2:
    print("\n\nusage: python EmailParser.py [-m] [email/text/document/path(s)]\n")
    print("type python EmailParser.py -help for more information\n\n")
    sys.exit()

if sys.argv[1] == "-help":
    print("")

#If -m is given, multiple arguments are given
#adjust email strings to start from index 2
if sys.argv[1] == "-m":

    i=2

    emailStrings = sys.argv[2:]

#default
else:
    i=1

    emailStrings = [sys.argv[1]]


numArgs = len(sys.argv)

emailText = []


#Get file text and add to the list of emailText
while i < numArgs:

    string = getTextFromFile(sys.argv[i])    

    emailText.append(string)

    i+=1

#Create an email parser
emailParser = fieldParser(emailStrings)

#Parse the email
i=0
numArgs = len(emailText)
while i < numArgs:

    parseEmail(emailParser, emailText[i], i)

    i+=1

#Print the parser
print (emailParser)
