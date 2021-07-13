def hasReturn(link, initial_poi, inc_Unrealistic):
    if (not link.unrealistic) or inc_Unrealistic:
        for reversed_link in link.finalPOI.links:
            if (not reversed_link.unrealistic) or inc_Unrealistic:
                if reversed_link.finalPOI==initial_poi:
                    return True;
    return False;

def findPaths(POIs):
    for poi in POIs:
        for link in poi.links:
            link.returnIU=hasReturn(link, poi, True);
            link.returnEU=hasReturn(link, poi, False);

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
    print('Including Unrealistic: return links='+str(a[0]))
    print('Including Unrealistic: non return links='+str(a[1]))
    print('Excluding Unrealistic: return links='+str(a[2]))
    print('Excluding Unrealistic: non return links='+str(a[3]))

#Clasify paths
#        Input
#    POIs: List of places where a user can stay
#    recursion: If it is 0 or none it is the size of POIs 
def classifyPaths(POIs):
    findPaths(POIs);
    countPaths(POIs);
    