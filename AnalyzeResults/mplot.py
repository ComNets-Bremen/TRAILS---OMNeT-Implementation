import matplotlib.pyplot as plt     #Functions to plot graphs
import analyzem as an
import statistics as st
import estats as est

def importcsv(ffile):
    metric=[[],[]];
    efile = open(ffile,'r');
    for line in efile:
        line=line.split(',');
        metric[0].append(float(line[0]));
        metric[1].append(float(line[1]));
    efile.close();
    return metric;

def plotFigure(metric,output):
    fig=plt.figure();
    ax=fig.add_subplot(111);
    ax.plot(*metric);
    if output != None:
        fig.savefig(output, format='pdf');
        plt.close(fig);
    else:
        plt.show();

def plotCompare(m1,m2,output):
    fig=plt.figure();
    ax=fig.add_subplot(111);
    ax.plot(*m1,color='blue');
    ax.plot(*m2,color='red');
    #ax.set_yscale('log')
    #ax.set_xscale('log')
    if output != None:
        fig.savefig(output, format='pdf');
        plt.close(fig);
    else:
        plt.show();

def plotComparexlog(m1,m2,output):
    fig=plt.figure();
    ax=fig.add_subplot(111);
    ax.plot(*m1,color='blue');
    ax.plot(*m2,color='red');
    #ax.set_yscale('log')
    ax.set_xscale('log')
    if output != None:
        fig.savefig(output, format='pdf');
        plt.close(fig);
    else:
        plt.show();
        
def plotMeans(sinput,stopic):
    metric=[];
    for ind in xrange(0,10000):
        try:
            m=an.loadMetric(sinput+'/86400_'+str(ind)+stopic+'.csv',1);
        except:
            break;
        if len(m)>0:
            metric.append(st.mean(m));
    probVec=est.getCumulative(metric);
    est.getPDF(probVec);
    plotFigure([probVec[0],probVec[1]],sinput+stopic+'CDF.pdf');
    plotFigure([probVec[0],probVec[2]],sinput+stopic+'PDF.pdf');
    

print 'h'
nmetrics=['CDBN','CNPR','CTBN','NCBS','NCBN'];
general1='/home/leonardo/eclipse-workspace/analizeMobility/data/newyork/traces/stats/'
general2='/home/leonardo/eclipse-workspace/analizeMobility/data/newyork/m1/stats/'

general3='/home/leonardo/eclipse-workspace/analizeMobility/data/newyork/traces/cycles/functions/'
general4='/home/leonardo/eclipse-workspace/analizeMobility/data/newyork/m1/cycles/functions/'
'''
for nmetric in nmetrics:
    m=importcsv(general3+'86400_'+nmetric+'_PDF.csv');
    plotFigure(m,general3+nmetric+'_PDF.pdf');
    m=importcsv(general3+'86400_'+nmetric+'_PCF.csv');
    plotFigure(m,general3+nmetric+'_CDF.pdf');
    m=importcsv(general4+'86400_'+nmetric+'_PDF.csv');
    plotFigure(m,general4+nmetric+'_PDF.pdf');
    m=importcsv(general4+'86400_'+nmetric+'_PCF.csv');
    plotFigure(m,general4+nmetric+'_CDF.pdf');
'''
for nmetric in nmetrics:
    m1=importcsv(general1+nmetric+'_PDF.csv');
    m2=importcsv(general2+nmetric+'_PDF.csv');
    plotCompare(m1,m2,general2+nmetric+'_vsPDF.pdf');
    plotComparexlog(m1,m2,general2+nmetric+'_vsPDF_log_lin.pdf');
    m1=importcsv(general1+nmetric+'_PCF.csv');
    m2=importcsv(general2+nmetric+'_PCF.csv');
    plotCompare(m1,m2,general2+nmetric+'_vsCDF.pdf');
    plotComparexlog(m1,m2,general2+nmetric+'_vsCDF_log_lin.pdf');
