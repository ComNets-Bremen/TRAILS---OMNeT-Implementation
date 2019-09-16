package inet.mobility.trails;
simple Coordinator
{
    string trailsFolder = default("");
    int mode = default(2);	//Behavior accordind cyclic paths
    //mode = 0 Simulate only paths with ways to return
    //mode = 1 Transform all paths into bidirectional paths
    //mode = 2 Transform to a bidirectional path only if there is no way to return
    bool includeUnrealistic = default(false);	//Include unrealistic paths
    bool enable = default(true);				//Enable coordinator functionality
    @display("i=status/yellow;is=n");
}
