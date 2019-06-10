package inet.examples.trails;

import inet.examples.mobility.MobileHost;
import inet.mobility.trails.Coordinator;


network Trails
{
    parameters:
        int numHosts = default(1);

    submodules:
        coordinator: Coordinator {
            @display("p=163,174;i=status/yellow");
        }
        mobileHost[numHosts]: MobileHost {
            @display("p=200,200;is=vs");
        }
}
