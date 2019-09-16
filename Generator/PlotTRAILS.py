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
inOutF.inFolder='/home/leonardo/TRAILSResults/output/SmartTRAILS';
inOutF.outFolder='/home/leonardo/TRAILSResults/output';
#Parameters to plot graphs
plotP=g.PlotParameters;
plotP.POISize = 15;    #Size of the object representing locations
plotP.arrowSize = 200;      #Size of the arrows to describe the direction of paths
plotP.lineWidth = 0.25;     #Width of the line representing a path
plotP.dpi=100;              #Dots per inch
plotP.fSize=(6.4,4.8);      #Plot Size (width,length) in inches
#Main function
orig_stdout = sys.stdout
f = open(inOutF.outFolder+'/TRAILSPlotOuput.txt', 'w')    #Summary file of the generator
sys.stdout = f
start = timeit.default_timer();
POIs=tg.importPOIs(inOutF.inFolder);
tg.importLinks(inOutF.inFolder,POIs);
tg.plotFigure(POIs,plotP,False,False,inOutF.outFolder+'/trails.pdf');
tg.plotFigure(POIs,plotP,True,False,inOutF.outFolder+'/trails_noReturn.pdf');
tg.plotFigure(POIs,plotP,False,True,inOutF.outFolder+'/trails_Unrealistic.pdf');
tg.plotFigure(POIs,plotP,True,True,inOutF.outFolder+'/trails_noReturn_Unrealistic.pdf');
stop = timeit.default_timer();
print("Time to generate the TRAILS graph(s)=" + str(stop - start));
sys.stdout = orig_stdout
f.close()
