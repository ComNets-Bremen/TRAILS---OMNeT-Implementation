#ifndef __INET_USER_H
#define __INET_USER_H

#include "inet/common/INETDefs.h"
#include <omnetpp.h>
#include "inet/common/ModuleAccess.h"
#include <string>
#include "inet/mobility/base/LineSegmentsMobilityBase.h"
#include "inet/mobility/trails/coordinator.h"

using namespace omnetpp;
using namespace std;

namespace inet {
    class INET_API TRAILS : public LineSegmentsMobilityBase{
      protected:
        virtual void setInitialPosition() override;     //Get an initial random poi
        virtual int numInitStages() const override { return NUM_INIT_STAGES; }
        virtual void initialize(int stage) override;    //Start communication with the coordinator
        virtual void setTargetPosition() override;      //Go to the next position or ask to the coordinator next instruction
        virtual void move() override;
        int count;
        Coordinator *trailsFunctions;
        void* pPOI;
        sLink_t* pLink;
        sInstruction_t currentInstruction;
      public:
        TRAILS();
    };
} // namespace inet

#endif // ifndef __INET_RANDOMWPMOBILITY_H

