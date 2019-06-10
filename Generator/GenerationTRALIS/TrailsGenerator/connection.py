#Creates paths between locations
import objects as o             #Objets used as structures for the TRAILS graph generator
from Compare import comd as c   #Comparisson of multiple distances algorithim

#Find out if a path is an unrealistic path
#        Input
#    link: Set of points connecting 2 locations
#    BDe: Threshold eucledean distance (BD) to clasify as unrealistic path with its equivalents
def isUnknown(link,BDe):
    tx=[x for x in link.x];
    tx.insert(0,link.initialPOI.px);
    tx.append(link.finalPOI.px);
    ty=[y for y in link.y];
    ty.insert(0,link.initialPOI.py);
    ty.append(link.finalPOI.py);
    for i in xrange(1,len(tx)):
        dx=abs(tx[i]-tx[i-1]);
        dy=abs(ty[i]-ty[i-1]);
        if not c.isInRange(dx,dy,BDe):
            return True;
    return False;

#Find unrealistic paths
#        Input
#    locations: List of places where a user can stay
#    BDe: Threshold eucledean distance (BD) to clasify as unrealistic path with its equivalents
def findUnknown(links,BDe):
    a=0;
    for link in links:
        link.unrealistic=isUnknown(link,BDe);
        if link.unrealistic:
            a+=1;
    print "Unrealistic links="+str(a);

#Compute time intrvals between consecutive time stamps
#        Input
#    time: List of time stamps
#        Output
#    deltaTime: List of time intervals
def getDeltaTime(time):
    deltaTime=[time[i+1]-time[i] for i in xrange(0,len(time)-1)];
    return deltaTime;

#Get input and output ports for each POI
#        Input
#    POIs: list of Places in which a user spends part of its time
def getPorts(POIs):
    for poi in POIs:
        for stp in poi.listSTP:
            stp.user.inputPort[stp.pointsIndex[0]]=poi;
            stp.user.outputPort[stp.pointsIndex[-1]]=poi;

#Get connected locations with paths
#        Input
#    users: List of users traces
#    POIs: list of Places in which a user spends part of its time
#        Output
#    links: List of links
def getLinks(users,POIs):
    links=[];
    getPorts(POIs);   #Get input and output ports for each POI
    for user in users:       
        outputIndexes=[index for index in range(len(user.outputPort)) if user.outputPort[index] is not None];
        inputIndexes=[index for index in range(len(user.inputPort)) if user.inputPort[index] is not None];
        for i in xrange(0,len(outputIndexes)-1):
            x=user.x[outputIndexes[i]+1:inputIndexes[i+1]];
            y=user.y[outputIndexes[i]+1:inputIndexes[i+1]];
            finalPOI=user.inputPort[inputIndexes[i+1]];
            initialPOI=user.outputPort[outputIndexes[i]];
            deltaTime=getDeltaTime(user.time[outputIndexes[i]:inputIndexes[i+1]+1]);
            link=o.Link(x,y,deltaTime,finalPOI,initialPOI);
            links.append(link);
    return links;

#Clasify links unrealistic
#        Input
#    POIs: List of places where a user can stay
#    MinU: Break distance, Minimum distance to identify an unrealistic path
def classifyLinks(links,MinU):
    if MinU != None:
        if MinU>0:
            breakDistance=c.Threshold(MinU);
            findUnknown(links,breakDistance);

#Remove locations that do not belog to any path
#        Input
#    POIs: list of Places in which a user spends part of its time
#        Output
#    newPOIs: locations with paths
def getConnectedPOIs(links):
    newPOIs=[];
    i=0;
    for link in links:
        if link.initialPOI.pIndex==None:
            link.initialPOI.pIndex=i;
            newPOIs.append(link.initialPOI);
            i+=1;
        if link.finalPOI.pIndex==None:
            link.finalPOI.pIndex=i;
            newPOIs.append(link.finalPOI);
            i+=1;
    print 'POIs with paths='+str(i);
    return newPOIs;
    