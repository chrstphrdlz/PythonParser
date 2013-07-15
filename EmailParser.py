"""
Christopher Deleuze
This program will get the email text string and parse through it line by line.
If it is continuing a subject, it will continue adding it, if not it will make a new entry for the subject
It checks for fields by parsing through a list of strings accociated with those subjects, 
adding the characters after the string to the feild (if it is a feild)
The main running function is at the bottom
"""

#These feilds can be expanded to include more options
recipientList = ["Delivered-To:","To:","To"]
senderList = ["Received: from", "From:","From"]
subjectList = ["Subject:","Subject"]
dateList = ["Date:","Date"]

AllFeilds = [dateList, senderList,subjectList,recipientList]

feildStrings = ["Date: ", "Sender: ", "Subject: ", "Recipient: "]

#Gets the word list from the index of feildType
def getWordList(feildType):

    return AllFeilds[feildType]

#The enums for feilds
class FieldEnum:
    DATE = 0
    SENDER = 1
    SUBJECT = 2
    RECIPIENT = 3
    NOTHING = 4


#The main parsing function       
def parse_email():

    #Shares the gloabl file and dictionary
    global file
    
    global dictionary

    #Initialize the dictionary
    dictionary = {}

    #Reads the file into a giant string
    fileString = file.read()

    #Splits it up by newline characters
    fileString = fileString.split("\n")
    
    #Initializes the feild type as nothing
    feildType = FieldEnum.NOTHING

    #Will read through each line in the file, and check for field information
    for line in fileString:
        
        #If it continues, add the line to the dictionary feild
        if continuesInfo(line):

            continueFeild(feildType,line)     

        #If not, get the feild and make a new entry for the dictionary
        else:

            feildType = getFeildType(line)

            addToFeild(feildType,line)

    return


#Will have to continue if the line starts with a space (the feild is not finished)
def continuesInfo(line):
    return line!="" and (line[0]==" " or line[0] == "\t")


#Will get the feild type of the line
def getFeildType(line):
    i = 0

    while i < len(AllFeilds):

        if isOfType(AllFeilds[i],line):

            return i

        i+=1

    return 4


def isOfType(keyWord,line):

    #Checks for feilds among a list of strings
    for i in keyWord :

        #If the beginning is the same as one of the entries
        if i == line[0:len(i)]:

            return True

    return False


#Make the line (without the initial string) to the dictionary entry for it
def addToFeild(feildType,line):

    global dictionary

    if feildType == FieldEnum.NOTHING:
        return 

    dictionary[feildStrings[feildType]] = line[len(feildStrings[feildType]):]


    return

#Add the line (without the initial string) to the dictionary entry for it
def continueFeild(feildType,line):

    global dictionary

    if feildType == FieldEnum.NOTHING:
        return 

    dictionary[feildStrings[feildType]] += line[len(feildStrings[feildType]):]


    return


#This is the main running function

#Get the path, and open the file
filestring = input("Please give the path of the text file\n")

file = open (filestring,"r")

#Parse the email
parse_email()

#Print the result
for entry in dictionary:
    print  (entry+" "+dictionary[entry])    
