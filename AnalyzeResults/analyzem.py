import re
import estats as es;
import scipy.stats as stats;
import statistics as st;

numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
rx = re.compile(numeric_const_pattern, re.VERBOSE)
import timeit 

class Metric(object):
    def __init__(self,CDBN,CNPR,NCBS,NCBN,CTBN):
        self.CDBN = CDBN;   #Contact duration
        self.CNPR = CNPR;   #Contact probability
        self.NCBS = NCBS;   #Number of contacts between the same nodes
        self.NCBN = NCBN;   #Total number of contacts per each node
        self.CTBN = CTBN;   #Contact time between nodes
#Generate a logfile per each node
def divideLogs(inputPath,outPath,numUsers):
    events=["" for i in xrange(0,numUsers)];
    efile = open(inputPath,'r');
    #econtent=efile.read();
    #efile.close();
    #econtent=econtent.splitlines();
    for eline in efile:
    #for eline in econtent:
        probe="says:";
        index=eline.find(probe);
        if index>-1:
            evalues=rx.findall(eline);
            time=evalues[0];
            node=int(evalues[1]);
            neighbor=evalues[2];
            if len(evalues)>4:
                duration=evalues[4];
            else:
                duration='-1';
            events[node]+=time+';'+neighbor+';'+duration+'\n';
    efile.close();
    for i in xrange(0,numUsers):
        efile = open(outPath+'/'+str(i)+'.csv','w');
        efile.write(events[i]);
        efile.close();
#Index of last item inside a the timeLimit
def findsublist(events,timeLimit):
    for i in xrange(0,len(events)):
        if events[i][0]>timeLimit:
            return i-1;
    return len(events)-1;
#Contact duration
#sum contact duration
#Number of contacts between the same nodes
#Total number of contacts per each node
#Contact time between nodes
def getCDBN(events,node,timeLimit,startTime,samplesize,CDBN,SCDB,NCBS,NCBN,CTBN):
    sums=[0 for i in xrange(0,node)];
    counts=[0 for i in xrange(0,node)];
    tcounts=0;
    firstcontact=samplesize;
    lastcontact=samplesize;
    for i in xrange(0,len(events)):
        if events[i][0]>timeLimit:
            break;
        elif events[i][0]>startTime:
            neighbor=events[i][1];
            if neighbor<node:
                duration=events[i][2];
                if duration>0:
                    sums[neighbor]+=duration;
                    CDBN.append(duration);
                else:
                    counts[neighbor]+=1;
                    tcounts+=1;
                    if events[i][0]>firstcontact:
                        duration=events[i][0]-lastcontact;
                        lastcontact=events[i][0];
                        CTBN.append(duration);
    SCDB.extend(sums);
    NCBS.extend(counts);
    NCBN.append(tcounts);
#Transform list to string
def list2str(elist):
    estr="";
    for e in elist:
        estr+=str(e)+'\n';
    return estr;
#Save list
def savelist(elist,histpath,ename):
    estr=list2str(elist);
    efile = open(histpath+'/'+ename+'.csv','w');
    efile.write(estr);
    efile.close();
#Save realizations
def saveCyclicHist(histpath,per,ind,CDBN,CNPR,NCBS,NCBN,CTBN):
    savelist(CDBN,histpath,str(per)+'_'+str(ind)+'CDBN');
    savelist(CNPR,histpath,str(per)+'_'+str(ind)+'CNPR');
    savelist(NCBS,histpath,str(per)+'_'+str(ind)+'NCBS');
    savelist(NCBN,histpath,str(per)+'_'+str(ind)+'NCBN');
    savelist(CTBN,histpath,str(per)+'_'+str(ind)+'CTBN');
#Transform sring to list
def str2list(econtent):
    events=[];
    econtent=econtent.splitlines();
    for ec in econtent:
        ec=ec.split(';');
        e=[float(ec[0]),int(ec[1]),float(ec[2])];
        events.append(e);
    return events;
#Save histogram and statistics parameters
def saveStats(histPath,m):
    es.getstats(m.CDBN, histPath,'CDBN');
    es.getstats(m.CNPR, histPath,'CNPR');
    es.getstats(m.NCBS, histPath,'NCBS');
    es.getstats(m.NCBN, histPath,'NCBN');
    es.getstats(m.CTBN, histPath,'CTBN');
