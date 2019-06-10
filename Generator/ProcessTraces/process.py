#Process traces and it creates a TRAILS graph
from ImportTraces import users as us           #Functions to process traces
from ImportTraces import type0 as ut0          #Functions to import traces of a specific format
from ImportTraces import type1 as ut1          #Functions to import traces of a specific format
from ImportTraces import type2 as ut2          #Functions to import traces of a specific format
from ImportTraces import tracefilter as tf     #Detects and removes undesired trace-points
import timeit                               #Funtions to meassure computation time

#Input and output directories
class InOutFiles(object):
    def __init__(self):
        self.inFolder=None;   #Input
        self.outFolder=None;  #Output

#Parameters to process a traces
class TraceParameters(object):
    def __init__(self):
        self.traceType=None;        #Format of the traces to import
        self.maxSpeed=None;         #Velocity threshold to filter traces m/s
        self.maxDistance=None;      #Distance threshold to filter traces
        self.resolution=None;       #New resolution for traces

#Process, reformat, and export traces
#        Input
#    inOutF: Input and output directories
#    traceP: Parameters to process a traces
def process(inOutF,traceP):
    #Trace operations
    start = timeit.default_timer();
    if traceP.traceType==0:
        users = ut0.importUsers(inOutF.inFolder);
    elif traceP.traceType==1:
        users = ut1.importUsers(inOutF.inFolder);
    else:
        users = ut2.importUsers(inOutF.inFolder);
    tf.mergePoints(users,traceP.resolution);
    users=tf.cleanPoints(users,traceP.maxSpeed,traceP.maxDistance);
    limits = us.removeOffset(users);
    us.exportUsers(inOutF.outFolder,users);
    print('Width(m)='+str(limits.maxX));
    print('Length(m)='+str(limits.maxY));
    print('Time(s)='+str(limits.maxTime));
    print('Users='+str(limits.nUsers));
    stop = timeit.default_timer();
    print("Time to process Traces(s)=" + str(stop - start));