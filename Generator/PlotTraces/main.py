#Load custom parameters in the generator
import sys              #Export print functions into a file
import plotFigure as g  #Process traces and it creates a TRAILS graph
#Input and output directories
inOutF=g.InOutFiles;
inOutF.inFolder='/home/user/Traces';
inOutF.outFolder='/home/user/output';
#Parameters to plot graphs
plotP=g.PlotParameters;
plotP.lineWidth = 0.25;     #Width of the line representing a path
plotP.dpi=100;              #Dots per inch
plotP.fSize=(6.4,4.8);      #Plot Size (width,length) in inches
#Main function
orig_stdout = sys.stdout;
f = open(inOutF.outFolder+'/TracesPlotOuput.txt', 'w');    #Summary file of the generator
sys.stdout = f;
g.plotFigure(inOutF,plotP);
sys.stdout = orig_stdout;
f.close();
