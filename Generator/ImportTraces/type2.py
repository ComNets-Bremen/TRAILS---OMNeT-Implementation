#Functions to import traces of a specific format
#https://crawdad.org/roma/taxi/20140717/taxicabs/
import users as u   #Functions to process traces
import re           #Functions to parse strings
import csv          #Functions to create csv tables
import datetime     #Funtion to work with time-stamps

#Get total seconds from time stamp
#        Input
#    tstamp: String with time stamp
#        Output
#    Total seconds
def getTime(tstamp):
    try:
        utc_time = datetime.datetime.strptime(tstamp, "%Y-%m-%d %H:%M:%S.%f+01");
    except:
        utc_time = datetime.datetime.strptime(tstamp, "%Y-%m-%d %H:%M:%S+01");
    return (utc_time - datetime.datetime(1970, 1, 1)).total_seconds();

#Parse coorditates from string
#        Input
#    Pstr: String with coordinaltes
#        Output
#    Coordinates of trace-point
def getPosition(Pstr):
    return re.findall("\d+\.\d+",Pstr);

#Process to import traces
#        Input
#    inFile: Input file where the traces are described
def importUsers(inFile):
    reader = csv.reader(open(inFile, "rb"), delimiter=';');
    a = list(reader);
    timeAll = [getTime(l[1]) for l in a];
    position = [getPosition(l[2]) for l in a];
    userIndex = [int(l[0]) for l in a];
    del(a);
    yAll = [float(pos[0]) for pos in position]; #latitude
    xAll = [float(pos[1]) for pos in position]; #logitude
    del(position);
    users = [u.User([],[],[]) for i in xrange(0,max(userIndex)+1)];
    for i in xrange(0,len(userIndex)):
        users[userIndex[i]].time.append(timeAll[i]);
        users[userIndex[i]].x.append(xAll[i]);
        users[userIndex[i]].y.append(yAll[i]);
    users[userIndex[i]].inputPort=[None]*len(users[userIndex[i]].x);
    users[userIndex[i]].outputPort=[None]*len(users[userIndex[i]].x);
    del(timeAll,xAll,yAll,userIndex);
    users = [user for user in users if len(user.x)>0];
    for user in users:
        user.inputPort = [None]*len(user.x);
        user.outputPort = [None]*len(user.x);
    u.transformDegreesMeters(users);  
    return users;