#Group objects by the Smallest enclosing circle
#Library Based on Smallest enclosing circle impementation of Project Nayuki 
#https://www.nayuki.io/page/smallest-enclosing-circle
from TrailsGenerator import objects as o         #Objets used as structures for the TRAILS graph generator

_MULTIPLICATIVE_EPSILON = 1+1e-14;  #Constant to find points in the border of a circle

#Compute the Minimum bounding box of [box,p]
#        Input
#    box: Box object
#    p: Point coordinates or box object
#        Output
#    newBox: Minimum bounding box of [box,p]
def getBoundingBox(box,p):
    if type(p) is o.Point:
        xMin=p.x;
        xMax=p.x;
        yMin=p.y;
        yMax=p.y;
    else:
        xMin=p.minX;
        xMax=p.maxX;
        yMin=p.minY;
        yMax=p.maxY;        
    minX=box.minX if box.minX<xMin else xMin;
    minY=box.minY if box.minY<yMin else yMin;
    maxX=box.maxX if box.maxX>xMax else xMax;
    maxY=box.maxY if box.maxY>yMax else yMax;
    return o.Box(minX,minY,maxX,maxY);

#Find out if the point is inside the circle
#        Input
#    circle: limiting shape
#    point: coordinates to be evualated
#        Output
#    Boolean flag
def is_in_circle(circle, point):
    if circle != None:
        if circle.centerX==point.x and circle.centerY==point.y:
            return True;
        if circle.squareRadius>0.0:
            rx=abs(circle.centerX-point.x);
            ry=abs(circle.centerY-point.y); 
            if rx**2+ry**2<circle.squareRadius*_MULTIPLICATIVE_EPSILON: 
                return True;
    return False;

#Compute the circle described by the coordinates of 2 points
#        Input
#    a,b: Points coordinates
#        Output
#    circle: Circle described by the coordinates of 2 points
def twoPointCircle(a, b):
    cx=(a.x + b.x)/2;
    cy=(a.y + b.y)/2;
    sr0=(cx-a.x)**2+(cy - a.y)**2;
    sr1=(cx-b.x)**2+(cy - b.y)**2;
    sr=sr0 if sr0>sr1 else sr1;
    return o.Circle(cx,cy,sr);

#Compute the Circumscribed circle described by the coordinates of 3 points (https://en.wikipedia.org/wiki/Circumscribed_circle)
#        Input
#    a,b,c: Points coordinates
#        Output
#    circle: Circumscribed circle described by the coordinates of 3 points
def threePointCircle(a,b,c):
    ox=(min(a.x,b.x,c.x)+max(a.x,b.x,c.x))/2;
    oy=(min(a.y,b.y,c.y)+max(a.y,b.y,c.y))/2;
    ax=a.x-ox;  
    ay=a.y-oy;
    bx=b.x-ox;  
    by=b.y-oy;
    cx=c.x-ox;  
    cy=c.y-oy;
    d=(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))*2;
    if d == 0.0:
        return None
    x=ox+((ax*ax+ay*ay)*(by-cy)+(bx*bx+by*by)*(cy-ay)+(cx*cx+cy*cy)*(ay-by))/d
    y=oy+((ax*ax+ay*ay)*(cx-bx)+(bx*bx+by*by)*(ax-cx)+(cx*cx+cy*cy)*(bx-ax))/d
    sra=(x-a.x)**2+(y-a.y)**2;
    srb=(x-b.x)**2+(y-b.y)**2;
    src=(x-c.x)**2+(y-c.y)**2;
    return o.Circle(x,y,max(sra, srb, src));

#Returns twice the signed area of the triangle defined by (x0, y0), (x1, y1), (x2, y2)
#        Input
#    x0, y0, x1, y1, x2, y2: Coordinates of 3 points
#        Output
#    Twice the signed area of the triangle defined by (x0, y0), (x1, y1), (x2, y2)
def _cross_product(x0, y0, x1, y1, x2, y2): 
    return (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)

