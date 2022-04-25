import math

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

        # These variables are used for evaluation
        if self.node_type == 'INPUT':
            self.output = 1
        else:
            self.output = 0
        self.inputs = {}

    def sigmoidal_transfer(self, x):
        return 1 / (1 + pow(math.e, -4.9*x))

    def evaluate(self):
        self.output = 0
        for value in self.inputs.values():
            self.output += value
        self.output = self.sigmoidal_transfer(self.output)
        return self.output