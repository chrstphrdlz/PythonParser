"""
Christopher Deleuze
This program will parse through a raw email text file and search through the following lists to loof for the following fields,
extracting the information following it. The main function is at the bottom.
"""
recipientString = ["Delivered-To:","To:","To"]
senderString = ["Received: from", "From:","From"]
subjectString = ["Subject:","Subject"]
dateString = ["Date:","Date"]

#If the works appear, in order that they are found in the input list
#will return either the next word, or line (depending on returnEntireLine)
def getInfo(keyWord,line, returnEntireLine):

    #Keeps track of if the feild is found
    foundFeild = False

    #Checks for feilds among a list of strings
    for i in keyWord :

        #if the beginning is the same
        if i == line[0:len(i)]:

            #Set the boolean as true        
            foundFeild = True

            #Remove the string from the line
            line = line[len(i)+1:]

            #Stop searching
            break

    #If it is found
    if foundFeild:

        #if returning the whole line, make the returner the rest of the line
        if returnEntireLine :
            returnLine = line
        #If not, make it the first word
        else:
            returnLine = line.split()[0]

    #If not found, make returning string ""
    else:
        returnLine = ""

    #This removes the ending newline if there is one
    if not returnLine == "":

        returnLine=returnLine.replace("\n","")
    
    #Return the result
    return returnLine

#Will have to continue if the line starts with a space
def continuesInfo(line):
    return line!="" and (line[0]==" " or line[0] == "\t")

def checkAndParseLine(line,checkingWordList,readToEndOfLine,mappingString):
    global file
    global dictionary
    #print(dictionary)
    subject = getInfo(checkingWordList,line, readToEndOfLine)

    #If not "", found matching case
    
    if subject != "":
        
        #store matching case
        dictionary[mappingString] =  subject
          
        #Read in next line
        if readToEndOfLine:

            '''Saves the file position. Does so after ever iteration
            This is because once a line is found that does NOT continue the feild,
            we will return the file to the previous state for parseing for the other feilds'''
            previous_position = file.tell()
            
            line = file.readline()

           
            #Subject can continue to next line, so we check for that
            while continuesInfo(line) :

                #Removes previous newline
                dictionary[mappingString] = dictionary[mappingString][0:len(dictionary[mappingString])-1]

                #Adds the next scanned line to the entry, without the newline
                dictionary[mappingString]+=line.replace("\n","")

                #Saves the file position
                previous_position = file.tell()
                
                #updates the line
                line = file.readline()

        file.seek(previous_position)
        
        return True
    
    
    return False
            
def parse_email():

    global file
    
    global dictionary
    dictionary = {}
    
    line = file.readline()

    #Will read through each line in the file, and check for field information
    while line != "":
        
        if checkAndParseLine(line,senderString,True,"Sender:"):
            line = file.readline()
            continue

        if checkAndParseLine(line,subjectString,True,"Subject:") :
            line = file.readline()
            continue
    
        if checkAndParseLine(line,recipientString,True,"Recipient:"):
            line = file.readline()
            continue
        
        if checkAndParseLine(line,dateString,True,"Date:"):
            line = file.readline()
            continue

        #If none found, update line
        line = file.readline();    
        
    return




#This is the main running function
#declare the file as global, get the path, and open the file
global file

filestring = input("Please give the path of the text file\n")

file= open (filestring,"r")

#declare the dictionary as global, and parse the email
global dictionary

parse_email()

#print the result
for entry in dictionary:
    print  (entry+" "+dictionary[entry])

    

    
