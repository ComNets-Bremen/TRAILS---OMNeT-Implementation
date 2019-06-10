#Functions to import traces of a specific format
#https://crawdad.org/epfl/main/20090224/
import users as u   #Functions to process traces
import os           #Functions to create directories
import csv          #Functions to create csv tables

#Process to import one user trace
#        Input
#    inFolder: Input folder where the traces are saved
def importUser(inFolder):
    reader = csv.reader(open(inFolder, "rb"), delimiter=' ');
    a = list(reader);
    y = [float(l[0]) for l in a][::-1]; #latitude
    x = [float(l[1]) for l in a][::-1]; #logitude
    time = [float(l[3]) for l in a][::-1];
    return u.User(time,x,y);

#Process to import traces
#        Input
#    inFolder: Input folder where the traces are saved
def importUsers(inFolder):
    onlyfiles = [f for f in os.listdir(inFolder) if (os.path.isfile(os.path.join(inFolder, f)) and f.find('new')==0)];
    users = [importUser(inFolder+'/'+fileName) for fileName in onlyfiles]; 
    u.transformDegreesMeters(users);
    return users;