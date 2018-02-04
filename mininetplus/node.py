from mininet.node import Host as HostM
from mininet.node import Node as NodeM


class Host(HostM):

    def config(self, **params):
        super(Host, self).config(**params)
        
        if 'routes' in params:
            for route in params['routes']:
                self.cmd('ip route %s' % route)
                   

    def terminate(self):
        super(Host, self).terminate()

    def addRoute(self, route):
        self.cmd('ip route add %s' % route)

    def routes(self):
        res = []
        cmd = self.cmd('route -n | tail -n +3')
        lines = cmd.split('\n')
        for line in lines:
            res.append(line.split())

        return res


class Node(NodeM):

    def config(self, **params):
        super(Node, self).config(**params)
        
        if 'routes' in params:
            for route in params['routes']:
                self.cmd('ip route %s' % route)
                   

    def terminate(self):
        super(Node, self).terminate()

    def addRoute(self, route):
        self.cmd('ip route add %s' % route)

    def routes(self):
        res = []
        cmd = self.cmd('route -n | tail -n +3')
        lines = cmd.split('\n')
        for line in lines:
            res.append(line.split())

        return res
