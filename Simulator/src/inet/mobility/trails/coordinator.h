#ifndef __INET4_COORDINATOR_H_
#define __INET4_COORDINATOR_H_

#include <omnetpp.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <iterator>
#include <string>
#include <algorithm>

using namespace omnetpp;
using namespace std;

struct sPOI_t;
struct sContainer_t;

//Struct to group elements with same values
struct sOrgval_t{
    vector<int> activations;        /*Unique values*/
    vector<vector<int>> indexes;    /*Indexes with same values*/
};
//Link between 2 pois
struct sLink_t{
    vector<int> x;           //List of X coordinates
    vector<int> y;           //List of Y coordinates
    vector<int> deltaTime;   //List of time between consecutive link-points
    int totalTime;           //Period to arrive to next POI
    int activation;          //Time the link was used in real traces
    sContainer_t* parent;    //Pointer to the container (Careful reallocation)
};

/**
 * Container of links with the same source POI and destination POI
 */
struct sContainer_t{
    int ifinalPOI;                  /*Index of final poi (avoid reallocation problems)*/
    vector<sLink_t> links;          /*List of links with the same source POI and destination POI*/
    sOrgval_t ulinks;               /*Links grouped bay activation time*/
};

//Place where a user spends part of its time
struct sPOI_t{
    int centerX;                     //Coordinates of the poi
    int centerY;
    vector<int> stayPeriod;             //List of time intervals 2
    vector<int> stayActivation;         //List of time intervals 1
    sOrgval_t ustays;                   /*Stay times grouped bay activation time*/
    vector<sContainer_t> containers;    //List of containers of links with the destination POI
    vector<int> congestionNumber;       //Relative number of hosts in the POI 4
    vector<int> congestionTime;         //Time stamp of the congestion 3
    sOrgval_t ucongestion;              /*Congestion grouped bay activation time*/

};

/**
 * Flag used in random search algorithm
 */
enum dLim_t {
    LEFT = 0,   /*Closest smaller than*/
    CENTER = 1, /*Closest*/
    RIGHT = 2,  /*Closest bigger than*/
};

/**
 * Instruction sent to user
 */
struct sInstruction_t {
    int stayTime;
    sLink_t *link;
    sPOI_t *poi;
};

namespace inet {
    class Coordinator : public cSimpleModule{
        protected:
            unsigned int recordedTime; /*Time of the original traces*/
            int windowTime; /*Deviation time allowed for a desired activation time*/
            vector<sPOI_t> pois; /*List of pois*/
            vector<sPOI_t*> pPOIs;  /*List of pointers of active pois*/
            virtual void splitString(string *line, string *delimeter, vector<string> *vec);
            virtual void readMatrix(string fileName, vector<vector<string>> *dataList);
            virtual void toIntVector(vector<string> *vec, vector<int> *res);
            virtual void addLink(int poiIndex, int nextPOIIndex, sLink_t *link);
            virtual void addParent();
            virtual void groupContainers(sContainer_t *container);
            virtual void groupElements(vector<int> *activationTime, sOrgval_t *uvalues);
            virtual void groupPOIs();
            virtual void printGraph();
            virtual void initialize();
            virtual int random_search(std::vector<int> *list,int desired, int deviation, dLim_t dLimit);
            virtual int weghtedRandom(vector<int> *vweights);
            virtual int randomGroupedSearch(sOrgval_t *uValues, int desired, int deviation, dLim_t dLimit);
            virtual sLink_t *chooseLink(sContainer_t *container, int desired);
            virtual int getCongestion(sLink_t *link, int arrTime);
            virtual sLink_t *chooseDestination(sPOI_t *poi, int desired, int *arrTime);
            virtual int get_stayTime(sLink_t *link, int arrTime);
            virtual void handleMessage(cMessage *msg);
        public:
            sPOI_t *getInitialPOI();
            sInstruction_t getInstructions(sPOI_t *poi);
    };

}

#endif
