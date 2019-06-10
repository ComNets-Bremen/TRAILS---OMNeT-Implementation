#Load custom parameters in the generator
import sys              #Export print functions into a file
import generation as g  #Process traces and it creates a TRAILS graph
#Input and output directories
inOutF=g.InOutFiles;
inOutF.inFolder='/home/user/output/Traces';
inOutF.outFolder='/home/user/output';
#Parameters to generate a TRAILS graph
trailsP=g.TrailsParameters;
trailsP.SR=30;              #Spatial range used to group trace-points and POIs meters
trailsP.TR=180;             #Temporal range, minimum time for a POI seconds
trailsP.MinU=2000;          #Distance threshold to detect an unrealistic path meters
#Main function
orig_stdout = sys.stdout;
f = open(inOutF.outFolder+'/TRAILSGraphOuput.txt', 'w');    #Summary file of the generator
sys.stdout = f;
g.generator(inOutF,trailsP);
sys.stdout = orig_stdout;
f.close();
