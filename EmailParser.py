"""
Christopher Deleuze
Contains an email parsing class which is initialized with a list of regex strings to search with
Can be used to parse multiple emails with it's parse function
Results from search displayed by printing object

"""
import re
import sys

#Main class, stores a dictionary mapping the email textfile names, 
#and the regular expression search strings
#Prints the email file name, and the found strings
class emailParser:
    
    #Takes in a list or regex strings to search
    def __init__(self,regexStrings):
        self.fieldDictionary = {}
        self.regexStrings = regexStrings

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
    def addParsedInfo(self, emailName, message):

        if emailName in self.fieldDictionary:            
            self.fieldDictionary[emailName].append(message)

        else:
            self.fieldDictionary[emailName] = [message]

    #Finds string matched by the emailParser's regexStrings and mapps it to the object's dictionary
    def parseEmail(self, text, emailName):
        for expression in self.regexStrings:
            result = re.findall(expression, text, re.DOTALL)
            if len(result) > 0:
                self.addParsedInfo(emailName, result[0])





#Make a default field emailParser
def parseDefaultFields():
    return emailParser(['Subject\s*?:.*?\n','Date\s*?:.*?\n','To\s*?:.*?\n','From\s*?:.*?\n','--.*?Content.*?Type.*?:(.*?)--.*?Content.*?Type.*?:'])





def getTextFromFile(fileString):
    try:
        file = open(fileString,"r")

    except  IOError:
        print("Could not open " + fileString + ". File does not exist")
        return ""

    addToString = file.read()

    return addToString




#Main running function
#If arguments improperly used
if len(sys.argv) < 2 or "-e" not in sys.argv:
    print("\n\nusage: python EmailParser.py -e email/text/document/path(s) [-c config/file/location]\n")
    sys.exit()

#Initialize 
i=2
emailFileNames = sys.argv[2:]
numArgs = len(sys.argv)
emailText = []

#Ignore the last two arguments if there is a -c
if "-c" in sys.argv:
    numArgs = numArgs - 2

#Get file text and add to the list of emailText
while i < numArgs:

    string = getTextFromFile(sys.argv[i])    

    emailText.append(string)

    i+=1

#Create an email parser
#For customized searching, look for -c
if "-c" in sys.argv:
    #get the text from the file, split it and use the regex commands to initialize the parser
    userArguments = getTextFromFile(sys.argv[len(sys.argv)-1])

    userArguments = userArguments.split(" ")

    emailParser = emailParser(userArguments)

#Default (no -c)
else:    
    emailParser = parseDefaultFields()


#Parse the email
i=0
numEmails = len(emailText)
while i < numEmails:

    emailParser.parseEmail(emailText[i], emailFileNames[i])

    i+=1

#Print the results of the parsing
print (emailParser)