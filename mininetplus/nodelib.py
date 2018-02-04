from mininet.nodelib import *
from mininetplus.node import *

class HTTPServer(Host):

    def config(self, **params):
        super(HTTPServer, self).config(**params)
        # Enable HTTP server on port 80
        self.pid_file = '%s.pid' % (self.name)
        print(self.cmd('python -m SimpleHTTPServer 80 > http_log 2>&1 & echo $! > %s' % (self.pid_file)))
    
    def terminate(self):
        # Stop HTTP Server
        self.cmd('kill -9 `cat %s`' % self.pid_file)
        self.cmd('rm %s' % self.pid_file)
        super(HTTPServer, self).terminate()
            
class Router(Host):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(Router, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')
        

    def terminate(self):
        # Disable ip forwarding
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(Router, self).terminate()

class NAT(Node):
    "NAT: Provides connectivity to external network"

    def __init__( self, name, subnet='10.0/8',
                  localIntf=None, flush=False, **params):
        """Start NAT/forwarding between Mininet and external network
           subnet: Mininet subnet (default 10.0/8)
           flush: flush iptables before installing NAT rules"""
        super( NAT, self ).__init__( name, **params )

        self.subnet = subnet
        self.localIntf = localIntf
        self.flush = flush
        self.forwardState = self.cmd( 'sysctl -n net.ipv4.ip_forward' ).strip()

    def config( self, **params ):
        """Configure the NAT and iptables"""
        super( NAT, self).config( **params )

        if not self.localIntf:
            self.localIntf = self.defaultIntf()

        if self.flush:
            self.cmd( 'sysctl net.ipv4.ip_forward=0' )
            self.cmd( 'iptables -F' )
            self.cmd( 'iptables -t nat -F' )
            # Create default entries for unmatched traffic
            self.cmd( 'iptables -P INPUT ACCEPT' )
            self.cmd( 'iptables -P OUTPUT ACCEPT' )
            self.cmd( 'iptables -P FORWARD DROP' )

        # Install NAT rules
        self.cmd( 'iptables -I FORWARD',
                  '-i', self.localIntf, '-d', self.subnet, '-j DROP' )
        self.cmd( 'iptables -A FORWARD',
                  '-i', self.localIntf, '-s', self.subnet, '-j ACCEPT' )
        self.cmd( 'iptables -A FORWARD',
                  '-o', self.localIntf, '-d', self.subnet, '-j ACCEPT' )
        self.cmd( 'iptables -t nat -A POSTROUTING',
                  '-s', self.subnet, "'!'", '-d', self.subnet,
                  '-j MASQUERADE' )

        # Instruct the kernel to perform forwarding
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

        # Prevent network-manager from messing with our interface
        # by specifying manual configuration in /etc/network/interfaces
        intf = self.localIntf
        cfile = '/etc/network/interfaces'
        line = '\niface %s inet manual\n' % intf
        config = open( cfile ).read()
        if ( line ) not in config:
            info( '*** Adding "' + line.strip() + '" to ' + cfile + '\n' )
            with open( cfile, 'a' ) as f:
                f.write( line )
        # Probably need to restart network-manager to be safe -
        # hopefully this won't disconnect you
        self.cmd( 'service network-manager restart' )

    def terminate( self ):
        "Stop NAT/forwarding between Mininet and external network"
        # Remote NAT rules
        self.cmd( 'iptables -D FORWARD',
                   '-i', self.localIntf, '-d', self.subnet, '-j DROP' )
        self.cmd( 'iptables -D FORWARD',
                  '-i', self.localIntf, '-s', self.subnet, '-j ACCEPT' )
        self.cmd( 'iptables -D FORWARD',
                  '-o', self.localIntf, '-d', self.subnet, '-j ACCEPT' )
        self.cmd( 'iptables -t nat -D POSTROUTING',
                  '-s', self.subnet, '\'!\'', '-d', self.subnet,
                  '-j MASQUERADE' )
        # Put the forwarding state back to what it was
        self.cmd( 'sysctl net.ipv4.ip_forward=%s' % self.forwardState )
        super( NAT, self ).terminate()