#Save PDF and Cumulative function
def saveCyclicProbabilityVectors(histPath,m1,periods):
    for i,period in enumerate(periods):
        metric=[st.mean(m) for m in m1.CDBN[i] if len(m)>0];
        es.saveProbVec(metric,histPath+'/'+str(period)+'_CDBN');
        metric=[st.mean(m) for m in m1.CNPR[i] if len(m)>0];
        es.saveProbVec(metric,histPath+'/'+str(period)+'_CNPR');
        metric=[st.mean(m) for m in m1.NCBS[i] if len(m)>0];
        es.saveProbVec(metric,histPath+'/'+str(period)+'_NCBS');
        metric=[st.mean(m) for m in m1.NCBN[i] if len(m)>0];
        es.saveProbVec(metric,histPath+'/'+str(period)+'_NCBN');
        metric=[st.mean(m) for m in m1.CTBN[i] if len(m)>0];
        es.saveProbVec(metric,histPath+'/'+str(period)+'_CTBN');
#Save PDF and Cumulative function
def saveProbabilityVectors(histPath,m):
    es.saveProbVec(m.CDBN,histPath+'/CDBN');
    es.saveProbVec(m.CNPR,histPath+'/CNPR');
    es.saveProbVec(m.NCBS,histPath+'/NCBS');
    es.saveProbVec(m.NCBN,histPath+'/NCBN');
    es.saveProbVec(m.CTBN,histPath+'/CTBN');

def loadCycle(histPath,stopic,per,lenInd):
    metric=[];
    for ind in xrange(0,lenInd):
        metric.append(loadMetric(histPath+'/'+str(per)+'_'+str(ind)+stopic+'.csv',1));
    return metric;
#Load metric emode=0 Int emode=1 float
def loadMetric(inputpath,emode):
    metric=[];
    efile = open(inputpath,'r');
    for line in efile:
        if emode==0:
            metric.append(int(line));
        else:
            metric.append(float(line));
    efile.close();
    return metric;
def loadCyclicEvents(histPath,periods,simTime):
    CDBN=[None]*len(periods);
    CNPR=[None]*len(periods);
    NCBS=[None]*len(periods);
    NCBN=[None]*len(periods);
    CTBN=[None]*len(periods);
    for j in xrange(0,len(periods)):
        startTimes=[];
        i=0;
        h=0;
        while i<simTime:
            startTimes.append(i);
            i+=periods[j];
            h+=1;
        CDBN[j]=loadCycle(histPath,'CDBN',periods[j],h);
        CNPR[j]=loadCycle(histPath,'CNPR',periods[j],h);
        NCBS[j]=loadCycle(histPath,'NCBS',periods[j],h);
        NCBN[j]=loadCycle(histPath,'NCBN',periods[j],h);
        CTBN[j]=loadCycle(histPath,'CTBN',periods[j],h);
    return Metric(CDBN,CNPR,NCBS,NCBN,CTBN);
#save csv
def saveCSV(elist,outP):
    content="";
    for i in xrange(0,len(elist)):
        for j in xrange(0,len(elist[i])):
            if j<len(elist[i])-1:
                content+=str(elist[i][j])+',';
            else:
                content+=str(elist[i][j]);
        if i<len(elist)-1:
            content+='\n';
    efile = open(outP,'w');
    efile.write(content);
    efile.close();
#Compare cycle
def compareCycle(metric,periods,outP):
    cycle=[[None,None,None] for period in periods];
    for i in xrange(0,len(periods)):
        b = stats.kruskal(*metric[i]);
        cycle[i][0]=periods[i];
        cycle[i][1]=b.pvalue;
        cycle[i][2]=b.statistic;
    saveCSV(cycle,outP);

def compareCycles(m,ppath,periods):
    compareCycle(m.NCBS,periods,ppath+'/NCBS.csv');
    compareCycle(m.CDBN,periods,ppath+'/CDBN.csv');
    compareCycle(m.CNPR,periods,ppath+'/CNPR.csv');
    compareCycle(m.NCBN,periods,ppath+'/NCBN.csv');
    compareCycle(m.CTBN,periods,ppath+'/CTBN.csv');

