package inet.examples.traces;

import inet.examples.mobility.MobileHost;

network TRACES
{
    parameters:
        int numUsers = default(1);
        int numGateways = default(0);
        @display("bgb=31568.2,19598.8");
    submodules:
        mobileHost[numUsers]: MobileHost {
            @display("p=96813.72,2689.27;is=vs");
        }
}
