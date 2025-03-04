
class DummyNode:
    
    __networkMesh = {}
    
    def __init__(self, nodeIdentifier):
        if nodeIdentifier in DummyNode.__networkMesh:
            raise ValueError(f'A node with identifier {nodeIdentifier} already exists in the network. Use the static method "reset_network()" to reset the network and be able to register this node again.')
        self.nodeIdentifier = nodeIdentifier
        DummyNode.__networkMesh[nodeIdentifier] = self
    
    def send_object_to_node(self, obj, nodeIdentifier):
        if nodeIdentifier not in DummyNode.__networkMesh:
            return
        node = DummyNode.__networkMesh[nodeIdentifier]
        node.receive_object_from_node (obj, self.nodeIdentifier)
        
    def broadcast_object(self, obj):
        for nodeIdentifier in DummyNode.__networkMesh:
            if self.nodeIdentifier == nodeIdentifier:
                continue
            self.send_object_to_node(obj, nodeIdentifier)
            
    def receive_object_from_node(self, obj, nodeIdentifier):
        pass
            
    @staticmethod
    def reset_network():
        DummyNode.__networkMesh = {}