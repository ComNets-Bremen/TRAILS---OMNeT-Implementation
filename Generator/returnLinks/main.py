#Load custom parameters in the generator
import sys                  #Export print functions into a file
import classification as g  #Process traces and it creates a TRAILS graph
#Input and output directories
inOutF=g.InOutFiles;
inOutF.inFolder='/home/user/output/TRAILS';
inOutF.outFolder='/home/user/output';
#Recursion parameters
maximumRecursion=990;  #If is 0 or none it is the size of POIs 
#Main function
orig_stdout = sys.stdout;
f = open(inOutF.outFolder+'/TRAILSLinksOuput.txt', 'w');    #Summary file of the generator
sys.stdout = f;
g.classify(inOutF,maximumRecursion);
sys.stdout = orig_stdout;
f.close();
