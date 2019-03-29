import os
import re
import json

# Taking directory path from user (Default: etc\passwd)
passwdDirectoryPath = str(input("Enter the path to the directory containing passwd (Press Enter to use system default path)")) or "/etc"
passwdFilePath = passwdDirectoryPath+'/passwd'
groupDirectoryPath = str(input("Enter the path to the directory containing group (Press Enter to use system default path)")) or "/etc"
groupFilePath = groupDirectoryPath+'/group'

outputFilePath = str(input("Enter the path to the directory for saving the output (Press enter to save in the same working directory)"))  or str(os.getcwd()) 
textFile = open(outputFilePath+'/'+"json.txt","w+")


# Checking the availability and loading the files
if os.path.isfile(passwdFilePath):
    passwdData = open(passwdFilePath, "r")
else:
    print ("passwd file is not available in " + str(passwdDirectoryPath)+"Directory")
    quit()
if os.path.isfile(groupFilePath):
    groupData = open(groupFilePath, "r")
else:
    print ("group file is not available in " + str(groupDirectoryPath)+"Directory")
    quit()

# Defining lists to store values form /etc/passwd and /etc/group files
userName = []
UID = []
fullName = []
groupName = []
groupMembers = []

# Saving userNames, UIDs and full names into different lists
for lines in passwdData:
    line = lines.split(":")
    userName.append(line[0])
    UID.append(line[2])
    # Removing phone number and email address from the user info
    userInfo = line[4]
    email = re.findall('\S+@\S+',userInfo)
    phoneNumber = re.findall(r'[0-9]+', userInfo)
    
    if len(email) or len(phoneNumber) is not 0:
        for i in range(len(email)):
            userInfo = userInfo.replace(str(email[i]), '')
        for i in range(len(phoneNumber)):
            userInfo = userInfo.replace(str(phoneNumber[i]), '')
       
    fullName.append(userInfo)

# Storing group names and group members into different lists
for lines in groupData:
    line = lines.split(":")
    groupName.append(line[0])
    usersInGroup = line[3].strip('\n').strip().split(",")
    temp = []
    for n in range(len(usersInGroup)):
        temp.append(usersInGroup[n])
    groupMembers.append(temp)


jsonDictionary = {}  # dictionary to load into json

# Storing values into jsonDictionary
for i in range(len(userName)):
    temp_group = []
    # Finding groups in which the user is a member
    for j in range(len(groupMembers)):
        if userName[i] in groupMembers[j]:
            temp_group.append(groupName[j])
    jsonDictionary.update({str(userName[i]): {"uid":str(UID[i]),"groups":temp_group,"full_name":str(fullName[i])}})

# Dumping the dictionary into a json
jsonOutput=json.dumps(jsonDictionary, indent = 4)
textFile.write(jsonOutput)
textFile.close()
print (jsonOutput)



