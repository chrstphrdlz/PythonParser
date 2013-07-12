"""
Christopher Deleuze
This program will parse through a raw email text file and search through the following lists to look for the following fields,
extracting the information following it. The main function is at the bottom.
It works by sharing a global file and reading in line by line into chechAndParseLine
If the information is found at the beginning of the line, it will continue to read lines until
a terminating condition is satisfied. It will then return the file to the previous condition so
a different feild may be searched for.
"""

#These feilds can be expanded to include more options
recipientList = ["Delivered-To:","To:","To"]
senderList = ["Received: from", "From:","From"]
subjectList = ["Subject:","Subject"]
dateList = ["Date:","Date"]

AllFeilds = [recipientList,senderList,subjectList,dateList]





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








#Will have to continue if the line starts with a space (the feild is not finished)
def continuesInfo(line):
    return line!="" and (line[0]==" " or line[0] == "\t")









"""
Will check each input line for relevent information, returning an empty string if not
initially found. If it is found, it will continue reading lines until a terminating condition
is found. It will then return the file to the position directly after
the information was extracted
"""
def checkAndParseLine(line,checkingWordList,readToEndOfLine,mappingString):
    global file
    global dictionary
    
    subject = getInfo(checkingWordList,line, readToEndOfLine)

    #If not "", found matching case
    
    if subject != "":
        
        #Store matching case
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
                
                #Updates the line
                line = file.readline()


            #Returns file to previous position (so it may be checked for feilds)
            file.seek(previous_position)
        
        return True
    
    
    return False









#The main parsing function       
def parse_email():

    #Shares the gloabl file and dictionary
    global file
    
    global dictionary

    #Initialize the dictionary
    dictionary = {}

    #Initially reads a line
    line = file.readline()

    #Will read through each line in the file, and check for field information
    while line != "":
        
        if checkAndParseLine(line,senderList,True,"Sender:"):
            line = file.readline()
            continue

        if checkAndParseLine(line,subjectList,True,"Subject:") :
            line = file.readline()
            continue
    
        if checkAndParseLine(line,recipientList,True,"Recipient:"):
            line = file.readline()
            continue
        
        if checkAndParseLine(line,dateList,True,"Date:"):
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

    

    
