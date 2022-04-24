class NodeGene:
    """A class to define a single node within a NEAT neural network

    Attributes:
        node_type (string): The type of node that this is (INPUT/HIDDEN/OUTPUT)
        innovation (int): The innovation number of this node
    """

    TYPES = {
        'INPUT': 0,
        'HIDDEN': 1,
        'OUTPUT': 2
    }

    def __init__(self, node_type, innovation):
        self.innovation = innovation

        if node_type not in self.TYPES:
            raise ValueError(f"node_type: type must be one of {self.TYPES}.")
        
        self.node_type = node_type

    def equals(self, object):
        """A method to determine if two NodeGenes have the same innovation number
        
        Parameters:
            object (NodeGene): NodeGene to compare with
        
        Returns:
            equals (bool): If these two nodes have the same innovation number
        """
        if not isinstance(object, NodeGene):
            return False
        return self.innovation == object.innovation