from matplotlib import pyplot as plt
import statistics as st
import scipy.stats as stats
import numpy as np

def power_divergence(f_obs, f_exp=None, ddof=0, axis=0):
    f_obs = np.asanyarray(f_obs)
    f_exp = np.atleast_1d(np.asanyarray(f_exp));
    terms = (f_obs - f_exp)**2 / f_exp;
    stat = terms.sum(axis=axis)
    num_obs = np.ma.count(terms, axis=axis)
    ddof = np.asarray(ddof)
    p = stats.distributions.chi2.sf(stat, num_obs - 1 - ddof)
    return stat, p;

def CLT_test(data):
    cdata = [float(item) for sublist in data for item in sublist]
    grand_mean = st.mean(cdata)
    means=[st.mean(d) for d in data];
    terms=[(emean-grand_mean)**2/grand_mean for emean in means];
    stat=sum(terms);  
    pvalue=1-stats.chi2.cdf(stat, len(means)-1);
    return stat, pvalue, grand_mean, means;

def CLT2_test(data):
    cdata = [float(item) for sublist in data for item in sublist]
    grand_mean = st.mean(cdata)
    means=[st.mean(d) for d in data];
    var=[st.variance(d) for d in data];
    print var
    terms=[(means[i]-grand_mean)**2/(var[i]/len(data[i])) for i in xrange(0,len(means))];
    stat=sum(terms);  
    pvalue=1-stats.chi2.cdf(stat, len(means)-1);
    return stat, pvalue, grand_mean, means, [v**0.5 for v in var];

def mean_test(metric):
    cmetric=[prediction_interval(m) for m in metric];
    print [len(m) for m in metric];
    print [len(m) for m in cmetric];
    print 'h'
    sr='\n';
    sr+=str(CLT_test(metric))+'\n';
    sr+=str(CLT2_test(metric))+'\n';
    sr+=str(CLT_test(cmetric))+'\n';
    try:
        sr+=str(CLT2_test(cmetric))+'\n';
    except:
        sr+='var=0.0\n';
    return sr;

def prediction_interval(data, confidence=0.95):
    b=sorted(data);
    c=(1-confidence)/2.0    
    iout=int(round(len(b)*c));
    return b[iout:-iout]

#Calculate the bins for a histogram
def getBins(metric,r):
    if r==0:
        nbins=2*len(metric)**(1/3.0);    #Rice's Rule
        ebins=(max(metric)-min(metric))/nbins;
    elif r==1:
        nbins=3.49*st.stdev(metric)*len(metric)**(-1/3.0); #Scott's Rulest
        ebins=(max(metric)-min(metric))/nbins;
    else:
        ebins=1;
    i=min(metric);
    ebin=[min(metric)];
    while i<=max(metric):
        i+=ebins;
        ebin.append(i);
    return ebin;
#Estimate sample confidence interval
def confidence_interval(data, confidence=0.95):
    b=sorted(data);
    c=(1-confidence)/2.0    
    iout=int(len(b)*c);
    return [b[iout],b[-iout-1]]
#Plot relative frequency
def plotFigure(metric,output,erule):
    ebin=getBins(metric,erule);
    hist=getHist(metric,ebin);
    fig=plt.figure();
    ax=fig.add_subplot(111);
    ex=[(ebin[i+1]+ebin[i])/2 for i in xrange(0,len(ebin)-1)];
    ax.bar(x=ex,height=hist,width=(ebin[1]-+ebin[0])*0.95);
    ax.set_yscale('linear');
    fig.savefig(output+'.pdf', format='pdf');
    ax.set_yscale('log');
    fig.savefig(output+'_ylog.pdf', format='pdf');
    plt.close(fig);
#estimate the histogram
def getstats(metric,histPath,stopic):
    efile = open(histPath+'/'+stopic+'_stats.txt','w');
    efile.write("mean: "+str(st.mean(metric))+"; stdev: "+str(st.stdev(metric))+'\n');
    efile.write("absolute min: "+str(min(metric))+"; absolute max: "+str(max(metric))+'\n');
    cmin,cmax=confidence_interval(metric);
    efile.write("cf min: "+str(cmin)+"; cf max: "+str(cmax)+'\n');
    efile.write("realizations: "+str(len(metric))+'\n');
    efile.close();
#Estimate probability cummulative function
def getCumulative(metric):  
    #maxcb=250000.0;
    probVec=[[0,0,0]];
    metric.sort();
    #eb=(metric[-1]-metric[0])/maxcb;
    eb=0;
    lenMetric=len(metric);
    for i in xrange(0,lenMetric):
        if metric[i]<=probVec[-1][0]+eb:
            probVec[-1][1]=i+1;
        else:
            probVec.append([metric[i],i+1,0]);
    for p in probVec:
        p[1]=p[1]/(lenMetric*1.0);
    return probVec;
#Estimate probability desity function   
def getPDF(probVec):
    for i in xrange(1,len(probVec)-1):
        backward=(probVec[i][1]-probVec[i-1][1])/(1.0*(probVec[i][0]-probVec[i-1][0]));
        forward =(probVec[i+1][1]-probVec[i][1])/(1.0*(probVec[i+1][0]-probVec[i][0]));
        probVec[i][2]=0.5*(forward+backward);
    if(probVec[0][1])!=0:
        probVec[0][2]=None;

def saveNormality(metric):
    try:
        return str(stats.shapiro(metric))+'\n'+str(stats.normaltest(metric));
    except:
        return ""
#Save probability vector
def saveProbVec(metric,outputPath):
    #limitsize=1000;
    #limitprob=0.975;
    probVec=getCumulative(metric);
    getPDF(probVec);
    cfile = open(outputPath+'_PCF.csv','w');
    pfile = open(outputPath+'_PDF.csv','w');
    if probVec[0][2]!=None:
        pfile.write(str(probVec[0][0])+','+str(probVec[0][2])+'\n');
    cfile.write(str(probVec[0][0])+','+str(probVec[0][1])+'\n');
    for i in xrange(1,len(probVec)):
        pfile.write(str(probVec[i][0])+','+str(probVec[i][2])+'\n');
        cfile.write(str(probVec[i][0])+','+str(probVec[i][1])+'\n');
        #if i>=limitsize and probVec[i][1]>=limitprob:
        #    break;
    cfile.close();
    pfile.close();
    nfile = open(outputPath+'_normality.csv','w');
    nfile.write(saveNormality(metric));
    nfile.close();
#Estimate histogram 
def getHist(metric,ebin):
    hist=[0 for i in xrange(0,len(ebin)-1)];
    for event in metric:
        for h in xrange(0,len(ebin)-1):
            if event>=ebin[h] and event<ebin[h+1]:
                hist[h]+=1;
    return hist;       
#Save statistical parameters
def save_stats(metric,histPath,stopic,erule):
    getstats(metric,histPath,stopic);