#Process traces and it creates a TRAILS graph
from ImportTraces import users as us           #Functions to process traces
from ImportTraces import type0 as ut0          #Functions to import traces of a specific format
import timeit                               #Funtions to meassure computation time

#Input and output directories
class InOutFiles(object):
    def __init__(self):
        self.inFolder=None;   #Input
        self.outFolder=None;  #Output
#Parameters to plot graphs
class PlotParameters(object):
    def __init__(self):
        self.lineWidth=None;    #Width of the line representing a path
        self.dpi=None;          #Dots per inch
        self.fSize=(None,None); #Plot Size (width,length) in inches
#Plot traces
#        Input
#    inOutF: Input and output directories
#    plotP: Parameters to plot graphs
def plotFigure(inOutF,plotP):
    #Trace operations
    start = timeit.default_timer();
    users = ut0.importUsers(inOutF.inFolder);
    us.plotTraces(users,inOutF.outFolder+'/traces.pdf',plotP);
    stop = timeit.default_timer();
    print("Time to plot Traces(s)=" + str(stop - start));