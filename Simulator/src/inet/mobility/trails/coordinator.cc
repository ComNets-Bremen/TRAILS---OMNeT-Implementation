//Send links and pois to users
#include "coordinator.h"
namespace inet {

    Define_Module(Coordinator);

    /**
     * Splits strings into vectors
     * @param line pointer to Input String
     * @param delimeter pointer to substring delimeter
     * @param vec pointer with the list of the returned substrings
     */
    void Coordinator::splitString(string *line, string *delimiter, vector<string> *vec) {
        vec->clear();
        size_t pos = 0;
        while ((pos = line->find(*delimiter)) != string::npos) {
            vec->push_back(line->substr(0, pos));
            line->erase(0, pos + delimiter->length());
        }
        vec->push_back(*line);
    }

    /**
     * Imports a CSV table
     * @param fileName adress of the CSV file
     * @param dataList matrix of the parsed CSV table
     */
    void Coordinator::readMatrix(string fileName, vector<vector<string>> *dataList) {
        dataList->clear();
        static string delimiter = " ";
        ifstream file(fileName);
        string line = "";
        vector<string> vec;
        while (getline(file, line)){
            vec.clear();
            splitString(&line, &delimiter, &vec);
            dataList->push_back(vec);
        }
        file.close();
    }

    //Transforms a string vector into a double vector
    //      Input
    //  vec: String vector
    //      Output
    //  res: Double vector
    /**
     * Transforms a string vector into an int vector
     */
    void Coordinator::toIntVector(vector<string> *vec, vector<int> *res){
        res->clear();
        for (unsigned int i=0;i<vec->size();i++){
            res->push_back(stoi(vec->at(i)));
        }
    }

    /**
     * Adds a link to container
     * @param poiIndex index of initial poi
     * @param nextPOIIndex index of final poi
     * @param link element to insert in the container
     */
    void Coordinator::addLink(int poiIndex, int nextPOIIndex, sLink_t *link){
        bool found=false;
        sContainer_t *pcontainer;
        for(int i=0;not(found)&&i<pois.at(poiIndex).containers.size();i++){
            if (pois.at(poiIndex).containers.at(i).ifinalPOI==nextPOIIndex){
                pcontainer=&pois.at(poiIndex).containers.at(i);
                found=true;
                break;
            }
        }
        if (not(found)){
            pois.at(poiIndex).containers.push_back(sContainer_t());
            pcontainer=&pois.at(poiIndex).containers.back();
            pcontainer->ifinalPOI=nextPOIIndex;
        }
        pcontainer->links.push_back(*link);

    }

    /**
     * Add the parent pointer on each link
     * It is done after all elements are allocated to avoid invalid pointers because of vector reallocation
     */
    void Coordinator::addParent(){
        for(int i=0;i<pPOIs.size();i++){
            for(int j=0;j<pPOIs.at(i)->containers.size();j++){
                sContainer_t *cont = &pPOIs.at(i)->containers.at(j);
                for(int h=0;h<cont->links.size();h++){
                    cont->links.at(h).parent = cont;
                }
            }
        }
    }

    /**
     * Group indexes of elements with the same activation time in different arrays
     * @param activationTime pointer to list of activation times
     * @param uvalues pointer to struct to group elements with same values
     */
    void Coordinator::groupElements(vector<int> *activationTime, sOrgval_t *uval){
        sOrgval_t uvalues;
        uvalues.activations.push_back(activationTime->at(0));
        uvalues.indexes.push_back(vector<int>());
        for (int i=0;i<activationTime->size();i++){
            if (activationTime->at(i)!=uvalues.activations.back()){
                uvalues.activations.push_back(activationTime->at(i));
                uvalues.indexes.push_back(vector<int>());
            }
            uvalues.indexes.back().push_back(i);
        }
        for (int i=0;i<uvalues.indexes.size();i++){
            for (int j=0;j<uvalues.indexes.at(i).size();j++){
                uval->activations.push_back(uvalues.activations.at(i));
                uval->indexes.push_back(uvalues.indexes.at(i));
            }
        }
    }

