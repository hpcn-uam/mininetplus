from mininetplus.topolib import LinearSwitchTopo
from mininetplus.nodelib import HTTPServer, NAT
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from time import sleep
import traceback


def main():
    n = 6
    samples = 1000
    topo = LinearSwitchTopo(n=n, delays=[10+2*(i) for i in range(n-1)], lastNode=NAT)
    net = Mininet(topo=topo, link=TCLink)
    net.addNAT().configDefault()

    net.start()
    
    try:
        #net.pingAll()
        h0, hN = net.get('h0', 'hN')
        #net.iperf((h0, hN))
        #net.pingPairFull()
        CLI(net)
        intfs = {}
        for i, switch in enumerate(net.switches):
            intfs[str(switch)] = [switch.intfs[1]]
            print('Interfaces for switch %d' % (i))
            print(switch.intfs[1])
            print(switch.intfs[2])
        print('Interfaces for h0')
        print(h0.intfs[0])
        #intfs[str(h0)] = [h0.intfs[0]]

        print('Interfaces for hN')
        print(hN.intfs[0])
        #intfs[str(hN)] = [hN.intfs[0]]
        raise ValueError('stop')
        for node, interfaces in intfs.iteritems():
            for intf in interfaces:
                print('TCPDump on %s' % intf)
                net.get(node).sendCmd('tcpdump -i %s -w ./%s.pcap' % (intf, intf))
        sleep(5)

        print('Generating traffic')
        for i in range(samples):
            h0.cmd('wget %s' % (hN.IP()))
            if (i % 100 == 0):
                print('Iteration %d' % i)
                sleep(1)
        sleep(10)

        print('Waiting for tcpdumps...')
        for node, intf in intfs.iteritems():
            net.get(node).sendInt()
            print('Waiting for %s...' % node)
            res = net.get(node).waitOutput()
       

        print('Processing pcaps...')
        for node, interfaces in intfs.iteritems():
            for intf in interfaces:
                print('Building %s.csv' % (intf))
                h0.cmd('python processPcap.py -i %s.pcap -o %s.csv' % (intf, intf))
        h0.cmd('rm index.html.*')
        h0.cmd('rm wget-log.*')
    except Exception as e:
        print('>>>> EXCEPTION <<<<')
        traceback.print_exc()

    net.stop()

    

if __name__ == '__main__':
    setLogLevel('debug')
    main()