#Compare means
def compareMean(mtrails,mtraces):
    mtrails=[st.mean(m) for m in mtrails if len(m)>0];
    meantrails=st.mean(mtrails);
    varmeantrails=st.variance(mtrails)/len(mtrails);
    meantraces=st.mean(mtraces);
    err=(meantraces-meantrails)**2/varmeantrails;
    pvalue=1-stats.chi2.cdf(err, 1);
    return str(err)+','+str(pvalue)+','+str(meantrails)+','+str(meantraces)+'\n';

def compareMeans(mTrails,mTraces,outP):
    efile=open(outP,'w');
    efile.write('NCBS '+compareMean(mTrails.NCBS[1],mTraces.NCBS));
    efile.write('CDBN '+compareMean(mTrails.CDBN[1],mTraces.CDBN));
    efile.write('CNPR '+compareMean(mTrails.CNPR[1],mTraces.CNPR));
    efile.write('NCBN '+compareMean(mTrails.NCBN[1],mTraces.NCBN));
    efile.write('CTBN '+compareMean(mTrails.CTBN[1],mTraces.CTBN));
    efile.close();
#Compare metrics
def compare(m1,m2,stopic):
    scomp1='CDBN '+str(stats.ranksums(m1.CDBN, m2.CDBN))+'\n'+\
        'CNPR '+str(stats.ranksums(m1.CNPR, m2.CNPR))+'\n'+\
        'NCBS '+str(stats.ranksums(m1.NCBS, m2.NCBS))+'\n'+\
        'NCBN '+str(stats.ranksums(m1.NCBN, m2.NCBN))+'\n'+\
        'CTBN '+str(stats.ranksums(m1.CTBN, m2.CTBN))+'\n';
    scomp2='CDBN_median '+str(stats.median_test(m1.CDBN, m2.CDBN))+'\n'+\
        'CDBN '+str(st.median(m1.CDBN))+','+str(st.median(m2.CDBN))+'\n'+\
        'CNPR_median '+str(stats.median_test(m1.CNPR, m2.CNPR))+'\n'+\
        'CNPR '+str(st.median(m1.CNPR))+','+str(st.median(m2.CNPR))+'\n'+\
        'NCBS_median '+str(stats.median_test(m1.NCBS, m2.NCBS))+'\n'+\
        'NCBS '+str(st.median(m1.NCBS))+','+str(st.median(m2.NCBS))+'\n'+\
        'NCBN_median '+str(stats.median_test(m1.NCBN, m2.NCBN))+'\n'+\
        'NCBN '+str(st.median(m1.NCBN))+','+str(st.median(m2.NCBN))+'\n'+\
        'CTBN_median '+str(stats.median_test(m1.CTBN, m2.CTBN))+'\n'+\
        'CTBN '+str(st.median(m1.CTBN))+','+str(st.median(m2.CTBN))+'\n';
    efile = open(stopic,'w');
    efile.write(scomp1+scomp2);
    efile.close();

#Compare metrics
def compare_Means(m1,m2,stopic):
    scomp2='CDBN'+es.mean_test([m1.CDBN, m2.CDBN])+\
        'CNPR'+es.mean_test([m1.CNPR, m2.CNPR])+\
        'NCBS'+es.mean_test([m1.NCBS, m2.NCBS])+\
        'NCBN'+es.mean_test([m1.NCBN, m2.NCBN])+\
        'CTBN'+es.mean_test([m1.CTBN, m2.CTBN]);
    efile = open(stopic,'w');
    efile.write(scomp2);
    efile.close();
    