    /**
     * Group indexes of links with the same activation time in different arrays
     * @param container pointer to container of links
     */
    void Coordinator::groupContainers(sContainer_t *container){
        sOrgval_t uvalues;
        uvalues.activations.push_back(container->links.at(0).activation);
        uvalues.indexes.push_back(vector<int>());
        for (int i=0;i<container->links.size();i++){
            if (container->links.at(i).activation!=uvalues.activations.back()){
                uvalues.activations.push_back(container->links.at(i).activation);
                uvalues.indexes.push_back(vector<int>());
            }
            uvalues.indexes.back().push_back(i);
        }
        for (int i=0;i<uvalues.indexes.size();i++){
            for (int j=0;j<uvalues.indexes.at(i).size();j++){
                container->ulinks.activations.push_back(uvalues.activations.at(i));
                container->ulinks.indexes.push_back(uvalues.indexes.at(i));
            }
        }
    }

    /**
     * Group stay periods, congestion, and links by same activation time
     */
    void Coordinator::groupPOIs(){
        for (int i=0; i<pPOIs.size(); i++){
            groupElements(&pPOIs.at(i)->stayActivation, &pPOIs.at(i)->ustays);
            groupElements(&pPOIs.at(i)->congestionTime, &pPOIs.at(i)->ucongestion);
            for (int j=0;j<pPOIs.at(i)->containers.size();j++){
                groupContainers(&pPOIs.at(i)->containers.at(j));
            }
        }
    }

    /**
     * Prints the loaded TRAILS graph
     */
    void Coordinator::printGraph(){
        for (int i=0;i<pPOIs.size();i++){
            sPOI_t* sp=pPOIs.at(i);
            EV<<"POI "<<i<<'\n';
            EV<<"Stay (Activation,Period)"<<'\n';
            for (int j=0;j<sp->stayActivation.size();j++){
                EV<<" , "<<sp->stayActivation.at(j);
            }
            EV<<'\n';
            for (int j=0;j<sp->stayActivation.size();j++){
                EV<<" , "<<sp->stayPeriod.at(j);
            }
            EV<<'\n';
            EV<<"U_Stay (Activation,indexes)"<<'\n';
            for (int j=0;j<sp->ustays.activations.size();j++){
                EV<<" , "<<sp->ustays.activations.at(j);
            }
            EV<<'\n';
            for (int j=0;j<sp->ustays.activations.size();j++){
                for (int h=0;h<sp->ustays.indexes.at(j).size();h++){
                    EV<<" , "<<sp->ustays.indexes.at(j).at(h);
                }
                /*
                EV<<";";
                if(sp->ustays.indexes.at(j).size()>1){
                    char text[128];
                    sprintf(text, "Same stay activation time %d", i);
                    getSimulation()->getActiveEnvir()->alert(text);
                }
                */
            }
            EV<<'\n';
            EV<<"Congestion (Activation,Users)"<<'\n';
            for (int j=0;j<sp->congestionTime.size();j++){
                EV<<" , "<<sp->congestionTime.at(j);
            }
            EV<<'\n';
            for (int j=0;j<sp->congestionTime.size();j++){
                EV<<" , "<<sp->congestionNumber.at(j);
            }
            EV<<'\n';
            EV<<"U_Congestion (Activation,indexes)"<<'\n';
            for (int j=0;j<sp->ucongestion.activations.size();j++){
                EV<<" , "<<sp->ucongestion.activations.at(j);
            }
            EV<<'\n';
            for (int j=0;j<sp->ucongestion.activations.size();j++){
                for (int h=0;h<sp->ucongestion.indexes.at(j).size();h++){
                    EV<<" , "<<sp->ucongestion.indexes.at(j).at(h);
                }
                EV<<";";
                /*
                if(sp->ucongestion.indexes.at(j).size()>1){
                    char text[128];
                    sprintf(text, "Same congestion activation time %d", i);
                    getSimulation()->getActiveEnvir()->alert(text);
                }
                */
            }
            EV<<'\n';
            for (int j=0;j<sp->containers.size();j++){
                EV<<"Container (Activation)"<<'\n';
                for (int h=0;h<sp->containers.at(j).links.size();h++){
                    sLink_t plink = sp->containers.at(j).links.at(h);
                    EV<<" , "<<plink.activation;
                }
                EV<<'\n';
                EV<<"U_Container (Activation,indexes)"<<'\n';
                for (int h=0;h<sp->containers.at(j).ulinks.activations.size();h++){
                    EV<<" , "<<sp->containers.at(j).ulinks.activations.at(h);
                }
                EV<<'\n';
                for (int h=0;h<sp->containers.at(j).ulinks.activations.size();h++){
                    for (int k=0;k<sp->containers.at(j).ulinks.indexes.at(h).size();k++){
                        EV<<" , "<<sp->containers.at(j).ulinks.indexes.at(h).at(k);
                    }
                    EV<<";";
                    /*
                    if(sp->containers.at(j).ulinks.indexes.at(h).size()>1){
                        char text[128];
                        sprintf(text, "Same link activation time %d", i);
                        getSimulation()->getActiveEnvir()->alert(text);
                    }
                    */
                }
                EV<<'\n';
            }
        }
    }

