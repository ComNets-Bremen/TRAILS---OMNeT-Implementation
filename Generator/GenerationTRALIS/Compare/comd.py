#Comparison of multiple distances algorithm
#Equivalent to compare the euclidean distance of 2 points with a constant threshold
ROOT2=2**0.5;   #Constant to compute equivalent distances

#Threshold Range
class Threshold(object):
    def __init__(self,rRange):  #Equivalent thresholds are calculated only once
        self.range=1.0*rRange;
        self.sideRange=self.range/ROOT2;
        self.squareRange=self.range**2;
        self.manhattanRange=ROOT2*self.range;
       
#Find out if the eucleadean distance between 2 points is smaller than a range
#        Input
#    rx: Distance in X between 2 points
#    ry: Distance in Y between 2 points
#    SRe: range and its equivalents
#        Output
#    Boolean flag
def isInRange(rx,ry,eRange):
    cd=rx if rx>ry else ry;
    if cd>eRange.range:
        return False;
    if cd<=eRange.sideRange:
        return True;
    md=rx+ry;
    if md>eRange.manhattanRange:
        return False;
    if md<=eRange.range:
        return True
    if rx**2+ry**2<=eRange.squareRange:   
        return True;
    return False;