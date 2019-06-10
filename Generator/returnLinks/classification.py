#Process traces and it creates a TRAILS graph
from TrailsGenerator import trails as tg        #Functions to generate TRAILS graphs
from TrailsGenerator import connection as c     #Functions to generate TRAILS graphs
import timeit                                   #Funtions to meassure computation time

#Input and output directories
class InOutFiles(object):
    def __init__(self):
        self.inFolder=None;   #Input
        self.outFolder=None;  #Output

#Classify links
#Classify links and export TRAILS
#        Input
#    inOutF: Input and output directories
#    recursion: If it is 0 or none it is the size of POIs 
def classify(inOutF,recursion):
    start = timeit.default_timer();
    POIs=tg.importPOIs(inOutF.inFolder);
    tg.importLinks(inOutF.inFolder,POIs);
    c.classifyPaths(POIs,recursion);
    tg.exportTrails(inOutF.outFolder,POIs);
    stop = timeit.default_timer();
    print("Time to generate the TRAILS graph(s)=" + str(stop - start));