#Compare metrics
def compareCLT(m1,m2,stopic):
    scomp2='CDBN_mean '+str(es.CLT_test([m1.CDBN, m2.CDBN]))+'\n'+\
        'CDBN '+str(st.mean(m1.CDBN))+','+str(st.mean(m2.CDBN))+'\n'+\
        'CNPR_mean '+str(es.CLT_test([m1.CNPR, m2.CNPR]))+'\n'+\
        'CNPR '+str(st.mean(m1.CNPR))+','+str(st.mean(m2.CNPR))+'\n'+\
        'NCBS_mean '+str(es.CLT_test([m1.NCBS, m2.NCBS]))+'\n'+\
        'NCBS '+str(st.mean(m1.NCBS))+','+str(st.mean(m2.NCBS))+'\n'+\
        'NCBN_mean '+str(es.CLT_test([m1.NCBN, m2.NCBN]))+'\n'+\
        'NCBN '+str(st.mean(m1.NCBN))+','+str(st.mean(m2.NCBN))+'\n'+\
        'CTBN_mean '+str(es.CLT_test([m1.CTBN, m2.CTBN]))+'\n'+\
        'CTBN '+str(st.mean(m1.CTBN))+','+str(st.mean(m2.CTBN))+'\n';
    efile = open(stopic,'w');
    efile.write(scomp2);
    efile.close();

#Compare metrics
def compareCLT2(m1,m2,stopic):
    scomp2='CDBN_mean '+str(es.CLT2_test([m1.CDBN, m2.CDBN]))+'\n'+\
        'CDBN '+str(st.mean(m1.CDBN))+','+str(st.mean(m2.CDBN))+'\n'+\
        'CNPR_mean '+str(es.CLT2_test([m1.CNPR, m2.CNPR]))+'\n'+\
        'CNPR '+str(st.mean(m1.CNPR))+','+str(st.mean(m2.CNPR))+'\n'+\
        'NCBS_mean '+str(es.CLT2_test([m1.NCBS, m2.NCBS]))+'\n'+\
        'NCBS '+str(st.mean(m1.NCBS))+','+str(st.mean(m2.NCBS))+'\n'+\
        'NCBN_mean '+str(es.CLT2_test([m1.NCBN, m2.NCBN]))+'\n'+\
        'NCBN '+str(st.mean(m1.NCBN))+','+str(st.mean(m2.NCBN))+'\n'+\
        'CTBN_mean '+str(es.CLT2_test([m1.CTBN, m2.CTBN]))+'\n'+\
        'CTBN '+str(st.mean(m1.CTBN))+','+str(st.mean(m2.CTBN))+'\n';
    efile = open(stopic,'w');
    efile.write(scomp2);
    efile.close();

#Analyze distribution
def analyzeCyclic(outputPath,histPath,numNodes,samplesize,timeLimit,startTime,per,ind):
    CDBN=[];#Contact duration
    SCDB=[];#sum contact duration
    NCBS=[];#Number of contacts between the same nodes
    NCBN=[];#Total number of contacts per each node
    CTBN=[];#Contact time between nodes
    for i in xrange(0,numNodes):
        efile = open(outputPath+'/'+str(i)+'.csv','r');
        econtent=efile.read();
        efile.close();
        events=str2list(econtent);
        if i>0:
            getCDBN(events,i,timeLimit,startTime,samplesize,CDBN,SCDB,NCBS,NCBN,CTBN);
    CNPR=[e/(timeLimit-startTime) for e in SCDB]; #Contact probability
    saveCyclicHist(histPath,per,ind,CDBN,CNPR,NCBS,NCBN,CTBN);

#Load realizations
def loadEvents(histPath): 
    CDBN=loadMetric(histPath+'/'+'CDBN.csv',1);
    CNPR=loadMetric(histPath+'/'+'CNPR.csv',1);
    NCBS=loadMetric(histPath+'/'+'NCBS.csv',1);
    NCBN=loadMetric(histPath+'/'+'NCBN.csv',1);
    CTBN=loadMetric(histPath+'/'+'CTBN.csv',1);
    return Metric(CDBN,CNPR,NCBS,NCBN,CTBN);

#Save realizations
def saveHist(histpath,CDBN,CNPR,NCBS,NCBN,CTBN):
    savelist(CDBN,histpath,'CDBN');
    savelist(CNPR,histpath,'CNPR');
    savelist(NCBS,histpath,'NCBS');
    savelist(NCBN,histpath,'NCBN');
    savelist(CTBN,histpath,'CTBN');

