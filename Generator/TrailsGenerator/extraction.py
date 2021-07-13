#Functions to extract locations from traces
from TrailsGenerator import objects as o             #Objets used as structures for the TRAILS graph generator
from TrailsGenerator import smallestcircle as c      #Group objects by the Smallest enclosing cicle
from Compare import comd as d   #Comparisson of multiple distances algorithim
import math as m                #Mathematic functions

#Group trace-points in a STP given a POI
#        Input
#    index: identifier of the first trace-point in the POI
#    user: user's trace where the trace-point tp[index] belongs
#    poi: Place in which a user spends part of its time
#    SRe: Spatial range and its equivalents
#    TR:Temporal range, minimum time for a POI
#        Output
#    POI: Point of interest
def findSTP(index,user,poi,Sre,TR):
    pointsIndex=[index];
    for j in range(index,len(user.x)):
        point=o.Point(user.x[j],user.y[j]);
        dx=abs(poi.px-point.x);
        dy=abs(poi.py-point.y);
        if d.isInRange(dx,dy,Sre):
            pointsIndex.append(j);
        else:
            stayTime=user.time[pointsIndex[-1]]-user.time[pointsIndex[0]];
            if stayTime >= TR:
                return o.STP(user,pointsIndex,user.time[pointsIndex[0]],user.time[pointsIndex[-1]]);
            else:
                return None;            
    return None

#Find the POI where the STP belongs
#        Input
#    index: identifier of the first trace-point in the POI
#    user: user's trace where the trace-point tp[index] belongs
#    grid: Grid with locations
#    Sre: Spatial radius (SR/2) and its equivalents
#    TR:Temporal range, minimum time for a POI
#        Output
#    POI: Place in which a user spends part of its time
def findPOI(index,user,grid,Sre,TR):
    resolution=Sre.range;
    point=o.Point(user.x[index],user.y[index]);
    i=int(m.floor(point.x/resolution));
    j=int(m.floor(point.y/resolution));
    lowI=i-1 if i>0 else 0;
    highI=i+1 if i<len(grid)-1 else len(grid)-1;
    lowJ=j-1 if j>0 else 0;
    highJ=j+1 if j<len(grid[i])-1 else len(grid[i])-1;
    for I in range(lowI,highI+1):
        for J in range(lowJ,highJ+1):       
            for poi in grid[I][J]:
                stp=findSTP(index,user,poi,Sre,TR);
                if stp != None:
                    poi.listSTP.append(stp);
                    return stp;        
    return None;

#Create a POI
#        Input
#    grid: Grid with POIs
#    POIs: List of points of interest
#    Sre: Spatial radius (SR/2) and its equivalents
#    stp: Set of consecutive trace-points
def createPOI(grid,POIs,Sre,stp):
    poi=o.POI([stp],stp.px,stp.py,None,None);
    POIs.append(poi);
    resolution=Sre.range;
    i=int(m.floor(stp.px/resolution));
    j=int(m.floor(stp.py/resolution));
    grid[i][j].append(poi);
  
#Find a STP that belongs to a POI
#        Input
#    index: identifier of the first trace-point in the search cycle
#    iopt: Last Index of point of stp
#    TR:Temporal range, minimum time for a POI
#    user: user's trace
#    grid: Grid with locations
#    Sre: Spatial radius (SR/2) and its equivalents
#    lenUser: Size of trace array
#        Output
#    stp: Set of consecutive trace-points
#    iopt: Index of point whe time between point[index] is bigger than TR
def getPOI(index,iopt,TR,user,grid,Sre,lenUser):
    for i in range(index,lenUser):
        if i>iopt:
            return None;
        stp=findPOI(i,user,grid,Sre,TR);
        if stp != None:
            return stp;
    return None;

#Defines a grid that covers all the area of a Traces graph
#The size of a cell is MxM, where M is the spatial range (SR) over 2
#        Input
#    maxX: Width of traces area
#    maxY: Length of the traces area
#    Sre: Spatial range (SR/2) and its equivalents
#        Output
#    grid: NCL grid with locations
def createGrid(maxX,maxY,Sre):
    resolution=Sre.range;
    xResolution=int(m.floor(maxX/resolution))+1;
    yResolution=int(m.floor(maxY/resolution))+1;
    grid=[[[] for j in range(0,yResolution)] for i in range(0,xResolution)];
    return grid;

#Generate TRAILS locations from traces
#        Input
#    users: List of users traces
#    SRe: Spatial range (SR) and its equivalents
#    Sre: Spatial radius (SR/2) and its equivalents
#    TR:Temporal range, minimum time for a POI
#    maxX: Width of traces area
#    maxY: Length of the traces area
#        Output
#    Pois: list of Places in which a user spends part of its time
def extractPOIs(users,SRe,Sre,TR,maxX,maxY):
    POIs=[];
    grid=createGrid(maxX,maxY,Sre);
    for user in users:
        index=0;
        lenUser=len(user.x);
        while index<lenUser:
            nSTP=c.getSTP(user,index,SRe,Sre,TR);
            if nSTP != None:
                aSTP=getPOI(index,nSTP.pointsIndex[-1],TR,user,grid,Sre,lenUser);
                if aSTP != None:
                    index=aSTP.pointsIndex[-1];
                else:
                    createPOI(grid,POIs,Sre,nSTP);
                    index=nSTP.pointsIndex[-1];
            index+=1;
    print('Extracted POIs='+str(len(POIs)))
    return POIs;
