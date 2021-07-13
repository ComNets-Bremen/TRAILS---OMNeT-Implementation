#Functions to import traces of a specific format
#https://crawdad.org/ncsu/mobilitymodels/20090723/    With delimeter '\t'
from ImportTraces import users as u   #Functions to process traces
import csv          #Functions to create csv tables
import os           #Functions to navigate through directories

#Process to import one user trace
#        Input
#    inFolder: Input folder where the traces are saved
#    delimeter: The delimeter of the csv table
def importUser(inFolder, **keyword_parameters):
    if ('delimeter' in keyword_parameters):
        csvdelimeter = keyword_parameters['delimeter'];
    else:
        csvdelimeter = '\t';
    reader = csv.reader(open(inFolder, "r"), delimiter=csvdelimeter);
    a = list(reader);
    time = [float(l[0]) for l in a];
    x = [float(l[1]) for l in a];
    y = [float(l[2]) for l in a];
    return u.User(time,x,y);

#Process to import traces
#        Input
#    inFolder: Input folder where the traces are saved
def importUsers(inFolder):
    onlyfiles = [f for f in os.listdir(inFolder) if os.path.isfile(os.path.join(inFolder, f))]
    users = [importUser(inFolder+'/'+fileName) for fileName in onlyfiles];    
    return users;