    /**
     * It loads the TRAILS graph
     */
    void Coordinator::initialize(){
        bool enable = par("enable");
        if (enable){
            recordedTime = par("recordedTime");
            windowTime = par("windowTime");
            bool includeUnrealistic = par("includeUnrealistic");
            const char *trailsFolder=par("trailsFolder").stringValue();
            string trailsDirectory(trailsFolder);
            vector<vector<string>> dataList;
            readMatrix(trailsDirectory+"/POIs.csv",&dataList);

            for (unsigned int i=0;i<dataList.size()-4;i+=5){
                sPOI_t poi;
                poi.centerX=stoi(dataList.at(i).at(0));
                poi.centerY=stoi(dataList.at(i).at(1));
                toIntVector(&dataList.at(i+1),&poi.stayActivation);
                toIntVector(&dataList.at(i+2),&poi.stayPeriod);
                toIntVector(&dataList.at(i+3),&poi.congestionTime);
                toIntVector(&dataList.at(i+4),&poi.congestionNumber);
                poi.containers=vector<sContainer_t>();
                pois.push_back(poi);
            }
            /* Read Links */
            readMatrix(trailsDirectory+"/Links.csv",&dataList);
            for (unsigned int i=0;i<dataList.size()-3;i+=4){
                bool linkUnrealistic = stoi(dataList.at(i).at(2))==1;
                if (includeUnrealistic || (not linkUnrealistic)){
                    vector<int> deltaTime;
                    toIntVector(&dataList.at(i+1),&deltaTime);
                    vector<int> x;
                    vector<int> y;
                    if (deltaTime.size()>1){
                        toIntVector(&dataList.at(i+2),&x);
                        toIntVector(&dataList.at(i+3),&y);
                    }
                    bool linkReturn;
                    if (includeUnrealistic){
                        linkReturn=stoi(dataList.at(i).at(3))==1;
                    }else{
                        linkReturn=stoi(dataList.at(i).at(4))==1;
                    }
                    int poiIndex=stoi(dataList.at(i).at(0));
                    int nextPOIIndex=stoi(dataList.at(i).at(1));
                    int totalTime=stoi(dataList.at(i).at(5));   /*Time spent in a link*/
                    int activationTime=stoi(dataList.at(i).at(6));
                    sLink_t link;
                    link.x=x;
                    link.x.push_back(pois.at(nextPOIIndex).centerX);
                    link.y=y;
                    link.y.push_back(pois.at(nextPOIIndex).centerY);
                    link.deltaTime=deltaTime;
                    link.totalTime=totalTime;
                    link.activation=activationTime;
                    addLink(poiIndex, nextPOIIndex, &link);
                    if (not(linkReturn)){
                        sLink_t rLink;
                        rLink.x=x;
                        reverse(rLink.x.begin(),rLink.x.end());
                        rLink.x.push_back(pois.at(poiIndex).centerX);
                        rLink.y=y;
                        reverse(rLink.y.begin(),rLink.y.end());
                        rLink.y.push_back(pois.at(poiIndex).centerY);
                        rLink.deltaTime=deltaTime;
                        reverse(rLink.deltaTime.begin(),rLink.deltaTime.end());
                        rLink.totalTime=totalTime;
                        rLink.activation=0;
                        addLink(nextPOIIndex, poiIndex, &rLink);
                    }
                }
            }
            /* Get pointers of valid POIs */
            for (unsigned int i=0;i<pois.size();i++){
                if(pois.at(i).containers.size()>0){
                    pPOIs.push_back(&pois.at(i));
                }
            }
            groupPOIs();
            addParent();
            //printGraph();
        }
    }

