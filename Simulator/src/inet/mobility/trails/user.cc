//User behavior for the TRAILS model
#include "user.h"

namespace inet {

    Define_Module(TRAILS);

    TRAILS::TRAILS(){}
    /**
     * Get an initial random poi
     */
    void TRAILS::setInitialPosition(){
        pPOI = trailsFunctions->getInitialPOI();
        lastPosition.x=pPOI->centerX;
        lastPosition.y=pPOI->centerY;
        lastPosition.z=0;
        currentInstruction = trailsFunctions->getInstructions(pPOI);
        count = 0;
        targetPosition.x=pPOI->centerX;
        targetPosition.y=pPOI->centerY;
        targetPosition.z=0;
        nextChange=simTime()+1;
    }

    /**
     * Start communication with the coordinator
     * @param stage phase of initialization
     */
    void TRAILS::initialize(int stage){
        LineSegmentsMobilityBase::initialize(stage);
        if (stage==1){
            cModule *coordinator = getParentModule()->getParentModule()->getSubmodule("coordinator");
            trailsFunctions = check_and_cast<Coordinator *>(coordinator);
        }
    }

    /**
     * Go to the next position or ask to the coordinator next instruction
     */
    void TRAILS::setTargetPosition(){
        if (count<currentInstruction.link->x.size()){
            targetPosition.x=currentInstruction.link->x.at(count);
            targetPosition.y=currentInstruction.link->y.at(count);
            nextChange=simTime()+currentInstruction.link->deltaTime.at(count);
            count++;
        }else{
            nextChange=simTime()+currentInstruction.stayTime;
            pPOI = currentInstruction.poi;
            count = 0;
            currentInstruction = trailsFunctions->getInstructions(pPOI);
        }
    }

    void TRAILS::move(){
        LineSegmentsMobilityBase::move();
    }
}

