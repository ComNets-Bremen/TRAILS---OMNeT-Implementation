//Send links and pois to users
#include "coordinator.h"

namespace inet {

    Define_Module(Coordinator);

    //Splits strings into vectors
    //      Input
    //  line: Input String
    //  delimiter: delimiter
    //      Output
    //  vec: String vector
    vector<string> Coordinator::splitString(string line, string delimiter) {
        vector<string> vec;
        size_t pos = 0;
        string token;
        while ((pos = line.find(delimiter)) != string::npos) {
            token = line.substr(0, pos);
            vec.push_back(token);
            line.erase(0, pos + delimiter.length());
        }
        vec.push_back(line);
        return vec;
    }

    //Imports a CSV table
    //      Input
    //  fileName: Trace file
    //      Output
    //  dataList: CSV table imported
    vector<vector<string>> Coordinator::readMatrix(string fileName) {
        string delimiter = " ";
        ifstream file(fileName);
        vector<vector<string>> dataList;
        string line = "";
        // Iterate through each line and split the content using delimiter
        while (getline(file, line)){
            vector<string> vec;
            vec=splitString(line, delimiter);
            dataList.push_back(vec);
        }
        // Close the File
        file.close();
        return dataList;
    }

    //Transforms a string vector into a double vector
    //      Input
    //  vec: String vector
    //      Output
    //  res: Double vector
    vector<double> Coordinator::toDoubleVector(vector<string> vec){
        vector<double> res;
        for (unsigned int i=0;i<vec.size();i++){
            res.push_back(stod(vec[i]));
        }
        return res;
    }

    //Loads the TRAILS graph from a file with pois and a file with links
    void Coordinator::initialize(){
        bool enable = par("enable");
        if (enable){
            bool linkUnrealistic;
            bool linkReturn;
            int mode = par("mode");
            bool includeUnrealistic = par("includeUnrealistic");
            const char *trailsFolder=par("trailsFolder").stringValue();
            string trailsDirectory(trailsFolder);
            vector<vector<string>> dataList=readMatrix(trailsDirectory+"/POIs.csv");
            for (unsigned int i=0;i<dataList.size()-1;i+=2){
                sPOI_t poi;
                poi.centerX=stod(dataList[i][0]);
                poi.centerY=stod(dataList[i][1]);
                poi.stayTimes=toDoubleVector(dataList[i+1]);
                vector<sLink_t> links;
                poi.links=links;
                pois.push_back(poi);
            }
            dataList=readMatrix(trailsDirectory+"/Links.csv");
            for (unsigned int i=0;i<dataList.size()-3;i+=4){
                vector<double> deltaTime=toDoubleVector(dataList[i+1]);
                vector<double> x;
                vector<double> y;
                if (deltaTime.size()>1){
                    x=toDoubleVector(dataList[i+2]);
                    y=toDoubleVector(dataList[i+3]);
                }
                if (stoi(dataList[i][2]) == 1){
                    linkUnrealistic=true;
                }else{
                    linkUnrealistic=false;
                }
                if (includeUnrealistic){
                    if (stoi(dataList[i][3])==1){
                        linkReturn=true;
                    }else{
                        linkReturn=false;
                    }
                }else{
                    if (stoi(dataList[i][4])==1){
                        linkReturn=true;
                    }else{
                        linkReturn=false;
                    }
                }
                if (not linkUnrealistic || includeUnrealistic){
                    if (linkReturn || mode != 0){
                        int poiIndex=stoi(dataList[i][0]);
                        int nextPOIIndex=stoi(dataList[i][1]);
                        sLink_t link;
                        link.pNextPOI=&pois[nextPOIIndex];
                        link.x=x;
                        link.x.push_back(pois[nextPOIIndex].centerX);
                        link.y=y;
                        link.y.push_back(pois[nextPOIIndex].centerY);
                        link.deltaTime=deltaTime;
                        pois[poiIndex].links.push_back(link);
                        if ((mode==2 && not linkReturn) || mode==1){
                            sLink_t rLink;
                            rLink.pNextPOI=&pois[poiIndex];
                            rLink.x=x;
                            reverse(rLink.x.begin(),rLink.x.end());
                            rLink.x.push_back(pois[poiIndex].centerX);
                            rLink.y=y;
                            reverse(rLink.y.begin(),rLink.y.end());
                            rLink.y.push_back(pois[poiIndex].centerY);
                            rLink.deltaTime=deltaTime;
                            reverse(rLink.deltaTime.begin(),rLink.deltaTime.end());
                            pois[nextPOIIndex].links.push_back(rLink);
                        }
                    }
                }
            }
            for (unsigned int i=0;i<pois.size();i++){
                if(pois[i].links.size()>0){
                    pPOIs.push_back(&pois[i]);
                }
            }
            for (unsigned int i=0;i<pPOIs.size();i++){
                sPOI* sp=static_cast<sPOI*>(pPOIs[i]);
                EV<<"poi "<<i<<'\n';
                EV<<"links "<<sp->links.size()<<"\n";
                EV<<"times "<<sp->stayTimes.size()<<"\n";
            }
        }
    }

    //Give a instruction to a user every time it arrives to a poi
    //      Input
    //  *p: Pointer of the poi where the user arrived
    //      Output
    //  instruction: Amount of time the user should spend in the poi, and the pointer of the link that the user should follow next
    sInstruction_t Coordinator::getInstruction(void *p){
        sInstruction_t instruction;
        sPOI* sp=static_cast<sPOI*>(p);
        int index=intuniform(0,sp->stayTimes.size()-1);
        instruction.stayTime=sp->stayTimes[index];
        if (sp->links.size()>0){
            instruction.deadEnd=false;
            index=intuniform(0,sp->links.size()-1);
            instruction.pLink=&(sp->links[index]);
            return instruction;
        }else{
            instruction.deadEnd=true;
        }
        return instruction;
    }

    //Give a random poi to the user at the start of the simulation
    //      Output
    //  pointer of initial poi
    void* Coordinator::getInitialPOI(){
        int index=intuniform(0,pPOIs.size()-1);
        return pPOIs[index];
    }

    void Coordinator::handleMessage(cMessage *msg){}
} //namespace
