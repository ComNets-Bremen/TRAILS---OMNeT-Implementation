#Functions to generate TRAILS graphs
import os                                                   #Functions to create directories
import csv                                                  #Functions to create csv tables
from TrailsGenerator import extraction as e                 #Functions to extract locations from traces
from TrailsGenerator import connection as t                 #Creates paths between locations
from TrailsGenerator import objects as o                    #Objects to describe TRAIS graphs
from Compare import comd as c                               #Comparisson of multiple distances algorithim
import matplotlib.pyplot as plt                             #Functions to plot graphs

PLOTDELTA = 10**-6;                                         #Constant used to plot arrows

def orderCongestion(POIs):
    for poi in POIs:
        poi.congestion.sort(key=lambda elem:elem[0]);

def orderStays(POIs):
    for poi in POIs:
        z=list(zip(poi.enterTimes,poi.stayTimes))
        z.sort(key=lambda elem:elem[0]);
        poi.enterTimes=[x[0] for x in z];
        poi.stayTimes=[x[1] for x in z];

def orderTrails(POIs,links):
    orderCongestion(POIs);
    orderStays(POIs);
    links.sort(key=lambda link:link.enterTime);

#Estimate the number of hosts in a POI over time
def getPOICongestion(poi):
    precongestion=[];
    for stp in poi.listSTP:
        precongestion.append([stp.enterTime,1]);
        precongestion.append([stp.exitTime,-1]);
    precongestion.sort(key=lambda elem:elem[0]);
    sumV=0;
    for elem in precongestion:
        sumV+=elem[1];
        elem[1]=sumV;
    congestion=[];
    if (len(precongestion)>0):
        if (precongestion[0][0]>0):
            precongestion.insert(0, [0.0,0]);
        for i in range(0,len(precongestion)-1):
            if (precongestion[i][0]!=precongestion[i+1][0]):
                congestion.append(precongestion[i]);
        congestion.append(precongestion[-1])
    poi.congestion=congestion;
    
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
    POIs=e.extractPOIs(users,SRe,Sre,TR,maxX,maxY);             #Generate TRAILS locations from traces
    for poi in POIs:                                                    
        stayTimes=[stp.stayTime for stp in poi.listSTP];        #Get stay intervals for each POI
        enterTimes=[stp.enterTime for stp in poi.listSTP];      #Get enter times for each POI
        z=list(zip(enterTimes,stayTimes))
        z.sort(key=lambda elem:elem[0]);
        poi.stayTimes=[x[1] for x in z];
        poi.enterTimes=[x[0] for x in z];
        getPOICongestion(poi);                                  
    links=t.getLinks(users,POIs);                               #Get connected locations with links
    t.classifyLinks(links,MinU);                                #Classify paths unrealistic
    POIs=t.getConnectedPOIs(links)                              #Remove POIs that do not belog to any link
    return POIs,links;

#Export the TRAILS graph into csv files
#        Input
#    outputFolder: Output directory
#    POIs: List of POIs
#    links: List of links
def exportTrails(outputFolder,POIs,links,base_time=0):
    for i in range(0,len(POIs)):
        POIs[i].pindex=i;
    if base_time>0:
        TRAILSpath = outputFolder+'/TRAILS'+str(base_time);
    else:
        TRAILSpath = outputFolder+'/TRAILS';
    if not os.path.exists(TRAILSpath):
        os.makedirs(TRAILSpath);
    with open(TRAILSpath+'/POIs.csv', 'w') as f:
        writer = csv.writer(f, delimiter =' ');
        for poi in POIs:
            writer.writerow([int(poi.px),int(poi.py)]);
            writer.writerow([int(e) for e in poi.enterTimes]);
            writer.writerow([int(e) for e in poi.stayTimes]);
            writer.writerow([int(elem[0]) for elem in poi.congestion]);
            writer.writerow([int(elem[1]) for elem in poi.congestion]);
    with open(TRAILSpath+'/Links.csv', 'w') as f:
        writer = csv.writer(f, delimiter =' ');
        for link in links:
            initialPOI=link.initialPOI.pIndex;
            finalPOI=link.finalPOI.pIndex;
            unrealistic=1 if link.unrealistic else 0;
            returnIU=1 if link.returnIU else 0;
            returnEU=1 if link.returnEU else 0;                
            writer.writerow([int(initialPOI),int(finalPOI),int(unrealistic),int(returnIU),int(returnEU),int(link.totalTime),int(link.enterTime)]);
            writer.writerow([int(e) for e in link.timeInterval]);
            writer.writerow([int(e) for e in link.x]);
            writer.writerow([int(e) for e in link.y]);