    /**
     * Give a random poi to the user at the start of the simulation
     * @return poi pointer to poi
     */
    sPOI_t *Coordinator::getInitialPOI(){
        int index=intuniform(0,pPOIs.size()-1);
        return pPOIs[index];
    }

    /**
     * Searches for a value in ascending ordered list
     * @param list pointer of the list
     * @param desired desired value
     * @param deviation accepted error between the desired value and the value to be found
     * @param dLimit if a value is not found return lIndex if LEFT, return hIndex if RIGHT, or return closest value if CENTER
     * @return rIndex Index of the value found by the algorithm
     */
    int Coordinator::random_search(std::vector<int> *list,int desired, int deviation, dLim_t dLimit){
        int hIndex=list->size();
        if (list->at(hIndex-1)<=(desired-deviation)){
            return hIndex-1;
        }
        int lIndex=-1;
        if (list->at(lIndex+1)>=(desired+deviation)){
            return lIndex+1;
        }
        int rIndex;
        //int deb=0;
        while (hIndex-lIndex>1){
            /*
            deb++;
            if(deb>1 && dLimit==CENTER){
                char text[128];
                sprintf(text, "search round %d", deb);
                getSimulation()->getActiveEnvir()->alert(text);
            }
            */
            rIndex=intuniform(lIndex+1,hIndex-1);
            if (abs(list->at(rIndex)-desired)<=deviation){
                return rIndex;
            }
            if(list->at(rIndex)>(desired+deviation)){
                hIndex=rIndex;
            }else{
                lIndex=rIndex;
            }
        }
        if (lIndex==-1) lIndex=0;
        if (hIndex==int(list->size())) hIndex-=1;
        switch(dLimit){
        case LEFT:
            return lIndex;
        case RIGHT:
            return hIndex;
        default:
            return (abs(list->at(hIndex)-desired)<abs(desired-list->at(lIndex))) ? hIndex:lIndex;
        }
    }

    /**
     * Chooses a random element from a list with weights
     * @param vweights pointer o a list with weights
     * @return rIndex index of the random element
     */
    int Coordinator::weghtedRandom(vector<int> *vweights){
        static std::vector<int> vsum;
        vsum.clear();
        vsum.reserve(vweights->size());
        int sum=0;
        for (int i=0;i<int(vweights->size());i++){
            sum+=((vweights->at(i)<<5)+1);
            vsum.push_back(sum);
        }
        int randval=intuniform(1,sum);
        return random_search(&vsum,randval, 0, RIGHT);
    }

    /**
     * Searches for a value in an ascending ordered list of grouped values by unique keys
     * @param uValues object with grouped values by unique keys
     * @param desired desired value
     * @param deviation accepted error between the desired value and the value to be found
     * @param dLimit if a value is not found return lIndex if LEFT, return hIndex if RIGHT, or return closest value if CENTER
     * @return cIndex Index of the value found by the algorithm
     */
    int Coordinator::randomGroupedSearch(sOrgval_t *uValues, int desired, int deviation, dLim_t dLimit){
        int aIndex = random_search(&uValues->activations, desired, deviation, dLimit);
        int iIndex = intuniform(0,uValues->indexes.at(aIndex).size()-1);
        return uValues->indexes.at(aIndex).at(iIndex);
    }

