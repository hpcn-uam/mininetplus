from mininet.link import Link, TCIntf



class TCLink( Link ):
    "Link with symmetric TC interfaces configured via opts"
    def __init__( self, node1, node2, port1=None, port2=None,
                  intfName1=None, intfName2=None,
                  addr1=None, addr2=None, params1=None, params2=None,
                  **params ):

        params1 = params1 if params1 is not None else {}
        params2 = params2 if params2 is not None else {}
        params1.update(params)
        params2.update(params)
        Link.__init__( self, node1, node2, port1=port1, port2=port2,
                       intfName1=intfName1, intfName2=intfName2,
                       cls1=TCIntf,
                       cls2=TCIntf,
                       addr1=addr1, addr2=addr2,
                       params1=params1,
                       params2=params2 )