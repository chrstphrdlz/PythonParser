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

    def __init__(self):
        #Fields map to corresponding regex search strings
        self.regexSearchDictionary = {'Subject': 'Subject\s*?:(.*?)\n\S',
        'Date' : 'Date\s*?:(.*?)\n\S','From' : 'From\s*?:(.*?)\n\S',
        'To' : 'To\s*?:(.*?)\n\S',
        'Content' : '--.*?\n(Content.*?Type.*?:.*?)(--.*--)',
        'Cc': 'Cc\s*?:(.*?)\n\S','Bcc': 'Bcc\s*?:(.*?)\n\S'}

    #Finds string matched by the EmailParser's regexStrings 
    #and stores the results in a seperate dictionary
    #Returns a ParsedEmail object made from the resulting dictionary
    def parseEmail(self, text, emailName):
        ParsedFieldDictionary = {}

        for expression in self.regexSearchDictionary:
            #Get all matches and store it as a list in result
            result = re.findall(self.regexSearchDictionary[expression], text, re.DOTALL)

            if len(result) > 0:
                #If it is the content, store the entire list
                #If not, just store the first match
                if(expression != 'Content'):
                    result = result[0]
                else:
                    result = list(result[0])

                ParsedFieldDictionary[expression] = result

        return ParsedEmail(ParsedFieldDictionary,emailName)


#Parsed email class, can print to display all parsed fields, or select a field to print
class ParsedEmail:
    #Has a dictionary mapping fields to the found strings
    #The content is mapped to a list of the separate multiple content sections
    def __init__(self, dictionary, emailName):
        self.emailName = emailName
        self.ParsedFieldDictionary = dictionary

    #Prints out the name and the found fields
    def __str__(self):
        returningString = "Parsed email: " + self.emailName + "\n"

        for field in self.ParsedFieldDictionary:
            #Print Content last
            if field != "Content":
                returningString += self.getParsedField(field) + "\n"

        if "Content" in self.ParsedFieldDictionary:
            returningString += self.getParsedField("Content") + "\n"

        return returningString

    #Returns a string representing the parsed field
    def getParsedField(self,field):

        returningString = ""
        returningString += field + ": "

        if field in self.ParsedFieldDictionary:

            if field == "Content":


                contentList = self.ParsedFieldDictionary[field]
                if len(contentList) > 1:
                    returningString += "There are multiple content sections\n"
                    for contentSection in contentList:
                        returningString += "\nContent section " + str(contentList.index(contentSection)+1) + \
                        "\n" + contentSection + "\n\n"
                else:
                    returningString += contentList[0] + "\n"

            else:
                returningString += self.ParsedFieldDictionary[field]
        else:
            returningString += "Field not found"

        return returningString


def getTextFromFile(fileString):
    try:
        file = open(fileString,"r")

    except  IOError:
        print("Could not open " + fileString + ". File does not exist")
        return ""

    fileText = file.read()

    return fileText
    

#Main running function
#If arguments improperly used
if len(sys.argv) < 2 :
    print("\n\nusage: python EmailParser.py [email/text/document/path(s)] \n")
    sys.exit()

emailText = []
emailFileNames = sys.argv[1:]

#Get file text and add to the list of emailText
for emailName in emailFileNames:
    string = getTextFromFile(emailName)    
    emailText.append(string)

#Create an email parser
emailParser = EmailParser()

#Parse the email
i=0
numEmails = len(emailFileNames)
while i < numEmails:
    parsedEmail = emailParser.parseEmail(emailText[i], emailFileNames[i])     
    print(parsedEmail)
    i+=1