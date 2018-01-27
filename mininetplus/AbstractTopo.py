from mininet.topo import Topo
from mininetplus.Router import Router

class AbstractTopo(Topo):

    def __init__(self):
        super(AbstractTopo, self).__init__()

    def addRouter(self, name):
        self.addHost(name, cls=Router)


topos = { 'AbstractTopo': (lambda: AbstractTopo()) }
