#Classifies links between POIs
import sys      #Functions to increasse recursion depth

DEFAULT_RECURSION=1000;     #Default recursion depth
SAFE_TRHESHOLD=10;          #Algorithm depth before recursion

#Recursive algorithm (Breath first search) to find out if a link P has return. Including unrealistic links
#        Input
#    POIs: List of already evaluated POIs
#    intialPOI: Initial POI of P
#    poi: Current poi to be evaluated  
#    i: Current level of depth
#    recursion: Maximum level of depth
def searchReturnLinkWithU(POIs,intialPOI,poi,i,recursion):
    i+=1;
    for link in poi.links:
        if link.finalPOI == intialPOI:
            link.returnIU=True;
            return True;
        elif (link.finalPOI not in POIs) and (i<recursion):
            POIs.append(poi);
            if searchReturnLinkWithU(POIs,intialPOI,link.finalPOI,i,recursion):
                link.returnIU=True;
                return True;
    return False;

#Find links with return. Including unrealistic links
#        Input
#    POIs: List of places where a user can stay
#    recursion: Maximum level of depth
def searchReturnLinksWithU(POIs,recursion):
    i=1;
    for poi in POIs:
        for link in poi.links:
            if not link.returnIU:
                link.returnIU=searchReturnLinkWithU([],poi,link.finalPOI,i,recursion);

#Recursive algorithm (Breath first search) to find out if a link P has return. Excluding unrealistic links
#        Input
#    POIs: List of already evaluated POIs
#    intialPOI: Initial Location of P
#    poi: Current POI to be evaluated
#    i: Current level of depth
#    recursion: Maximum level of depth
def searchReturnLinkWithoutU(POIs,intialLocation,poi,i,recursion):
    i+=1;
    for link in poi.links:
        if not link.unrealistic:
            if link.finalPOI == intialLocation:
                link.returnEU=True;
                return True;
            elif (link.finalPOI not in POIs) and (i<recursion):
                POIs.append(poi);
                if searchReturnLinkWithoutU(POIs,intialLocation,link.finalPOI,i,recursion):
                    link.returnEU=True;
                    return True;            
    return False;

#Find links with return. Excluding unrealistic links
#        Input
#    POIs: List of places where a user can stay
#    recursion: Maximum level of depth
def searchReturnLinksWithoutU(POIs,recursion):
    i=1;
    for poi in POIs:
        for link in poi.links:
            if not link.unrealistic:
                if not link.returnEU:
                    link.returnEU=searchReturnLinkWithoutU([],poi,link.finalPOI,i,recursion);

#Count the number of links of different type
#        Input
#    POIs: List of places where a user can stay
def countPaths(POIs):
    a=[0,0,0,0];
    for poi in POIs:
        for link in poi.links:            
            if link.returnIU:
                a[0]+=1;
            else:
                a[1]+=1;
            if link.returnEU:
                a[2]+=1;
            else:
                a[3]+=1;
    print 'Including Unrealistic: return links='+str(a[0]);
    print 'Including Unrealistic: non return links='+str(a[1]);
    print 'Excluding Unrealistic: return links='+str(a[2]);
    print 'Excluding Unrealistic: non return links='+str(a[3]);

#Clasify paths
#        Input
#    POIs: List of places where a user can stay
#    recursion: If it is 0 or none it is the size of POIs 
def classifyPaths(POIs,recursion):
    for poi in POIs:
        for link in poi.links:
            link.returnIU=False;
            link.returnEU=False;   
    lenPOIs=len(POIs);
    if recursion == None:
        recursion=lenPOIs;
    else:
        if recursion<=0 or recursion>lenPOIs:
            recursion=lenPOIs;
    sys.setrecursionlimit(recursion+SAFE_TRHESHOLD);
    searchReturnLinksWithoutU(POIs,recursion);
    searchReturnLinksWithU(POIs,recursion);
    sys.setrecursionlimit(DEFAULT_RECURSION);       
    countPaths(POIs);
    