package inet.mobility.traces;
import inet.mobility.base.MovingMobilityBase;
simple TRACES extends MovingMobilityBase
{
    parameters:
		string csvFolder = default("");	//Folder with traces
		bool initFromDisplayString = default(true); 
        @class(TRACES);
}