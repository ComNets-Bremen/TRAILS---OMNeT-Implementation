#Functions to generate TRAILS graphs
import os                           #Functions to create directories
import csv                          #Functions to create csv tables
import extraction as e              #Functions to extract locations from traces
import connection as t              #Creates paths between locations
from Compare import comd as c       #Comparisson of multiple distances algorithim

PLOTDELTA = 10**-6; #Constant used to plot arrows

# Generate the elements of the TRAILS graph
#        Input
#    users: List of users traces
#    SR:Spatial range used to group trace-points and POIs
#    TR:Temporal range, minimum time for a POI
#    MinU:Break distance, Minimum distance to identify an unrealistic path
#    maxX: Width of traces area
#    maxY: Length of the traces area
#        Output
#    locations: List of locations with paths (Complete TRAILS graph)
def getTrails(users,SR,TR,MinU,maxX,maxY):
    SRe=c.Threshold(SR);                                        #Spatial range and its equivalents
    Sre=c.Threshold((1.0*SR)/2);                                #Spatial radius and its equivalents
    POIs=e.extractPOIs(users,SRe,Sre,TR,maxX,maxY);   #Generate TRAILS locations from traces
    for poi in POIs:                                                    
        poi.stayTimes=[stp.stayTime for stp in poi.listSTP];    #Get stay intervals for each POI
    links=t.getLinks(users,POIs);                               #Get connected locations with links
    t.classifyLinks(links,MinU);                                #Classify paths cyclic/unrealistic
    POIs=t.getConnectedPOIs(links)                              #Remove POIs that do not belog to any link
    return POIs,links;

#Export the TRAILS graph into csv files
#        Input
#    outputFolder: Output directory
#    POIs: List of POIs
#    links: List of links
def exportTrails(outputFolder,POIs,links):
    for i in xrange(0,len(POIs)):
        POIs[i].pindex=i;
    TRAILSpath = outputFolder+'/TRAILS';
    if not os.path.exists(TRAILSpath):
        os.makedirs(TRAILSpath);
    with open(TRAILSpath+'/POIs.csv', 'wb') as f:
        writer = csv.writer(f, delimiter =' ');
        for poi in POIs:
            writer.writerow([poi.px,poi.py]);
            writer.writerow(poi.stayTimes);
    with open(TRAILSpath+'/Links.csv', 'wb') as f:
        writer = csv.writer(f, delimiter =' ');
        for link in links:
            initialPOI=link.initialPOI.pIndex;
            finalPOI=link.finalPOI.pIndex;
            unrealistic=1 if link.unrealistic else 0;
            writer.writerow([initialPOI,finalPOI,unrealistic,1,1]);
            writer.writerow(link.timeInterval);
            writer.writerow(link.x);
            writer.writerow(link.y);