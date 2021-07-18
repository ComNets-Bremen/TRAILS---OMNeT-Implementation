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
        int count; /*Number of trace point in a link*/
        Coordinator *trailsFunctions; /*pointer to Coordinator module*/
        sPOI_t *pPOI; /*pointer to current POI*/
        sInstruction_t currentInstruction; /*Instruction received from the Coordinator module*/
        virtual void setInitialPosition() override;
        virtual int numInitStages() const override { return NUM_INIT_STAGES; }
        virtual void initialize(int stage) override;
        virtual void setTargetPosition() override;
        virtual void move() override;
      public:
        TRAILS();
    };
}

#endif

