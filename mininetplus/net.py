from mininet.net import Mininet as MininetM
from mininet.net import *

class Mininet(MininetM):
    def routers(self):
        return self.get(*self.topo.routers)

