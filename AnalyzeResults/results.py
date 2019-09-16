import analyzem as an
import statistics as st
import timeit 

def analyze(outputPath,numNodes,samplesize,timeLimit,startTime):
    CDBN=[];#Contact duration
    SCDB=[];#sum contact duration
    NCBS=[];#Number of contacts between the same nodes
    NCBN=[];#Total number of contacts per each node
    CTBN=[];#Contact time between nodes
    for i in xrange(0,numNodes):
        efile = open(outputPath+'/'+str(i)+'.csv','r');
        econtent=efile.read();
        efile.close();
        events=an.str2list(econtent);
        if i>0:
            an.getCDBN(events,i,timeLimit,startTime,samplesize,CDBN,SCDB,NCBS,NCBN,CTBN);
    CNPR=[e/(timeLimit-startTime) for e in SCDB]; #Contact probability
    return CDBN,CNPR,NCBS,NCBN,CTBN;

def saveVector(outp,x,y):
    efile = open(outp,'w');
    for i in xrange(0,len(x)):
        efile.write(str(x[i])+','+str(y[i])+'\n');
    efile.close();
        
generalpath='/home/leonardo/eclipse-workspace/analizeMobility/data'
mnumNodes=536;
msimTime=2071530.0;

simTime=3600*2;
tCDBN=[];
tCNPR=[];
tNCBS=[];
tNCBN=[];
tCTBN=[];
tsim=[];
while simTime<msimTime:
    CDBN,CNPR,NCBS,NCBN,CTBN=analyze(generalpath+'/sanfrancisco/m1/iu/events',mnumNodes,1,simTime,0);
    tsim.append(simTime);
    tCDBN.append(st.mean(CDBN));
    tCNPR.append(st.mean(CNPR));
    tNCBS.append(st.mean(NCBS));
    tNCBN.append(st.mean(NCBN));
    tCTBN.append(st.mean(CTBN));
    simTime=simTime*2;

timepath=generalpath+'/sanfrancisco/m1/iu/stime/';
saveVector(timepath+'CDBN.csv',tsim,tCDBN);
saveVector(timepath+'CNPR.csv',tsim,tCNPR);
saveVector(timepath+'NCBS.csv',tsim,tNCBS);
saveVector(timepath+'NCBN.csv',tsim,tNCBN);
saveVector(timepath+'CTBN.csv',tsim,tCTBN);

start = timeit.default_timer();

numNodes=2;
nCDBN=[];
nCNPR=[];
nNCBS=[];
nNCBN=[];
nCTBN=[];
nsim=[];
while numNodes<mnumNodes:
    CDBN,CNPR,NCBS,NCBN,CTBN=analyze(generalpath+'/sanfrancisco/m1/iu/events',numNodes,1,msimTime,0);
    nsim.append(numNodes);
    nCDBN.append(st.mean(CDBN));
    nCNPR.append(st.mean(CNPR));
    nNCBS.append(st.mean(NCBS));
    nNCBN.append(st.mean(NCBN));
    nCTBN.append(st.mean(CTBN));
    numNodes=numNodes*2;
    
nodepath=generalpath+'/sanfrancisco/m1/iu/snodes/';
saveVector(nodepath+'CDBN.csv',nsim,nCDBN);
saveVector(nodepath+'CNPR.csv',nsim,nCNPR);
saveVector(nodepath+'NCBS.csv',nsim,nNCBS);
saveVector(nodepath+'NCBN.csv',nsim,nNCBN);
saveVector(nodepath+'CTBN.csv',nsim,nCTBN);

stop = timeit.default_timer();
print("Time to generate the TRAILS graph(s)=" + str(stop - start));