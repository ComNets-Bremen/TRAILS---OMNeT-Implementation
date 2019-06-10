#Functions to generate TRAILS graphs
import os                           #Functions to create directories
import csv                          #Functions to create csv tables
import objects as o

PLOTDELTA = 10**-6; #Constant used to plot arrows

#Export the TRAILS graph into csv files
#        Input
#    outputFolder: Output directory
#    POIs: List of POIs
#    links: List of links
def exportTrails(outputFolder,POIs):
    for i in xrange(0,len(POIs)):
        POIs[i].pindex=i;
    TRAILSpath = outputFolder+'/SmartTRAILS';
    if not os.path.exists(TRAILSpath):
        os.makedirs(TRAILSpath);
    with open(TRAILSpath+'/POIs.csv', 'wb') as f:
        writer = csv.writer(f, delimiter =' ');
        for poi in POIs:
            writer.writerow([poi.px,poi.py]);
            writer.writerow(poi.stayTimes);
    with open(TRAILSpath+'/Links.csv', 'wb') as f:
        writer = csv.writer(f, delimiter =' ');
        for poi in POIs:
            for link in poi.links:
                initialPOI=link.initialPOI.pIndex;
                finalPOI=link.finalPOI.pIndex;
                unrealistic=1 if link.unrealistic else 0;
                returnIU=1 if link.returnIU else 0;
                returnEU=1 if link.returnEU else 0;                
                writer.writerow([initialPOI,finalPOI,unrealistic,returnIU,returnEU]);
                writer.writerow(link.timeInterval);
                writer.writerow(link.x);
                writer.writerow(link.y);

#Process to import POIs
#        Input
#    inFolder: Input folder where the traces are saved
def importPOIs(inFolder):
    POIs=[];
    csvdelimeter = " ";
    reader = csv.reader(open(inFolder+"/POIs.csv", "rb"), delimiter=csvdelimeter);
    dataList=list(reader);
    for i in xrange(0,len(dataList),2):
        px=float(dataList[i][0]);
        py=float(dataList[i][1]);
        stayTimes=[float(stayTime) for stayTime in dataList[i+1]];
        poi=o.POI(px,py,stayTimes,i>>1)
        POIs.append(poi);
    return POIs;

#Process to import Links
#        Input
#    inFolder: Input folder where the traces are saved
#    POIs: List of points of interest
def importLinks(inFolder,POIs):
    csvdelimeter = " ";
    reader = csv.reader(open(inFolder+"/Links.csv", "rb"), delimiter=csvdelimeter);
    dataList=list(reader);
    for i in xrange(0,len(dataList),4):
        initialPOI=POIs[int(dataList[i][0])];
        finalPOI=POIs[int(dataList[i][1])];
        unrealistic=True if dataList[i][2]=="1" else False;
        timeInterval=[float(ti) for ti in dataList[i+1]];
        xv=[float(x) for x in dataList[i+2]];
        yv=[float(x) for x in dataList[i+3]];
        link=o.Link(xv,yv,timeInterval,finalPOI,initialPOI,unrealistic,False,False);
        initialPOI.links.append(link);