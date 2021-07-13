#Load custom parameters in the generator
import sys              #Export print functions into a file
import _operations as g  #General functions
#Input and output directories
inOutF=g.InOutFiles;
#inOutF.inFolder='/home/leonardo/TRAILSResults/input/Traces_TimeXY_30sec_txt/NewYork';    #traceP.traceType=0
#inOutF.inFolder='/home/leonardo/TRAILSResults/input/cabspottingdata';                    #traceP.traceType=1
#inOutF.inFolder='/home/leonardo/TRAILSResults/input/taxi_february/taxi_february.txt';    #traceP.traceType=2
inOutF.inFolder='/home/leonardo/TRAILSResults/output/sanfrancisco/SWIM/graph/03.csv'      #traceP.traceType=3
inOutF.outFolder='/home/leonardo/TRAILSResults/output/sanfrancisco/SWIM/graph';
#Parameters to process a traces
traceP=g.TraceParameters;
traceP.traceType=3;         #Format of the traces to import
traceP.MaxV=60;             #Velocity threshold to filter traces m/s
traceP.MaxD=100000;         #Distance threshold to filter traces meters
traceP.resolution=0.1;      #New resolution for traces meters
#Main function
orig_stdout = sys.stdout
f = open(inOutF.outFolder+'/SWIMGraphOuput.txt', 'w')    #Summary file of the generator
sys.stdout = f
g.processTraces(inOutF,traceP);
sys.stdout = orig_stdout
f.close()
