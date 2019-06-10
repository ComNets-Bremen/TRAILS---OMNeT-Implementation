#Functions and objects to process and represent traces
import os                           #Functions to create directories
import csv                          #Functions to create csv tables
import math                         #Mathematical functions

#User trace
class User(object):
    def __init__(self, time, x, y):
        self.time = time;   #list of time stamps of trace-points
        self.x = x;         #list of X coordinates of trace-points
        self.y = y;         #list of Y coordinates of trace-points

#General parameters of traces
class Limits(object):
    def __init__(self, maxTime,maxX,maxY,nUsers):
        self.maxTime = maxTime; #Recording time
        self.maxX = maxX;       #Maximum width
        self.maxY = maxY;       #Maximum length
        self.nUsers = nUsers;   #Number of users

#Compute distance between 2 points described in logitude and latitude
#https://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
#        Input
#    lon1: longitude of point1
#    latt1: latitude of point1
#    lon2: longitude of point2
#    latt2: latitude of point2
#        Output
#    Distance between 2 points in meters
def haversine(lon1,lat1,lon2,lat2): 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2]); 
    dlon = lon2 - lon1;
    dlat = lat2 - lat1;
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2; # haversine formula
    c = 2 * math.asin(math.sqrt(a)); # Radius of earth in kilometers is 6371
    return 6371000*c;

#Transform geographic coordinates into cartesian coordinates
#        Input
#    users: List of users traces
def transformDegreesMeters(users):
    minX=min([min(user.x) for user in users]);
    minY=min([min(user.y) for user in users]);
    for user in users:
        for i in xrange(0,len(user.x)):
            user.x[i]=haversine(minX, user.y[i], user.x[i], user.y[i]);
            user.y[i]=haversine(user.x[i], minY, user.x[i], user.y[i]);

#Find general parameters of traces
#        Input
#    users: List of users traces
#        Output
#    General parameters of traces
def removeOffset(users):
    minTime=min([min(user.time) for user in users]);
    minX=min([min(user.x) for user in users]);
    minY=min([min(user.y) for user in users]);
    for user in users:
        user.time=[time-minTime for time in user.time];
        user.x=[x-minX for x in user.x];
        user.y=[y-minY for y in user.y];
    maxTimes=max([max(user.time) for user in users]);
    maxXs=max([max(user.x) for user in users]);
    maxYs=max([max(user.y) for user in users]);
    return Limits(maxTimes,maxXs,maxYs,len(users));

#Export processed traces
#        Input
#    users: List of users traces
#    outFolder: Output directory to export traces
def exportUsers(outFolder,users):
    tracesPath = outFolder+'/Traces';
    if not os.path.exists(tracesPath):
        os.makedirs(tracesPath);
    for i in xrange(0,len(users)):
        with open(tracesPath+'/'+str(i)+'.csv', 'wb') as f:
            writer = csv.writer(f, delimiter ='\t');
            for j in xrange(0,len(users[i].x)):
                writer.writerow([users[i].time[j],users[i].x[j],users[i].y[j]]);