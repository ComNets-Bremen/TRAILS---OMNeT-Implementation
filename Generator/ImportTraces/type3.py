#Functions to import traces of a specific format
#Omnet++ output coordinates
from ImportTraces import users as u   #Functions to process traces

def findUser(userIndex,data,beg):
    searchStr='mobileHost['+str(userIndex)+'],coordX:vector,,,,"'
    intBeg=data.find(searchStr, beg[0])
    if intBeg>-1:
        beg[0]=data.find(searchStr, beg[0])+len(searchStr)
        return True
    return False

def getTime(data,beg):
    intBeg=beg[0]
    intEnd=data.find('"', intBeg)
    beg[0]=intEnd
    return [float(l) for l in data[intBeg:intEnd].split(" ")]

def getX(data,beg):
    intBeg=beg[0]+3
    intEnd=data.find('"', intBeg)
    beg[0]=intEnd
    return [float(l) for l in data[intBeg:intEnd].split(" ")]

def getY(data,beg):
    searchStr='coordY:vector,,,,"'
    intBeg=data.find(searchStr, beg[0])+len(searchStr)
    intBeg=data.find(',', intBeg)+2
    intEnd=data.find('"', intBeg)
    beg[0]=intEnd
    return [float(l) for l in data[intBeg:intEnd].split(" ")]

#Process to import traces
#        Input
#    inFile: Input file where the traces are described
def importUsers(inFile):
    users=[]
    with open(inFile, 'r') as file:
        data = file.read().replace('\n', ' ')
    i=0
    beg=[0]
    while True:
        if not(findUser(i,data,beg)):
            break;
        time = getTime(data,beg)
        x = getX(data,beg)
        y = getY(data,beg)
        users.append(u.User(time,x,y))
        i+=1
    return users