#Analyze distribution
def analyze(outputPath,histPath,numNodes,samplesize,timeLimit,startTime):
    CDBN=[];#Contact duration
    SCDB=[];#sum contact duration
    NCBS=[];#Number of contacts between the same nodes
    NCBN=[];#Total number of contacts per each node
    CTBN=[];#Contact time between nodes
    for i in xrange(0,numNodes):
        efile = open(outputPath+'/'+str(i)+'.csv','r');
        econtent=efile.read();
        efile.close();
        events=str2list(econtent);
        if i>0:
            getCDBN(events,i,timeLimit,startTime,samplesize,CDBN,SCDB,NCBS,NCBN,CTBN);
    CNPR=[e/(timeLimit-startTime) for e in SCDB]; #Contact probability
    saveHist(histPath,CDBN,CNPR,NCBS,NCBN,CTBN);

start = timeit.default_timer();

#Process sanfrancisco traces
'''
generalpath='/home/leonardo/eclipse-workspace/analizeMobility/data'
state='rome';
samplesize=1;
periods=[3600*8,3600*24,3600*24*7];
simTime=2591998.20398;
#periods=[3600];
numNodes=315;
statepath=generalpath+'/'+state;
#types=['/m0/eu','/m0/iu','/m1/eu','/m2/eu','/m2/iu'];
types=['/traces'];


for ttype in types:
    divideLogs(statepath+ttype+'/log.txt',statepath+ttype+'/events',numNodes);
'''
'''
periods=[3600*8,3600*24,3600*24*2,3600*24*3,3600*24*7];
generalpath='/home/leonardo/eclipse-workspace/analizeMobility/data'
state='/rome';
simTime=2591998.20398;
statepath=generalpath+'/'+state;
types=['/traces'];
numNodes=315;
samplesize=1;

#types=['/m0/iu'];
for ttype in types:
    outputPath=statepath+ttype+'/events';
    histPath=statepath+ttype+'/cycles/events';
    
    #analyze(outputPath,statepath+ttype+'/stats',numNodes,samplesize,simTime,0);
    for j in xrange(0,len(periods)):
        startTimes=[];
        i=0;
        while i<simTime:
            startTimes.append(i);
            i+=periods[j];
        print startTimes
        for i in xrange(0,len(startTimes)):
            analyzeCyclic(outputPath,histPath,numNodes,samplesize,startTimes[i]+periods[j],startTimes[i],periods[j],i);      
 


for ttype in types:
    mtrails=loadCyclicEvents(statepath+ttype+'/cycles/events',periods,simTime);
    
    compareCycles(mtrails,statepath+ttype+'/cycles/results',periods);
    saveCyclicProbabilityVectors(statepath+ttype+'/cycles/functions',mtrails,periods);
    
    #mtraces=loadEvents(statepath+'/traces'+'/stats');
    #compareMeans(mtrails,mtraces,statepath+ttype+'/compare/mean.txt')
    #mtrails=loadEvents(statepath+ttype+'/stats');
    #compare(mtrails,mtraces,statepath+ttype+'/compare/dist.txt')

'''
'''
generalpath='/home/leonardo/eclipse-workspace/analizeMobility/data'
types=['/m1/iu','/m1','/m1'];
states=['/rome','/orlando','/newyork'];
numNodes=315;
simTime=2591998.20398;
samplesize=1;
for i in xrange(0,len(types)):
    #analyze(generalpath+states[i]+types[i]+'/events',generalpath+states[i]+types[i]+'/stats',numNodes,samplesize,simTime,0)
    mtrails=loadEvents(generalpath+states[i]+types[i]+'/stats');
    mtraces=loadEvents(generalpath+states[i]+'/traces'+'/stats');
    saveProbabilityVectors(generalpath+states[i]+'/traces'+'/stats',mtraces)
    saveProbabilityVectors(generalpath+states[i]+types[i]+'/stats',mtrails)
    #compareCLT2(mtrails,mtraces,generalpath+states[i]+types[i]+'/compare/centralLimitTheorem2.txt')
    #compareCLT(mtrails,mtraces,generalpath+states[i]+types[i]+'/compare/centralLimitTheorem.txt')
    #compare(mtrails,mtraces,generalpath+states[i]+types[i]+'/compare/dist.txt')
    #compare_Means(mtrails,mtraces,generalpath+states[i]+types[i]+'/compare/Mean_values.txt')

'''
stop = timeit.default_timer();
print("Time to generate the TRAILS graph(s)=" + str(stop - start));
