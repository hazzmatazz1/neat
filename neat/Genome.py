from NodeGene import NodeGene
from ConnectionGene import ConnectionGene

class Genome:
    """A class to represent a single genome within a population

    Attributes:
        connections (dict): A dictionary mapping an innovation number to a connection
        nodes (dict): A dictionary mapping an innovation number to a node
        neat (NEAT): A reference to the NEAT manager class
    """
    def __init__(self, neat):
        self.connections = {}
        self.nodes = {}
        self.neat = neat

    def compatibility(self, genome):
        """The compatibility function checks two genomes to determine how similar they are for speciation.
        
        Parameters:
            genome (Genome): The genome to compare against
        
        Returns:
            similarity (float): A value to represent the genomes similarity for speciation
                OR
            species (bool): Representing if these genomes are part of the same species
        """
        if not isinstance(genome, Genome):
            raise ValueError(f"genome_2: type must be Genome. Current type is {type(genome)}")
        
        genome_1 = self
        genome_2 = genome

    def createConnection(self, in_node, out_node):
        """Creates a new connection between two specified nodes
        
        Parameters:
            in_node (NodeGene): The node which this connection originates from
            out_node (NodeGene): The node which this connection connects to
        
        Returns:
            connection (ConnectionGene): The connection created between the in and out nodes
        """
        connection = self.neat.createConnection(in_node, out_node)
        self.connections.update({str(connection.innovation): connection})
        return connection

    def addConnection(self, connection):
        """Adds a connection to this Genome. Usually called from the NEAT class
        
        Parameters:
            connection (ConnectionGene): The connection to be added to this genome
        """
        if not isinstance(connection, ConnectionGene):
            raise ValueError(f"connection: type must be ConnectionGene. Current type is {type(connection)}")
        self.connections.update({str(connection.innovation): connection})

    def getConnection(self, innovation):
        """Finds a connection within this genome based on the innovation number and returns it
        
        Parameters:
            innovation (int): The innovation number of the ConnectionGene to get
        
        Returns:
            connection (ConnectionGene): The connection found
        """
        if innovation < len(self.connections):
            return self.connections[str(innovation)]
        raise ValueError(f"Connection innovation number {innovation} does not exist.")

    def createNode(self, node_type):
        """Creates a new node
        
        Parameters:
            node_type (str): The type that the created node should be
        
        Returns:
            node (NodeGene): The node created
        """
        node = self.neat.createNode(node_type)
        self.nodes.update({str(node.innovation): node})
        return node

    def addNode(self, node):
        """Adds a node to this Genome. Usually called from the NEAT class
        
        Parameters:
            node (NodeGene): The node to be added to this genome
        """
        if not isinstance(node, NodeGene):
            raise ValueError(f"node: type must be NodeGene. Current type is {type(node)}")
        self.nodes.update({str(node.innovation): node})

    def getNode(self, innovation):
        """Finds a node within this genome based on the innovation number and returns it
        
        Parameters:
            innovation (int): The innovation number of the NodeGene to get
        
        Returns:
            node (NodeGene): The node found
        """
        if innovation < len(self.nodes):
            return self.nodes[str(innovation)]
        raise ValueError(f"NodeGene innovation number {innovation} does not exist.")

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