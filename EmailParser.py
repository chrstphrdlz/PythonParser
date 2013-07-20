"""
Christopher Deleuze
Contains an email parsing class which is initialized with a dictionary of fields mapped to 
corresponding regex strings. Can be used to parse multiple emails with its parse 
function, will return ParsedEmail object. Can display results by printing ParsedEmail object or 
printing individual parsed fields in the ParsedEmail object


"""
import re
import sys

#Main class, stores a dictionary mapping the email textfile names, 
#and the regular expression search strings
class EmailParser:
    
    #Takes in a list or regex strings to search
    def __init__(self):
        #All regex expressions map to inner field information
        self.fieldDictionary = {'Subject': 'Subject\s*?:(.*?)\n\S','Date' : 'Date\s*?:(.*?)\n\S','From' : 'From\s*?:(.*?)\n\S','To' : 'To\s*?:(.*?)\n\S','Content' : '--.*?\n(Content.*?Type.*?:.*?)(?=--)','Cc': 'Cc\s*?:(.*?)\n\S','Bcc': 'Bcc\s*?:(.*?)\n\S'}

    #Finds string matched by the EmailParser's regexStrings and mapps it to a seperate dictionary
    #Returns a ParsedEmail object made from the dictionary
    def parseEmail(self, text, emailName):
        getParsedFieldDictionary = {}

        for expression in self.fieldDictionary:
            #Get all matches and store it as a list in result
            result = re.findall(self.fieldDictionary[expression], text, re.DOTALL)

            if len(result) > 0:
                #If it is the content, store the entire list
                #If not, just store the first match
                if(expression != 'Content'):
                    result = result[0]

                getParsedFieldDictionary[expression] = result

        return ParsedEmail(getParsedFieldDictionary)


#Parsed email class, can print to display all parsed fields, or select a field to print
class ParsedEmail:
    #Has a dictionary mapping fields to the found strings
    #The content is mapped to a list of the separate multiple content sections
    def __init__(self, dictionary):
        self.getParsedFieldDictionary = dictionary

    def __str__(self):
        returningString = ""

        for field in self.getParsedFieldDictionary:
            #Print Content last
            if field != "Content":
                returningString += self.getParsedField(field) + "\n"
        if "Content" in self.getParsedFieldDictionary:
            returningString += self.getParsedField("Content") + "\n"
        return returningString

    #Returns a string representing the parsed field
    def getParsedField(self,field):

        returningString = ""
        returningString += field + ": "

        if field in self.getParsedFieldDictionary:

            if field == "Content":
                contentList = self.getParsedFieldDictionary[field]
                sizeContentList = len(contentList)
                i = 0

                if sizeContentList > 0:

                    if sizeContentList > 1:
                        returningString += "There are multiple content sections\n"

                        while i < sizeContentList:
                            returningString += "Content section " + str(i+1) + "\n" + contentList[i] + "\n"
                            i+=1
                    else:
                        returningString += contentList[i] + "\n"
            else:
                returningString += self.getParsedFieldDictionary[field]
        else:
            returningString += "Field not found"

        return returningString


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
if len(sys.argv) < 2 :
    print("\n\nusage: python EmailParser.py [email/text/document/path(s)] \n")
    sys.exit()

#Initialize 
i=1
emailFileNames = sys.argv[1:]
numArgs = len(sys.argv)
emailText = []

#Get file text and add to the list of emailText
while i < numArgs:
    string = getTextFromFile(sys.argv[i])    
    emailText.append(string)
    i+=1

#Create an email parser
emailParser = EmailParser()

#Parse the email
i=0
numEmails = len(emailFileNames)
while i < numEmails:
    parsedEmail = emailParser.parseEmail(emailText[i], emailFileNames[i])     
    print(parsedEmail)
    i+=1