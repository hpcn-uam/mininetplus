from mininet.node import Node as NodeM

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
            
class Router(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(Router, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')
        

    def terminate(self):
        # Disable ip forwarding
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(Router, self).terminate()