#Load custom parameters in the generator
import sys              #Export print functions into a file
import process as g  #Process traces and it creates a TRAILS graph
#Input and output directories
inOutF=g.InOutFiles;
inOutF.inFolder='/home/user/input/Traces_TimeXY_30sec_txt/NewYork';    #traceP.traceType=0
#inOutF.inFolder='/home/user/input/cabspottingdata';              #traceP.traceType=1
#inOutF.inFolder='/home/user/input/taxi_february/taxi_february.txt';   #traceP.traceType=2
inOutF.outFolder='/home/user/output';
#Parameters to process a traces
traceP=g.TraceParameters;
traceP.traceType=0;         #Format of the traces to import
traceP.maxSpeed=60;         #Velocity threshold to filter traces m/s
traceP.maxDistance=100000;  #Distance threshold to filter traces meters
traceP.resolution=0.1;      #New resolution for traces meters
#Main function
orig_stdout = sys.stdout;
f = open(inOutF.outFolder+'/TracesGraphOuput.txt', 'w');    #Summary file of the generator
sys.stdout = f;
g.process(inOutF,traceP);
sys.stdout = orig_stdout;
f.close();
