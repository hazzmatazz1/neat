"""
"""

from NodeGene import NodeGene
from ConnectionGene import ConnectionGene

class Genome:
    """
    """
    def __init__(self, neat):
        self.connections = {}
        self.nodes = {}
        self.neat = neat

    def compatibility(self, genome_2):
        """The compatibility function checks two genomes to determine how similar they are for speciation.
        inputs:
            Genome: genome_2 - The genome to compare against
        outputs:
            float: A value to represent the genomes similarity for speciation
                OR
            boolean: Representing if these genomes are part of the same species
        """
        if not isinstance(genome_2, Genome):
            raise ValueError(f"genome_2: type must be Genome. Current type is {type(genome_2)}")
        
        genome_1 = self

    def createConnection(self, in_node, out_node):
        """Creates a new connection between two specified nodes
        inputs:
            NodeGene: in_node - the node which this connection originates from
            NodeGene: out_node - the node which this connection connects to
        outputs:
            ConnectionGene: The connection created
        """
        connection = self.neat.createConnection(in_node, out_node)
        self.connections.update({str(connection.innovation): connection})
        return connection

    def addConnection(self, connection):
        """Adds a connection to this Genome. Usually called from the NEAT class
        inputs:
            ConnectionGene: connection - The connection to be added to this genome
        outputs:
            ConnectionGene: connection - return the same value
        """
        if not isinstance(connection, ConnectionGene):
            raise ValueError(f"connection: type must be ConnectionGene. Current type is {type(connection)}")
        self.connections.update({str(connection.innovation): connection})
        return connection

    def getConnection(self, innovation):
        """Finds a connection within this genome based on the innovation number and returns it
        inputs:
            int: innovation - The innovation number of the ConnectionGene to get
        outputs:
            ConnectionGene: The connection found
                OR
            None: No connection found
        """
        if innovation < len(self.connections):
            return self.connections[str(innovation)]
        return None

    def createNode(self, node_type):
        """Creates a new node
        inputs:
            string: node_type - The type that the created node should be
        outputs:
            NodeGene: The node created
        """
        node = self.neat.createNode(node_type)
        self.nodes.update({str(node.innovation): node})
        return node

    def addNode(self, node):
        """Adds a node to this Genome. Usually called from the NEAT class
        inputs:
            NodeGene: node - The node to be added to this genome
        outputs:
            NodeGene: node - return the same value
        """
        if not isinstance(node, NodeGene):
            raise ValueError(f"node: type must be NodeGene. Current type is {type(node)}")
        self.nodes.update({str(node.innovation): node})
        return node

    def getNode(self, innovation):
        """Finds a node within this genome based on the innovation number and returns it
        inputs:
            int: innovation - The innovation number of the NodeGene to get
        outputs:
            NodeGene: The node found
                OR
            None: No node found
        """
        if innovation < len(self.nodes):
            return self.nodes[str(innovation)]
        return None #self.createNode()

    def mutate(self):
        """
        """
        # Mutate weights or structure
        pass

    @classmethod
    def crossover(genome_1, genome_2):
        """
        """
        pass