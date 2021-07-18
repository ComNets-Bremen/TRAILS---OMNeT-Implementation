package inet.mobility.trails;
simple Coordinator
{
    string trailsFolder = default("");
    bool includeUnrealistic = default(false);	//Include unrealistic paths
    bool enable = default(true);				//Enable coordinator functionality
    int recordedTime @unit(s) = default(0s);	//Total recorded time
    int windowTime @unit(s) = default(-1s);	//Total recorded time
    @display("i=status/yellow;is=n");
}
