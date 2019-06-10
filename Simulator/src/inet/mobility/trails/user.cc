//User behavior for the TRAILS model
#include "user.h"

namespace inet {

    Define_Module(TRAILS);

    TRAILS::TRAILS(){}
    //Get an initial random poi
    void TRAILS::setInitialPosition(){
        pPOI = trailsFunctions->getInitialPOI();
        sPOI* sp = static_cast<sPOI*>(pPOI);
        lastPosition.x=sp->centerX;
        lastPosition.y=sp->centerY;
        lastPosition.z=0;
        currentInstruction=trailsFunctions->getInstruction(pPOI);
        if (not currentInstruction.deadEnd){
            pLink = static_cast<sLink_t*>(currentInstruction.pLink);
        }
        targetPosition.x=sp->centerX;
        targetPosition.y=sp->centerY;
        targetPosition.z=0;
        nextChange=simTime()+currentInstruction.stayTime;
        count = 0;
    }
    //Start communication with the coordinator
    void TRAILS::initialize(int stage){
        LineSegmentsMobilityBase::initialize(stage);
        if (stage==1){
            auto coordinator = getParentModule()->getParentModule()->getSubmodule("coordinator");
            trailsFunctions = check_and_cast<Coordinator *>(coordinator);
        }
    }
    //Go to the next position or ask to the coordinator next instruction
    void TRAILS::setTargetPosition(){
        if (not currentInstruction.deadEnd){
            if (count<pLink->x.size()){
                targetPosition.x=pLink->x[count];
                targetPosition.y=pLink->y[count];
                nextChange=simTime()+pLink->deltaTime[count];
                count++;
            }else{
                pPOI=pLink->pNextPOI;
                currentInstruction=trailsFunctions->getInstruction(pPOI);
                if (not currentInstruction.deadEnd){
                    pLink = static_cast<sLink_t*>(currentInstruction.pLink);
                }
                nextChange=simTime()+currentInstruction.stayTime;
                count=0;
            }
        }else{
            nextChange=simTime()+currentInstruction.stayTime;
        }
        sPOI* sp = static_cast<sPOI*>(pPOI);

    }

    void TRAILS::move(){
        LineSegmentsMobilityBase::move();
    }
} // namespace inet

