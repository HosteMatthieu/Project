
# Defines the base for a gateway to a peer-to-peer network.
# Any gateway design can use this exact layout for easy communication between peers.

class NodeBase:
    
    """
    Gateway object for easy communication between peers in a network. It can send and receive Python objects over the network.
    """
    
    # Constructor
    
    def __init__(self, nodeIdentifier):
        """
        Initializes the gateway object with an identity (peerIdentifier) that differentiates it from other peers on the network.
        """
        pass
        
    # Sending
    
    def send_object_to_node(self, obj, nodeIdentifier):
        """
        Sends a Python object to the node with identifier "nodeIdentifier".
        """
        raise NotImplementedError
        
    def broadcast_object(self, obj):
        """
        Sends a Python object to all nodes on the network.
        """
        raise NotImplementedError
        
    # Receiving
    
    def receive_object_from_node(self, obj, nodeIdentifier):
        """
        Receives an object that has been sent by a node.
        """
        raise NotImplementedError