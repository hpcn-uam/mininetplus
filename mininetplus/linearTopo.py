from mininetplus.AbstractTopo import AbstractTopo

class LinearSwitchTopo(AbstractTopo):

    def __init__(self, n=3, delays=[5, 10, 15], firstNode=None, lastNode=None, action=None):
        super(LinearSwitchTopo, self).__init__()
        s_old = False
        for i in range(n-2):
            s_new = self.addSwitch('s%d' % (i))
            if s_old:
                self.addLink(s_old, s_new, delay='%dms' % (delays[i+1]))
            s_old = s_new
        if firstNode is not None:
            h0 = self.addHost('h0', cls=firstNode)
        else:
            h0 = self.addHost('h0')
        if lastNode is not None:    
            hN = self.addHost('hN', cls=lastNode)
        else:
            hN = self.addHost('hN')
        switches = self.switches()
        self.addLink(switches[0], h0, delay='%dms' % (delays[0]))
        self.addLink(switches[-1], hN, delay='%dms' % (delays[-1]))
        
        if action is not None:
            action(self)

            
