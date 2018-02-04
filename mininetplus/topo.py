from mininet.topo import Topo as TopoM
from mininetplus.nodelib import Router

class Topo(TopoM):

    def __init__(self):
        self.routers = []
        super(Topo, self).__init__()

    def addRouter(self, name, **params):
        self.routers.append(name)
        if 'cls' not in params:
            params['cls'] = Router
        return self.addHost(name, **params)

topos = { 'Topo': (lambda: Topo()) }
