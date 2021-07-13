#Process traces and it creates a TRAILS graph
from ImportTraces import users as us            #Functions to process traces
from ImportTraces import type0 as ut0           #Functions to import traces of a specific format
from ImportTraces import type1 as ut1           #Functions to import traces of a specific format
from ImportTraces import type2 as ut2           #Functions to import traces of a specific format
from ImportTraces import type3 as ut3           #Functions to import traces of a specific format
from ImportTraces import tracefilter as tf      #Detects and removes undesired trace-points
from TrailsGenerator import trails as tg        #Functions to generate TRAILS graphs
from TrailsGenerator import classification as c #Functions to generate TRAILS graphs
import timeit                                   #Funtions to meassure computation time

#Input and output directories
class InOutFiles(object):
    def __init__(self):
        self.inFolder=None;   #Input
        self.outFolder=None;  #Output

#Parameters to process a traces
class TraceParameters(object):
    def __init__(self):
        self.traceType=None;        #Format of the traces to import
        self.MaxV=None;             #Velocity threshold to filter traces m/s
        self.MaxD=None;             #Distance threshold to filter traces
        self.resolution=None;       #New resolution for traces

#Parameters to generate a TRAILS graph
class TrailsParameters(object):
    def __init__(self):
        self.SR=None;           #Spatial range used to group trace-points and POIs meters
        self.TR=None;           #Temporal range, minimum time for a POI seconds
        self.MinU=None;         #Distance threshold to detect an unrealistic path

#Parameters to plot graphs
class PlotParameters(object):
    def __init__(self):
        self.POISize=None;      #Size of the object representing locations
        self.arrowSize=None;    #Size of the arrows to describe the direction of paths
        self.lineWidth=None;    #Width of the line representing a path
        self.dpi=None;          #Dots per inch
        self.fSize=(None,None); #Plot Size (width,length) in inches

#Process, reformat, and export traces
#        Input
#    inOutF: Input and output directories
#    traceP: Parameters to process a traces
def processTraces(inOutF,traceP):
    #Trace operations
    start = timeit.default_timer();
    if traceP.traceType==0:
        users = ut0.importUsers(inOutF.inFolder);
    elif traceP.traceType==1:
        users = ut1.importUsers(inOutF.inFolder);
    elif traceP.traceType==2:
        users = ut2.importUsers(inOutF.inFolder);
    elif traceP.traceType==3:
        users = ut3.importUsers(inOutF.inFolder)
    else:
        raise ValueError("Unknown type of traces")
    
    tf.mergePoints(users,traceP.resolution);
    users=tf.cleanPoints(users,traceP.MaxV,traceP.MaxD);
    limits = us.removeOffset(users);
    us.exportUsers(inOutF.outFolder,users);
    print('Width(m)='+str(limits.maxX));
    print('Length(m)='+str(limits.maxY));
    print('Time(s)='+str(limits.maxTime));
    print('Users='+str(limits.nUsers));
    stop = timeit.default_timer();
    print("Time to process Traces(s)=" + str(stop - start));
    
#Process, reformat, plot, and export traces
#Generate, plot, and eport a TRAILS graph based on imported traces
#        Input
#    inOutF: Input and output directories
#    trailsP: Parameters to generate a TRAILS graph
def generationTRAILS(inOutF,trailsP):
    start = timeit.default_timer();
    users = ut0.importUsers(inOutF.inFolder);
    maxXs=max([max(user.x) for user in users]);
    maxYs=max([max(user.y) for user in users]);
    POIs,links=tg.getTrails(users,trailsP.SR,trailsP.TR,trailsP.MinU,maxXs,maxYs);
    c.classifyPaths(POIs);
    tg.exportTrails(inOutF.outFolder,POIs,links);
    tg.printMeanStats(links,POIs)
    stop = timeit.default_timer();
    print("Time to generate the TRAILS graph(s)=" + str(stop - start));
    
#Plot traces
#        Input
#    inOutF: Input and output directories
#    plotP: Parameters to plot graphs
def plotTraces(inOutF,plotP):
    #Trace operations
    start = timeit.default_timer();
    users = ut0.importUsers(inOutF.inFolder);
    us.plotFigure(users,inOutF.outFolder+'/traces.pdf',plotP);
    stop = timeit.default_timer();
    print("Time to plot Traces(s)=" + str(stop - start));