def printMeanStats(links,POIs):
    v=0
    for link in links:
        dx=link.finalPOI.px-link.initialPOI.px
        dy=link.finalPOI.py-link.initialPOI.py
        d=(dx**2+dy**2)**0.5
        t=link.totalTime
        v+=d/t
    v=v/len(links)
    print ("mean velocity="+str(v))
    s=0
    c=0
    for poi in POIs:
        for e in poi.stayTimes:
            s+=e
        c+=len(poi.stayTimes)
    s=s/c
    print ("mean wait period="+str(s))

#Process to import POIs
#        Input
#    inFolder: Input folder where the traces are saved
def importPOIs(inFolder, base_time=0):
    POIs=[];
    csvdelimeter = " ";
    reader = csv.reader(open(inFolder+"/POIs.csv", "r"), delimiter=csvdelimeter);
    dataList=list(reader);
    for i in range(0,len(dataList),5):
        px=int(dataList[i][0]);
        py=int(dataList[i][1]);
        stayTimes=[int(elem) for elem in dataList[i+2]];
        poi=o.POI(None,px,py,stayTimes,i/5);
        if base_time>0:
            poi.enterTimes=[int(elem)%base_time for elem in dataList[i+1]];
            congestionTime=[int(elem)%base_time for elem in dataList[i+3]];
        else:
            poi.enterTimes=[int(elem) for elem in dataList[i+1]];
            congestionTime=[int(elem) for elem in dataList[i+3]];            
        congestionNum=[int(elem) for elem in dataList[i+4]];
        poi.congestion=list(zip(congestionTime,congestionNum));
        POIs.append(poi);
    return POIs;

#Process to import Links
#        Input
#    inFolder: Input folder where the traces are saved
#    POIs: List of points of interest
def importLinks(inFolder,POIs, base_time=0):
    csvdelimeter = " ";
    reader = csv.reader(open(inFolder+"/Links.csv", "r"), delimiter=csvdelimeter);
    dataList=list(reader);
    links=[];
    for i in range(0,len(dataList),4):
        initialPOI=POIs[int(dataList[i][0])];
        finalPOI=POIs[int(dataList[i][1])];
        totalTime=int(dataList[i][5]);
        timeInterval=[int(ti) for ti in dataList[i+1]];
        xv=[int(x) for x in dataList[i+2]];
        yv=[int(x) for x in dataList[i+3]];
        link=o.Link(xv,yv,timeInterval,totalTime,finalPOI,initialPOI);
        link.unrealistic=True if dataList[i][2]=="1" else False;
        link.returnIU=True if dataList[i][3]=="1" else False;
        link.returnEU=True if dataList[i][4]=="1" else False;
        if base_time>0:
            link.enterTime=int(dataList[i][6])%base_time;
        else:
            link.enterTime=int(dataList[i][6]);
        initialPOI.links.append(link);
        links.append(link);
    return links;

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
def plotFigure(POIs,plotP,incUnrealistic,output):
    fig = plt.figure();
    ax = fig.add_subplot(111);
    plotLocations=[];
    for poi in POIs:
        plotLocation=[poi.px,poi.py,False];
        for link in poi.links:
            cyclic=link.returnIU if incUnrealistic else link.returnEU;
            if incUnrealistic or not link.unrealistic:
                link.x.insert(0,link.initialPOI.px);
                link.y.insert(0,link.initialPOI.py);
                link.x.append(link.finalPOI.px);
                link.y.append(link.finalPOI.py);
                line=ax.plot(link.x,link.y, linewidth=plotP.lineWidth);
                ax.plot(link.x,link.y, linewidth=plotP.lineWidth);
                #createArrow(ax,line,plotP.arrowSize);        
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