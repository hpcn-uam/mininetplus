from mininetplus.linearTopo import LinearSwitchTopo
from mininetplus.HTTPServer import HTTPServer
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

def main():
    n = 5
    topo = LinearSwitchTopo(n=5, delays=[5*(i+1) for i in range(n)], lastNode=HTTPServer)
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    try:
        net.pingAll()
        h0, hN = net.get('h0', 'hN')
        #net.iperf((h0, hN))
        net.pingPairFull()

        for i, switch in enumerate(net.switches):
            print('Interfaces for switch %d' % (i))
            print(switch.intfs[1])
            print(switch.intfs[2])
        print('Interfaces for h0')
        print(h0.intfs[0])
        print('Interfaces for hN')
        print(hN.intfs[0])
        CLI(net)
    except Exception as e:
        print('>>>> EXCEPTION <<<<')
        print(e)

    net.stop()

    

if __name__ == '__main__':
    setLogLevel('info')
    main()

