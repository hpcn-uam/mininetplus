from mininet.node import Node

class HTTPServer(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(HTTPServer, self).config(**params)
        # Enable forwarding on the router
        self.cmd('python -m SimpleHTTPServer 8000 &')