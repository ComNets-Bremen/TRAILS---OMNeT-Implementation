#Process traces and it creates a TRAILS graph
from ImportTraces import type0 as ut0       #Functions to import traces of a specific format
from TrailsGenerator import trails as tg    #Functions to generate TRAILS graphs
import timeit                               #Funtions to meassure computation time

#Input and output directories
class InOutFiles(object):
    def __init__(self):
        self.inFolder=None;   #Input
        self.outFolder=None;  #Output

#Parameters to generate a TRAILS graph
class TrailsParameters(object):
    def __init__(self):
        self.SR=None;           #Spatial range used to group trace-points and POIs meters
        self.TR=None;           #Temporal range, minimum time for a POI seconds
        self.MinU=None;         #Distance threshold to detect an unrealistic path

#Process, reformat, plot, and export traces
#Generate, plot, and eport a TRAILS graph based on imported traces
#        Input
#    inOutF: Input and output directories
#    trailsP: Parameters to generate a TRAILS graph
def generator(inOutF,trailsP):
    start = timeit.default_timer();
    users = ut0.importUsers(inOutF.inFolder);
    maxXs=max([max(user.x) for user in users]);
    maxYs=max([max(user.y) for user in users]);
    POIs,links=tg.getTrails(users,trailsP.SR,trailsP.TR,trailsP.MinU,maxXs,maxYs);
    tg.exportTrails(inOutF.outFolder,POIs,links);
    stop = timeit.default_timer();
    print("Time to generate the TRAILS graph(s)=" + str(stop - start));
