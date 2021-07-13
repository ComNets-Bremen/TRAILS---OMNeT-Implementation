#Objects used as structures for the TRAILS graph generator
#Cartesean coordinate
class Point(object):
    def __init__(self,x,y):
        self.x=1.0*x;
        self.y=1.0*y;

class STP(object):
    def __init__(self,user,pointsIndex,enterTime,exitTime):
        self.user=user;                     #Trace user owner of the trace-points
        self.pointsIndex=pointsIndex;       #Identifier of the trace-points
        self.enterTime=enterTime;           #Time it arrives to the POI
        self.exitTime=exitTime;             #Time it leaves the POI
        self.stayTime=exitTime-enterTime;   #Time interval
        self.px=None;                       #Position in X
        self.py=None;                       #Position in Y
#Points of interest
class POI(object): 
    def __init__(self,ListSTP,px,py,stayTimes,pIndex):
        self.listSTP=ListSTP;       #List of Sets of trace points that are located within a range SR
        self.px=px;                 #Position in X
        self.py=py;                 #Position in Y
        self.pIndex=pIndex;         #POI Identifier 
        self.stayTimes=stayTimes;   #List of times that a user spends
        self.enterTimes=[];         #List of times a user arrives to a node
        self.links=[];              #List of links that has this POI as initalPOI
        self.congestion=[];         #List of number of hosts at different moments of time

#Track between locations
class Link(object):
    def __init__(self,x,y,timeInterval,totalTime,finalPOI,initialPOI):
        self.x=x;                       #list of X components of path-points
        self.y=y;                       #list of Y components of path-points
        self.timeInterval=timeInterval; #list of time intervals between path-points
        self.totalTime=totalTime;       #Time toarrive to a new POI
        self.enterTime=0;               #Time a user took that link
        self.finalPOI=finalPOI;         #POI that belogns to the final location
        self.initialPOI=initialPOI;     #POI that belongs to the initial location
        self.unrealistic=False;   #Flag to indicate unrealistic links
        self.returnIU=False;         #Flag to indicate return links including unrealistic
        self.returnEU=False;         #Flag to indicate return links excluding unrealistic links
#Enclosing object in the shape of a circle
class Circle(object):   
    def __init__(self,centerX,centerY,squareRadius): #Shape (centerX-x)^2+(centerY-y)^2=squareRadius
        self.centerX=1.0*centerX;
        self.centerY=1.0*centerY;
        self.squareRadius=1.0*squareRadius;

#Enclosing object in the shape of a rectangle        
class Box(object):  
    def __init__(self,minX,minY,maxX,maxY): #Coordinates [[minX,minY],[minX,maxY],[maxX,maxY],[maxX,minY]]
        self.minX=minX;
        self.minY=minY;
        self.maxX=maxX;
        self.maxY=maxY;
        