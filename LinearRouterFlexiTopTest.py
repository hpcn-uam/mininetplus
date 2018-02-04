from mininetplus.topolib import LinearLinuxRouterTopo
from mininetplus.nodelib import HTTPServer, NAT
from mininetplus.net import Mininet
from mininet.log import setLogLevel
from mininetplus.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from time import sleep
import traceback


def main():
    n = 6
    samples = 1000
    topo = LinearLinuxRouterTopo(n=n, delays=[10+2*(i) for i in range(n-1)], lastNodeParams={'cls': NAT, 
        'inNamespace': False, 'subnet':'20.0/8'})
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    try:
        h0, hN = net.get('h0', 'hN')
        #net.iperf((h0, hN))
        #net.pingAll()
        CLI( net )
        raise ValueError('stop')
        intfs = {}
        for i, router in enumerate(net.routers()):
            intfs[str(router)] = [router.intfs[1]]
            print('Interfaces for router %d' % (i))
            print(router.intfs)
            print(router.intfs[1])

        print('Interfaces for h0')
        print(h0.intfs[0])
        #intfs[str(h0)] = [h0.intfs[0]]

        print('Interfaces for hN')
        print(hN.intfs[0])
        #intfs[str(hN)] = [hN.intfs[0]]


        for node, interfaces in intfs.iteritems():
            for intf in interfaces:
                print('TCPDump on %s' % intf)
                net.get(node).sendCmd('tcpdump -i %s -w ./%s.pcap' % (intf, intf))
        sleep(2)
        print('Generating traffic')
        for i in range(samples):
            h0.cmd('wget %s' % (hN.IP()))
            if (i % 50 == 0):
                print('Iteration %d' % i)
                sleep(1)
        sleep(10)

        print('Waiting for tcpdumps...')
        for node, intf in intfs.iteritems():
            net.get(node).sendInt()
            print('Waiting for %s...' % node)
            res = net.get(node).waitOutput()
            print(res)
       

        print('Processing pcaps...')
        for node, interfaces in intfs.iteritems():
            for intf in interfaces:
                print('Building %s.csv' % (intf))
                h0.cmd('python processPcap.py -i %s.pcap -o %s.csv' % (intf, intf))
        h0.cmd('rm -rf index.html*')
        h0.cmd('rm -rf wget-log*')
    except Exception as e:
        print('>>>> EXCEPTION <<<<')
        traceback.print_exc()

    net.stop()

    

if __name__ == '__main__':
    setLogLevel('info')
    main()

