#Objects used as structures for the TRAILS graph generator
#Points of interest
class POI(object): 
    def __init__(self,px,py,stayTimes):
        self.px=px;                 #Position in X
        self.py=py;                 #Position in Y
        self.stayTimes=stayTimes;   #List of times that a user spends
        self.links=[];              #List of links that has this POI as initalPOI

#Track between locations
class Link(object):
    def __init__(self,x,y,timeInterval,finalPOI,initialPOI,unrealistic,returnIU,returnEU):
        self.x=x;                       #list of X components of path-points
        self.y=y;                       #list of Y components of path-points
        self.timeInterval=timeInterval; #list of time intervals between path-points
        self.finalPOI=finalPOI;         #POI that belogns to the final location
        self.initialPOI=initialPOI;     #POI that belongs to the initial location
        self.unrealistic=unrealistic;   #Flag to indicate unrealistic links
        self.returnIU=returnIU;         #Flag to indicate return links including unrealistic
        self.returnEU=returnEU;         #Flag to indicate unrealistic links