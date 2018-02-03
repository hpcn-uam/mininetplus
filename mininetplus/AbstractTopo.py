from mininet.topo import Topo
from mininetplus.node import Router

class AbstractTopo(Topo):

    def __init__(self):
        self.routers = []
        super(AbstractTopo, self).__init__()

    def addRouter(self, name, **params):
        self.routers.append(name)
        if 'cls' not in params:
            params['cls'] = Router
        return self.addHost(name, **params)

topos = { 'AbstractTopo': (lambda: AbstractTopo()) }
