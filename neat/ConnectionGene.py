"""
"""

class ConnectionGene:
    """
    """

    def __init__(self, in_node, out_node, weight, enabled, config):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = enabled
        self.innovation = None
        self.config = config

    def equals(self, object):
        """A method to determine if two ConnectionGenes are equal
        inputs:
            ConnectionGene object: ConnectionGene to compare with
        outputs:
            Boolean: If these two connections are the same
        """
        if not isinstance(object, ConnectionGene):
            return False
        return self.in_node.equals(object.in_node) and self.out_node.equals(object.out_node)

    # HashCode idea from Finn Eggers https://www.youtube.com/channel/UCaKAU8vQzS-_e5xt7NSK3Xw
    def hash(self):
        """A method to generate a hash to tell if two ConnectionGenes have the same in and out nodes
        This could function as the innovation number however will not be able to give historical information (such as when an innovation was created)
        inputs:
            None
        outputs:
            string: A hashcode to represent this ConnectionGene
        """
        return str(self.in_node.innovation * self.config.MAX_NODES + self.out_node.innovation)