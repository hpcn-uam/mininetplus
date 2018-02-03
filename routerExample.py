#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininetplus.linearTopo import LinearLinuxRouterTopo
from mininetplus.link import TCLink
from mininetplus.HTTPServer import HTTPServer


class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
    "A LinuxRouter connecting three IP subnets"

    def build( self, **_opts ):

        defaultIP = '10.0.0.100/24'  # IP address for r0-eth1
        router = self.addNode( 'r0', cls=LinuxRouter, ip= '192.168.1.1/24', defaultRoute='via 10.0.0.1' )

        h1 = self.addHost( 'h1', ip='192.168.1.100/24',
                           defaultRoute='via 192.168.1.1' )
        h2 = self.addHost( 'h2', ip='192.168.2.100/24',
                           defaultRoute='via 192.168.2.1' )
        router2 = self.addNode( 'r1', cls=LinuxRouter, ip='10.0.0.1/24', defaultRoute='via 10.0.0.100')

                
        self.addLink( h1, router, intfName2='r0-eth1',
                      params2={ 'ip' : '192.168.1.1/24' } )  # for clarity
        self.addLink( h2, router, intfName2='r0-eth2',
                      params2={ 'ip' : '192.168.2.1/24' } )  # for clarity
        self.addLink( router, router2,  intfName1='r0-eth8',
                      params1={ 'ip' : '10.0.0.100/24' }, intfName2='r1-eth7',
                      params2={ 'ip' : '10.0.0.1/24' } )  # for clarity
        print(self.g.node)
        print(self.g.edge)


def run():
    "Test linux router"
    n = 6
    samples = 100
    topo = LinearLinuxRouterTopo(n=n, delays=[10+2*(i) for i in range(n-1)], lastNode=HTTPServer)
    #topo = NetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    info( '*** Routing Table on Router:\n' )
    #info( net[ 'r0' ].cmd( 'route' ) )
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()