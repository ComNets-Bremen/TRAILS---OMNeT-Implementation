#Group objects by the Circle Box aproximation
import objects as o             #Objets used as structures for the TRAILS graph generator

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
