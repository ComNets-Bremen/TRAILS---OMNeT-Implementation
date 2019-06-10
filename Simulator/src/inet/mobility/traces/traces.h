#ifndef __INET_TRACES_H
#define __INET_TRACES_H

#include <omnetpp.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <iterator>
#include <string>
#include <algorithm>
#include "inet/common/INETDefs.h"
#include "inet/common/ModuleAccess.h"
#include "inet/mobility/base/LineSegmentsMobilityBase.h"

using namespace omnetpp;
using namespace std;

namespace inet {
    class INET_API TRACES : public LineSegmentsMobilityBase{
        protected:
            virtual vector<string> splitString(string line, string delimeter);      //Splits strings into vectors
            virtual vector<vector<double>> readMatrix(string filename);             //Reads a trace from a file
            virtual void setInitialPosition() override;                             //It starts at the beginning at the trace
            virtual int numInitStages() const override { return NUM_INIT_STAGES; }
            virtual void initialize(int stage) override;                            //Assigns a trace to the user and it imports the trace
            virtual void setTargetPosition() override;                              //When it arrives to a new position it chooses the next point in the trace
            virtual void move() override;
            vector<vector<double>> dbpositions;                                     //List with the trace-points
            unsigned int count;                                                     //Identifier of the current trace-point
        public:
            TRACES();
    };
} // namespace inet

#endif // ifndef __INET_RANDOMWPMOBILITY_H

