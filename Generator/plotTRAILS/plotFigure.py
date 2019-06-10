#Process traces and it creates a TRAILS graph
from TrailsGenerator import trails as tg    #Functions to generate TRAILS graphs
import timeit                               #Funtions to meassure computation time

#Input and output directories
class InOutFiles(object):
    def __init__(self):
        self.inFolder=None;   #Input
        self.outFolder=None;  #Output

#Parameters to plot graphs
class PlotParameters(object):
    def __init__(self):
        self.POISize=None; #Size of the object representing locations
        self.arrowSize=None;    #Size of the arrows to describe the direction of paths
        self.lineWidth=None;    #Width of the line representing a path
        self.dpi=None;          #Dots per inch
        self.fSize=(None,None); #Plot Size (width,length) in inches

#Plot TRAILS
#Import and plot TRAILS
#        Input
#    inOutF: Input and output directories
#    trailsP: Parameters to generate a TRAILS graph
def plotFigure(inOutF,plotP):
    start = timeit.default_timer();
    POIs=tg.importPOIs(inOutF.inFolder);
    tg.importLinks(inOutF.inFolder,POIs);
    tg.plotTrails(POIs,plotP,False,False,inOutF.outFolder+'/trails.pdf');
    #tg.plotTrails(POIs,plotP,True,False,inOutF.outFolder+'/trails_noReturn.pdf');
    tg.plotTrails(POIs,plotP,False,True,inOutF.outFolder+'/trails_Unrealistic.pdf');
    #tg.plotTrails(POIs,plotP,True,True,inOutF.outFolder+'/trails_noReturn_Unrealistic.pdf');
    stop = timeit.default_timer();
    print("Time to generate the TRAILS graph(s)=" + str(stop - start));
