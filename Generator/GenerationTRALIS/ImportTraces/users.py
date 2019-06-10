#objects to process and represent traces
#User trace
class User(object):
    def __init__(self, time, x, y):
        self.time = time;   #list of time stamps of trace-points
        self.x = x;         #list of X coordinates of trace-points
        self.y = y;         #list of Y coordinates of trace-points
        self.inputPort = [None]*len(self.x);    #list of input locations
        self.outputPort = [None]*len(self.x);   #list of output locations