    /**
     * Chooses a link based on the simulation time
     * @param container pointer to a container of links
     */
    sLink_t *Coordinator::chooseLink(sContainer_t *container, int desired){
        int cIndex;
        if (windowTime>=0){
            cIndex = randomGroupedSearch(&container->ulinks, desired, windowTime, CENTER);
        }else{
            cIndex = intuniform(0,container->links.size()-1);
        }
        return &container->links.at(cIndex);
    }

    /**
     *  Finds the congestion of a finalPoi if a link is taken
     *  @param link pointer to the link
     *  @param arrTime Time of arrival
     *  @return congestion number of nodes in a poi
     */
    int Coordinator::getCongestion(sLink_t *link, int arrTime){
        int ifinalPOI = link->parent->ifinalPOI;
        int cIndex = randomGroupedSearch(&pois.at(ifinalPOI).ucongestion, arrTime, 0, LEFT);
        return pois.at(ifinalPOI).congestionNumber.at(cIndex);
    }

    /**
     *  Chooses a poi as a destination based on the congestion
     *  @param poi pointer to the initialPoi
     *  @param desired current relative time
     *  @param arrtime pointer to time of arrival
     *  @return rlink pointer to a link with the chosen finalPoi
     */
    sLink_t *Coordinator::chooseDestination(sPOI_t *poi, int desired, int *arrTime){
        std::vector<sLink_t*> curLinks;
        curLinks.reserve(poi->containers.size());
        std::vector<int> arrTimes;
        arrTimes.reserve(poi->containers.size());
        for(int i=0;i<poi->containers.size();i++){
            /*  get one link per destination and estimate the arrival times*/
            curLinks.push_back(chooseLink(&poi->containers.at(i),desired));
            arrTimes.push_back((desired+curLinks.at(i)->totalTime)%recordedTime);
        }
        std::vector<int> congestions;
        congestions.reserve(poi->containers.size());
        for(int i=0;i<poi->containers.size();i++){  /* get the congestion of each link */
            congestions.push_back(getCongestion(curLinks.at(i), arrTimes.at(i)));
        }
        int lIndex = weghtedRandom(&congestions);   /* choose destination */
        //int lIndex = intuniform(0,congestions.size()-1);
        *arrTime = arrTimes.at(lIndex);
        return curLinks.at(lIndex);
    }

    /**
     * Chooses a random stay time based on a estimated time of arrival
     * @param link pointer to the link to be followed
     * @param arrTime Time of arrival
     * @return stayTime time a user would stay in the finalPoi
     */
    int Coordinator::get_stayTime(sLink_t *link, int arrTime){
        int ifinalPOI = link->parent->ifinalPOI;
        int cIndex;
        if (windowTime>=0){
            cIndex = randomGroupedSearch(&pois.at(ifinalPOI).ustays, arrTime, windowTime, CENTER);
        }else{
            cIndex = intuniform(0,pois.at(ifinalPOI).stayPeriod.size()-1);
        }
        return pois.at(ifinalPOI).stayPeriod.at(cIndex);
    }

    /**
     * Chooses the link and the stay time that the user should follow
     * @param poi pointer to current poi
     * @return an instruction for the user
     */
    sInstruction_t Coordinator::getInstructions(sPOI_t *poi){
        int desired = simTime().inUnit(SIMTIME_S) % recordedTime;
        int arrTime;
        sInstruction_t inst;
        inst.link = chooseDestination(poi, desired, &arrTime);
        inst.poi = &pois.at(inst.link->parent->ifinalPOI);
        inst.stayTime = get_stayTime(inst.link, arrTime);
        return inst;
    }

    void Coordinator::handleMessage(cMessage *msg){}
}
