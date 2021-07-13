#Load custom parameters in the generator
import sys                                  #Export print functions into a file
import _operations as g                      #General functions
from TrailsGenerator import trails as tg    #Functions to generate TRAILS graphs
import timeit                               #Funtions to meassure computation time
#Constants
CIRCLE=0;   #Smallest enclosing circle
BOX=1;      #Minimum bounding box
#Input and output directories
inOutF=g.InOutFiles;
inOutF.inFolder='/home/leonardo/TRAILSResults/output/TRAILS_Paper/sanfrancisco/TRAILS_10km';
inOutF.outFolder='/home/leonardo/TRAILSResults/output/TRAILS_Paper/sanfrancisco';
#Main function
orig_stdout = sys.stdout
f = open(inOutF.outFolder+'/TRAILSResizeOuput.txt', 'w')    #Summary file of the generator
sys.stdout = f
base_time=604800;
start = timeit.default_timer();
POIs=tg.importPOIs(inOutF.inFolder,base_time);
Links=tg.importLinks(inOutF.inFolder,POIs,base_time);
tg.orderTrails(POIs,Links);
tg.exportTrails(inOutF.outFolder,POIs,Links,base_time);
stop = timeit.default_timer();
print("Time to generate the TRAILS graph(s)=" + str(stop - start));
sys.stdout = orig_stdout
f.close()
