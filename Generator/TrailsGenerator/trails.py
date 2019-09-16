#Functions to generate TRAILS graphs
import os                           #Functions to create directories
import csv                          #Functions to create csv tables
import extraction as e              #Functions to extract locations from traces
import connection as t              #Creates paths between locations
import objects as o                 #Objects to describe TRAIS graphs
from Compare import comd as c       #Comparisson of multiple distances algorithim
import matplotlib.pyplot as plt     #Functions to plot graphs

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

#Export the TRAILS graph into csv files
#        Input
#    outputFolder: Output directory
#    POIs: List of POIs
#    links: List of links
def exportSmartTrails(outputFolder,POIs):
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
        poi=o.POI(None,px,py,stayTimes,i>>1);
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
        returnIU=True if dataList[i][3]=="1" else False;
        returnEU=True if dataList[i][4]=="1" else False;
        timeInterval=[float(ti) for ti in dataList[i+1]];
        xv=[float(x) for x in dataList[i+2]];
        yv=[float(x) for x in dataList[i+3]];
        link=o.Link(xv,yv,timeInterval,finalPOI,initialPOI,unrealistic,returnIU,returnEU);
        initialPOI.links.append(link);

#Creates arrows in the paths to describe direction
#        Input
#    ax: Subplot
#    line: Ploted path
#    arrsize: Size of the arrow
def createArrow(ax,line,arrsize):
    arx=line[0].get_xdata()[len(line[0].get_xdata())//2-1];
    ary=line[0].get_ydata()[len(line[0].get_ydata())//2-1];
    ardx=line[0].get_xdata()[len(line[0].get_xdata())//2]-arx+PLOTDELTA;
    ardy=line[0].get_ydata()[len(line[0].get_ydata())//2]-ary+PLOTDELTA;
    ax.arrow(arx,ary,ardx,ardy,shape='full',lw=0,length_includes_head=True,head_width=arrsize,color=line[0].get_color());

#Plot the TRAILS graph and save it as pdf
#        Input
#    POIs: List of locations with paths (Complete TRAILS graph)
#    plotP: Plot parameters
#    incNoReturn: Flag to include non links with no return
#    incUnrealistic: Flag to include unrealistic paths
#    output: Output directory to export the plot
def plotFigure(POIs,plotP,incNoReturn,incUnrealistic,output):
    fig = plt.figure();
    ax = fig.add_subplot(111);
    plotLocations=[];
    for poi in POIs:
        plotLocation=[poi.px,poi.py,False];
        for link in poi.links:
            cyclic=link.returnIU if incUnrealistic else link.returnEU;
            if incUnrealistic or not link.unrealistic:
                if incNoReturn or cyclic:
                    link.x.insert(0,link.initialPOI.px);
                    link.y.insert(0,link.initialPOI.py);
                    link.x.append(link.finalPOI.px);
                    link.y.append(link.finalPOI.py);
                    line=ax.plot(link.x,link.y, linewidth=plotP.lineWidth);
                    createArrow(ax,line,plotP.arrowSize);        
                    if not cyclic:
                        line=ax.plot(link.x[::-1],link.y[::-1], linewidth=plotP.lineWidth);
                        createArrow(ax,line,plotP.arrowSize);
                    plotLocation[2]=True;
        if plotLocation[2]:
            plotLocations.append(plotLocation);
    centerX = [plotPOI[0] for plotPOI in plotLocations];
    centerY = [plotPOI[1] for plotPOI in plotLocations];
    ax.scatter(centerX,centerY,marker='o',color='b',s=plotP.POISize);
    ax.axis('equal');
    ax.set_ylim(ax.get_ylim()[::-1]);        # invert the axis
    ax.xaxis.tick_top();                     # and move the X-Axis      
    if output != None:
        fig.savefig(output, format='pdf',dpi=plotP.dpi,figsize=plotP.fSize);
        plt.close(fig);
    else:
        plt.show();       