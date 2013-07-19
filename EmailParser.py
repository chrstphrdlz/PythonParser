"""
Christopher Deleuze
Contains an email parsing class which is initialized with a list of regex strings to search with
Can be used to parse multiple emails with it's parse function, will return ParsedEmail object
Can display results by printing ParsedEmail object or printing individual parsed fields in 
ParsedEmail object

"""
import re
import sys

#Main class, stores a dictionary mapping the email textfile names, 
#and the regular expression search strings
#Prints the email file name, and the found strings
class EmailParser:
    
    #Takes in a list or regex strings to search
    def __init__(self,regexFieldDictionary):
        self.fieldDictionary = regexFieldDictionary

    #Takes the index of the current email (for mapping) and the text to map it to
    def addParsedInfo(self, emailName, message):

        if emailName in self.fieldDictionary:            
            self.fieldDictionary[emailName].append(message)

        else:
            self.fieldDictionary[emailName] = [message]

    #Finds string matched by the EmailParser's regexStrings and mapps it to a seperate dictionary
    #Returns a ParsedEmail object made from the dictionary
    def parseEmail(self, text, emailName):
        parsedFieldDictionary = {}

        for expression in self.fieldDictionary:
            result = re.findall(self.fieldDictionary[expression], text, re.DOTALL)

            if len(result) > 0:
                #In the case of the content, the result is the boarder
                #Split the border and omit the first element in the list (not in the content)
                if(expression == 'Content'):
                    result = text.split(str(result[0]))[1:]
                    result = result[:len(result)-1]
                else:
                    result = result[0]

                #Replace the regex string with the found info
                parsedFieldDictionary[expression] = result

        return ParsedEmail(parsedFieldDictionary)


#Parsed email class, can print to display all parsed fields, or select a field to print
class ParsedEmail:
    #Has a dictionary mapping fields to the found strings
    #The content is mapped to a list of the seperate multiple content sections
    def __init__(self, dictionary):
        self.parsedFieldDictionary = dictionary

    def __str__(self):
        returningString = ""

        for field in self.parsedFieldDictionary:
            returningString += field + ": "

            #If field is content, print all sections seperatly, listing the content section number
            if field == "Content":
                contentList = self.parsedFieldDictionary[field]
                sizeContentList = len(contentList)
                i = 0

                if sizeContentList > 1:
                    returningString += "There are multiple content sections\n"

                    while i < sizeContentList:
                        returningString += "Content section " + str(i+1) + "\n" + contentList[i] + "\n"
                        i+=1
            else:
                 returningString += self.parsedFieldDictionary[field] + "\n"

        return returningString

    #Returns a string representing the parsed field
    def parsedField(self,field):

        returningString = ""

        if field in self.parsedFieldDictionary:
            returningString += field + ": "

            if field == "Content":
                contentList = self.parsedFieldDictionary[field]
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
                returningString += self.parsedFieldDictionary[field]

        else:
            returningString += "Field not found"

        return returningString


#Make a default field EmailParser
def DefaultParser():
    return EmailParser({'Subject': 'Subject\s*?:(.*?)\n','Date' : 'Date\s*?:(.*?)\n','From' : 'From\s*?:(.*?)\n','To' : 'To\s*?:(.*?)\n','Content' : '(--.*?)\nContent.*?Type.*?:.*?'})


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
#Get the text from the file, split it and use the regex commands to initialize the parser
EmailParser = DefaultParser()


#Parse the email
i=0
numEmails = len(emailFileNames)
while i < numEmails:
    parsedEmail = EmailParser.parseEmail(emailText[i], emailFileNames[i])
    print(parsedEmail)     
    i+=1