#ifndef __INET4_COORDINATOR_H_
#define __INET4_COORDINATOR_H_

#include <omnetpp.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <iterator>
#include <string>
#include <algorithm>

#include <thread>

using namespace omnetpp;
using namespace std;

//Link between 2 pois
typedef struct sLink{
    vector<double> x;           //List of X coordinates
    vector<double> y;           //List of Y coordinates
    vector<double> deltaTime;   //List of time between consecutive link-points
    void* pNextPOI;        //Pointer of next poi
}sLink_t;

//Place where a user spends part of its time
typedef struct sPOI{
    vector<double> stayTimes;   //List of time intervals
    vector<sLink_t> links;      //List of links that a user can follow from that poi
    double centerX;             //Coordinates of the poi
    double centerY;
}sPOI_t;

//Order sent to a user every time the user arrives to a poi
typedef struct sIntruction{
    double stayTime;    //Amount of time the user should spend in the poi
    void* pLink;        //Pointer of the link that the user should follow next
    bool deadEnd;       //POI without links
}sInstruction_t;

namespace inet {
    class Coordinator : public cSimpleModule{
        protected:
            virtual vector<string> splitString(string line, string delimeter);  //Splits strings into vectors
            virtual vector<vector<string>> readMatrix(string fileName);         //Imports a CSV table
            virtual vector<double> toDoubleVector(vector<string> vec);          //Transforms a string vector into a double vector
            virtual void initialize();                                          //Loads the TRAILS graph from a file with pois and a file with links
            virtual void handleMessage(cMessage *msg);
            vector<sPOI_t> pois;                                                //List of pois
        public:
            vector<void*> pPOIs;                                                //List of pointers of active pois
            sInstruction_t getInstruction(void *p);                             //Give a instruction to a user every time it arrives to a poi
            void* getInitialPOI();                                              //Give a random poi to the user at the start of the simulation
    };

}

#endif
