"""
"""

class NodeGene:
    """
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
        inputs:
            NodeGene object: NodeGene to compare with
        outputs:
            Boolean: If these two nodes have the same innovation number
        """
        if not isinstance(object, NodeGene):
            return False
        return self.innovation == object.innovation