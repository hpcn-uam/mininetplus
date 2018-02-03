from mininetplus.AbstractTopo import AbstractTopo
from mininetplus.node import Node, Router

class LinearSwitchTopo(AbstractTopo):
    def __init__(self, n=3, delays=[5, 10], firstNode=None, lastNode=None):
        self.n = n
        self.delays = delays
        self.firstNode = firstNode
        self.lastNode = lastNode
        super(LinearSwitchTopo, self).__init__()

    def build(self, **_opts):
        n = self.n
        delays = self.delays
        firstNode = self.firstNode
        lastNode = self.lastNode

        if firstNode is not None:
            h0 = self.addHost('h0', cls=firstNode)
        else:
            h0 = self.addHost('h0')

        s_old = h0
        for i in range(n-2):
            s_new = self.addSwitch('s%d' % (i+1))
            if s_old:
                self.addLink(s_old, s_new, delay='%dms' % (delays[i]))
            s_old = s_new
            hi = self.addHost('h%d' % (i+1))
            self.addLink(s_new, hi)

        if lastNode is not None:
            hN = self.addHost('hN', cls=lastNode)
        else:
            hN = self.addHost('hN')
        switches = self.switches()
        self.addLink(switches[0], h0, delay='%dms' % (delays[0]))
        self.addLink(switches[-1], hN, delay='%dms' % (delays[-1]))


class LinearLinuxRouterTopo(AbstractTopo):
    ip_counter3 = 20
    ip_counter2 = 0
    ip_counter1 = 0
   

    def __init__(self, n=3, delays=[5, 10], firstNode=None, lastNode=None):
        self.n = n
        self.delays = delays
        self.firstNode = firstNode
        self.lastNode = lastNode
        super(LinearLinuxRouterTopo, self).__init__()

    def build(self, **_opts):
        n = self.n
        delays = self.delays
        firstNode = self.firstNode
        lastNode = self.lastNode

        s_oldbytes = self.getAnotherIP()

        h0 = None

        if firstNode is not None:
            h0 = self.addHost('h0', cls=firstNode, ip='%d.%d.%d.100/24' % s_oldbytes)
        else:
            h0 = self.addHost('h0', ip='%d.%d.%d.100/24' % s_oldbytes, cls=Node)

        s_old = h0
        routes = []
        routes_intf = []

        # Add default route to h0
        routes_intf.append(('add 0.0.0.0/0 via %d.%d.%d.1 dev '  % s_oldbytes)  + ('%s-main' % s_old))
        self.nodeSetRoutes(s_old, routes_intf)

        for i in range(n-2):
            # Create new host
            s_new = self.addRouter('r%d' % (i+1), ip='%d.%d.%d.1/24' % s_oldbytes)
            if s_old:
                self.addLink(s_old, s_new, delay='%dms' % (delays[i]),
                intfName1='%s-main' % s_old, 
                params1={
                    'ip': '%d.%d.%d.100/24' % s_oldbytes
                },
                intfName2='%s-routing' % s_new, 
                params2={
                    'ip': '%d.%d.%d.1/24' % s_oldbytes
                }
                )

            # Push route of previous hop
            routes.append('add %s.0/24' % ('%d.%d.%d' % s_oldbytes))

            # For each previous host, we create a route through the routing intf
            routes_intf = [route + (' via %s.100 dev ' %  ('%d.%d.%d' % s_oldbytes) )
            + ('%s-routing' % s_new) for route in routes]

            # Get another IP
            s_newbytes = self.getAnotherIP()
            
            # Add default route
            routes_intf.append(('add 0.0.0.0/0 via %d.%d.%d.1 dev '  % s_newbytes)  + ('%s-main' % s_new))
            self.nodeSetRoutes(s_new, routes_intf)

            s_lastold = s_old
            s_lastoldbytes = s_oldbytes
            s_old = s_new
            s_oldbytes = s_newbytes

        s_new = s_old
        s_newbytes = s_oldbytes
        s_old = s_lastold
        s_oldbytes = s_lastoldbytes
       


        if lastNode is not None:
            hN = self.addHost('hN', cls=lastNode,
                              ip='%d.%d.%d.1/24' % s_newbytes, routes=routes_intf)
        else:
            hN = self.addHost('hN', ip='%d.%d.%d.1/24' % s_newbytes, routes=routes_intf, 
                cls=Node)
        self.addLink(s_new, hN, delay='%dms' % (delays[-1]),
                intfName1='%s-main' % s_new, 
                params1={
                    'ip': '%d.%d.%d.100/24' % s_newbytes
                },
                intfName2='%s-routing' % hN, 
                params2={
                    'ip': '%d.%d.%d.1/24' % s_newbytes
                }
                )

        # Push route of previous hop
        routes.append('add %s.0/24' % ('%d.%d.%d' % s_newbytes))

        # For each previous host, we create a route through the routing intf
        routes_intf = [route + (' via %s.100 dev ' %  ('%d.%d.%d' % s_newbytes) )
        + ('%s-routing' % hN) for route in routes]
        self.nodeSetRoutes(hN, routes_intf)


        

    def nodeSetRoutes(self, name, val):
        self.modifyProperty(name, 'routes', val)

    def nodeSetIP(self, name, val):
        self.modifyProperty(name, 'ip', val)

    def modifyProperty(self, name, prop, val):
        dic = {prop: val}
        info = self.nodeInfo(name)
        info.update(dic)
        self.setNodeInfo(name, info)
        
    def getAnotherIP(self):
        self.ip_counter1 += 1
        if self.ip_counter1 == 256:
            self.ip_counter1 = 0
            self.ip_counter2 += 1
            if self.ip_counter2 == 256:
                self.ip_counter2 = 0
                self.ip_counter3 += 1
                if self.ip_counter3 == 256:
                    raise ValueError('Too many IPs')
        return (self.ip_counter3, self.ip_counter2, self.ip_counter1)
