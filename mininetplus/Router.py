from mininet.node import Node

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