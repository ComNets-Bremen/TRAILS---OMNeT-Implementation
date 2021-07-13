#Detects and removes undesired trace-points
from Compare import comd as c   #Comparisson of multiple distances algorithim

#Estimates the square velocity between 2 points
#        Input
#    x1: X coordinate of point1
#    y1: Y coordinae of point2
#    t1: Time stamp of point1
#    x2: X coordinate of point2
#    y2: Y coordinate of point2
#    t2: Time stamp of point2
#        Output
#    square velocity of the 2 points
def derivative(x1,y1,t1,x2,y2,t2):
    dt=1.0*t2-t1;
    if dt>0:
        xd=abs(x2-x1);
        yd=abs(y2-y1);
        return (xd**2+yd**2)/(dt**2);
    return None;

#Find out if 2 points are in a distance smaller than distanceMax
#        Input
#    x1: X coordinate of point1
#    y1: Y coordinae of point2
#    x2: X coordinate of point2
#    y2: Y coordinate of point2
#    distanceMax: Maximum distance between 2 points
#        Output
#    Boolean flag
def inRange(x1,y1,x2,y2,distanceMax):
    xd=abs(x2-x1);
    yd=abs(y2-y1);
    if xd<=distanceMax.real:
        if yd<=distanceMax.real:
            md=yd+xd;
            if md<=distanceMax.manhattan:
                if md<=distanceMax.real:
                    return True;
                if yd**2+xd**2<=distanceMax.square:
                        return True;
    return False;

#Remove noisy trace-points based on distance between points
#        Input
#    user: user trace
#    distanceMax: Maximum distance between 2 points
def filterPointsDistance(user,maxDistance):
    x=[];
    y=[];  
    time=[];
    for i in range(0,len(user.x)):
        if i==0:
            if len(user.x)>1:
                dx=abs(user.x[i]-user.x[i+1]);
                dy=abs(user.y[i]-user.y[i+1]);
                ds=c.isInRange(dx,dy,maxDistance);   #Future
            else:
                ds=0;
        elif i==len(user.x)-1:
            if len(x)>0:
                dx=abs(x[-1]-user.x[i]);
                dy=abs(y[-1]-user.y[i]);
                ds=c.isInRange(dx,dy,maxDistance);   #Past
            else:
                dx=abs(user.x[i-1]-user.x[i]);
                dy=abs(user.y[i-1]-user.y[i]);
                ds=c.isInRange(dx,dy,maxDistance);   #Past
        else:
            dx=abs(user.x[i]-user.x[i+1]);
            dy=abs(user.y[i]-user.y[i+1]);
            ds1=c.isInRange(dx,dy,maxDistance);  #Future
            if len(x)>0:
                dx=abs(x[-1]-user.x[i]);
                dy=abs(y[-1]-user.y[i]);
                ds2=c.isInRange(dx,dy,maxDistance);  #Past
            else:
                dx=abs(user.x[i-1]-user.x[i]);
                dy=abs(user.y[i-1]-user.y[i]);
                ds2=c.isInRange(dx,dy,maxDistance);  #Past
            if ds1==False or ds2==False:
                ds=False;
            else:
                ds=True;
        if ds:
            time.append(user.time[i]);
            x.append(user.x[i]);
            y.append(user.y[i]);
    user.time=time;
    user.x=x;
    user.y=y;            

#Find out if the velocity between 2 points is smaller than maxSpeed
#        Input
#    ds: Square velocity between 2 trace-points
#    maxSpeed: Maximum speed between 2 points
#        Output
#    Boolean flag
def compareVelocity(ds,maxSpeed):
    if ds != None:
        if ds<=maxSpeed.squareRange:
            return True;
    return False;

#Remove noisy trace-points based on velocity of points
#        Input
#    user: user trace
#    maxSpeed: Maximum speed between 2 points
def filterPointsSpeed(user,maxSpeed):
    x=[];
    y=[];
    time=[];
    for i in range(0,len(user.x)):
        if i==0:
            if len(user.x)>1:
                ds=derivative(user.x[i],user.y[i],user.time[i],user.x[i+1],user.y[i+1],user.time[i+1]); #Future
            else:
                ds=0;
        elif i==len(user.x)-1:
            if len(x)>0:
                ds=derivative(x[-1],y[-1],time[-1],user.x[i],user.y[i],user.time[i]);   #Past
            else:
                ds=derivative(user.x[i-1],user.y[i-1],user.time[i-1],user.x[i],user.y[i],user.time[i]); #Past
        else:
            ds1=derivative(user.x[i],user.y[i],user.time[i],user.x[i+1],user.y[i+1],user.time[i+1]);    #Future
            if len(x)>0:
                ds2=derivative(x[-1],y[-1],time[-1],user.x[i],user.y[i],user.time[i]);  #Past
            else:
                ds2=derivative(user.x[i-1],user.y[i-1],user.time[i-1],user.x[i],user.y[i],user.time[i]);    #Past
            if ds1==None or ds2==None:
                ds=None;
            elif ds1>ds2:
                ds=ds1;
            else:
                ds=ds2;
        if compareVelocity(ds,maxSpeed):
            time.append(user.time[i]);
            x.append(user.x[i]);
            y.append(user.y[i]);
    user.time=time;
    user.x=x;
    user.y=y;

#Remove noisy trace-points
#        Input
#    users: List of users traces
#    distanceMax: Maximum distance between 2 points
#    maxSpeed: Maximum speed between 2 points
def cleanPoints(users,speedMax,distanceMax):
    if distanceMax != None:
        if distanceMax>0:
            maxDistance=c.Threshold(distanceMax);
            for user in users:
                filterPointsDistance(user,maxDistance);
    if speedMax != None:
        if speedMax>0:
            maxSpeed=c.Threshold(speedMax);
            for user in users:
                filterPointsSpeed(user,maxSpeed);
    users=[user for user in users if len(user.x)>1];
    return users;

#Reduce the resoluton ot trace-points and remove redundant points
#        Input
#    users: List of users traces
#    New resolution for traces
def mergePoints(users,resolution):
    if resolution != None:
        if resolution>0:
            resolution=1.0*resolution;
            for user in users:
                for i in range(0,len(user.x)):
                    if resolution != 1:
                        user.x[i]=round(user.x[i]/resolution)*resolution;
                        user.y[i]=round(user.y[i]/resolution)*resolution;
                    else:
                        user.x[i]=round(user.x[i]);
                        user.y[i]=round(user.y[i]);
    for user in users:
        newX=[user.x[0]];
        newY=[user.y[0]];
        newTime=[user.time[0]];
        for i in range(1,len(user.x)-1):
            if (user.x[i] != user.x[i-1] or user.x[i] != user.x[i+1] or 
                user.y[i] != user.y[i-1] or user.y[i] != user.y[i+1]):      
                newX.append(user.x[i]);
                newY.append(user.y[i]);
                newTime.append(user.time[i]);
        newX.append(user.x[-1]);
        newY.append(user.y[-1]);
        newTime.append(user.time[-1]);            
        user.x=newX;
        user.y=newY;
        user.time=newTime;