#Compute the smallest enclosing circle of [points,p,q]
#        Input
#    points: List of points coordinates
#    p: point coordinates in the border of the new smallest enclosing circle
#    q: Point coordinates in the border of the new smallest enclosing circle
#        Output
#    newCircle:New smallest enclosing circle
def _make_circle_two_points(points, p, q):  # Two boundary points known
    circ=twoPointCircle(p, q);
    left  = None
    right = None 
    for r in points:    # For each point not in the two-point circle
        if is_in_circle(circ, r):
            continue  
        cross = _cross_product(p.x, p.y, q.x, q.y, r.x, r.y);   # Form a circumcircle and classify it on left or right side
        c=threePointCircle(p, q, r);
        if c is None:
            continue;
        elif cross > 0.0 and (left is None or _cross_product(p.x, p.y, q.x, q.y, c.centerX, c.centerY) > _cross_product(p.x,p.y,q.x,q.y,left.centerX,left.centerY)):
            left = c;
        elif cross < 0.0 and (right is None or _cross_product(p.x, p.y, q.x, q.y, c.centerX, c.centerY) < _cross_product(p.x,p.y,q.x,q.y,right.centerX,right.centerY)):
            right = c;
    if left is None and right is None:  # Select which circle to return
        return circ;
    elif left is None:
        return right;
    elif right is None:
        return left;
    else:
        return left if (left.squareRadius <= right.squareRadius) else right;

#Find the smallest enclosing circle (SEC) of [points,newPoint] if you one have a point (q) that is in the border of the SEC of points
#        Input
#    points: List of the points coordinates of the set
#    circle: Smallest enclosing circle of points
#    newPoint: point coordinates to be evaluated
#    q: Point coordinates in the border of circle
#        Output
#    newCircle:New smallest enclosing circle
def getNewCircle(points,circle,newPoint,q):
    if circle.squareRadius == 0.0:
        return twoPointCircle(newPoint, q);
    else:
        return _make_circle_two_points(points,newPoint,q);

#Find out if a set of trace-points and a new trace-point can be merged in a circle with a maximum diameter SR
#        Input
#    points: List of the points coordinates of the set
#    circle: Smallest enclosing circle of points
#    newPoint: trace-point coordinates to be evaluated
#    SRe: Spatial range (SR) and its equivalents
#        Output
#    newPoints/points:New list of points if points and newPoint can be grouped, else return points
#    newCircle/circle:New smallest enclosing circle if points and newPoint can be grouped, else return circle
def addOnePoint(points,circle,newPoint,Sre):  # One boundary point known
    newPoints=[point for point in points];
    newPoints.insert(0,newPoint);
    if (not is_in_circle(circle,newPoint)):
        newCircle=o.Circle(0.0,0.0,0.0);
        for (i, q) in enumerate(points):    #Find a point in the border of the circle
            if newCircle.squareRadius==0.0 or (not is_in_circle(newCircle, q)):
                newCircle=getNewCircle(points[:i+1],newCircle,newPoint,q);
                if newCircle.squareRadius>Sre.squareRange:
                    return False,points,circle;
        return True,newPoints,newCircle;
    return True,newPoints,circle;

#Creates a Set of trace-points starting from the trace-point tp[index]
#        Input
#    user: user's trace
#    index: identifier of the first trace-point in the POI
#    SRe: Spatial range (SR) and its equivalents
#    Sre: Spatial radius (SR/2) and its equivalents
#    TR:Temporal range, minimum time for a POI
#        Output
#    POI: Point of interest
def getSTP(user,index,SRe,Sre,TR):
    pointsIndex=[index];                                                                #Add first point
    firstPoint=o.Point(x=user.x[index],y=user.y[index]);
    points=[firstPoint];
    box=o.Box(user.x[index],user.y[index],user.x[index],user.y[index]);
    circle=o.Circle(user.x[index],user.y[index],0.0);
    for i in range(index+1,len(user.time)):
        point=o.Point(user.x[i],user.y[i]);
        newBox=getBoundingBox(box,point);
        merge=False;
        if newBox.maxX-newBox.minX<=SRe.range and newBox.maxY-newBox.minY<=SRe.range:   #Check if the new point is inside the maximum allowed bouding box
            merge,points,circle=addOnePoint(points,circle,point,Sre);
        if merge:
            box=newBox;
            pointsIndex.append(i);                                                      #Add new point
        else:
            stayTime=user.time[pointsIndex[-1]]-user.time[pointsIndex[0]];
            if stayTime >= TR:
                stp=o.STP(user,pointsIndex,user.time[pointsIndex[0]],user.time[pointsIndex[-1]]);
                stp.px=circle.centerX;
                stp.py=circle.centerY;
                return stp;
            else:
                return None;
    return None;