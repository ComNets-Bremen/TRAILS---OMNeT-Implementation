#Functions to generate TRAILS graphs
import csv                          #Functions to create csv tables
import matplotlib.pyplot as plt     #Functions to plot graphs
import objects as o

PLOTDELTA = 10**-6; #Constant used to plot arrows

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
        poi=o.POI(px,py,stayTimes)
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
def plotTrails(POIs,plotP,incNoReturn,incUnrealistic,output):
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
    ax.scatter(centerX,centerY,marker='x',color='b',s=plotP.POISize);
    ax.axis('equal');
    ax.set_ylim(ax.get_ylim()[::-1]);        # invert the axis
    ax.xaxis.tick_top();                     # and move the X-Axis      
    if output != None:
        fig.savefig(output, format='pdf',dpi=plotP.dpi,figsize=plotP.fSize);
        plt.close(fig);
    else:
        plt.show();