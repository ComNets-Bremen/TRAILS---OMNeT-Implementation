#Load custom parameters in the generator
import sys                  #Export print functions into a file
import _operations as g  #General functions
#Input and output directories
inOutF=g.InOutFiles;
inOutF.inFolder='/home/leonardo/TRAILSResults/output/TRAILS';    #traceP.traceType=0
inOutF.outFolder='/home/leonardo/TRAILSResults/output';
#Recursion parameters
maximumRecursion=None;  #If is 0 or none it is the size of POIs 
#Main function
orig_stdout = sys.stdout
f = open(inOutF.outFolder+'/TRAILSLinksOuput.txt', 'w')    #Summary file of the generator
sys.stdout = f
g.returnLinks(inOutF,maximumRecursion);
sys.stdout = orig_stdout
f.close()
