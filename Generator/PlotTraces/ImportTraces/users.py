#Functions and objects to process and represent traces
import matplotlib.pyplot as plt     #Functions to plot graphs

#User trace
class User(object):
    def __init__(self, time, x, y):
        self.time = time;   #list of time stamps of trace-points
        self.x = x;         #list of X coordinates of trace-points
        self.y = y;         #list of Y coordinates of trace-points

#Plot a Traces graph and save it as pdf
#        Input
#    users: List of users traces
#    output: Output directory to export the plot
#    plotP: Plot parameters
def plotTraces(users,output,plotP):
    fig=plt.figure();
    ax=fig.add_subplot(111);
    for user in users:
        ax.plot(user.x,user.y, linewidth=plotP.lineWidth);
    ax.axis('equal');
    ax.set_ylim(ax.get_ylim()[::-1]);        # invert the axis
    ax.xaxis.tick_top();                     # and move the X-Axis 
    if output != None:
        fig.savefig(output, format='pdf',dpi=plotP.dpi,figsize=plotP.fSize);
        plt.close(fig);
    else:
        plt.show();