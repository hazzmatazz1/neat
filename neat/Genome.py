from NodeGene import NodeGene
from ConnectionGene import ConnectionGene

import copy
import random

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

    def _compatibilityCrossoverUtil(self, genome_a, genome_b, crossover=False):
        """As both compatibility checks and crossover need to do similar functionality, it has been brought here to avoid duplications

        Parameters:
            genome_a (Genome): The first genome to check
            genome_b (Genome): The second genome to check
            crossover (bool): What function needs to be performed
        Returns:
            similarity (float): A float is returned when crossover = False
            child (Genome): A child Genome is returned when crossover = True
        """
        if not isinstance(genome_a, Genome):
            raise ValueError(f"genome_a: type must be Genome. Current type is {type(genome_a)}")
        if not isinstance(genome_b, Genome):
            raise ValueError(f"genome_b: type must be Genome. Current type is {type(genome_b)}")

        # When checking compatibility genome_a must have the higher innovation number
        highest_innovation_a = list(genome_a.connections.keys()).sort()[-1]
        highest_innovation_b = list(genome_b.connections.keys()).sort()[-1]

        if not crossover and highest_innovation_a < highest_innovation_b:
            # Swap genomes over so genome_a has a higher maximum innovation number
            genome_a, genome_b = genome_b, genome_a

        # Need a list of the keys sorted by ascending order so that both genomes can be checked against each other
        genome_a_keys = list(genome_a.connections.keys()).sort()
        genome_b_keys = list(genome_b.connections.keys()).sort()

        # Keep track of an index for each to loop through and match genes in the genomes
        index_a = 0
        index_b = 0

        if crossover:
            # Create an empty child genome
            child = self.neat.empty_genome()
        else: # compatibility
            # These are all of the variables needed for the compatibility function
            disjoint = 0
            excess = 0
            similar = 0
            weight_difference = 0
            N = max(len(genome_a.connections), len(genome_b.connections))
            if N < 20:
                N = 1

        while index_a < len(genome_a.connections) and index_b < len(genome_b.connections):
            # Get the current innovation number being checked for each genome
            innovation_a = genome_a_keys[index_a]
            innovation_b = genome_b_keys[index_b]

            if crossover:
                # Get a copy of the gene for the current innovation number so that they can be given to the child
                gene_a = genome_a.getConnection(innovation_a)
                gene_b = genome_b.getConnection(innovation_b)

                if innovation_a == innovation_b:
                    # Similar Gene - take at random from either parent
                    if random.random() < 0.5:
                        child.addConnection(copy.deepcopy(gene_a))
                    else:
                        child.addConnection(copy.deepcopy(gene_b))
                    index_a += 1
                    index_b += 1
                elif innovation_a > innovation_b:
                    # Disjoint of b (ignored in crossover)
                    index_b += 1
                else:
                    # Disjoint of a - make sure to include in child
                    child.addConnection(copy.deepcopy(gene_a))
                    index_a += 1

            else: # compatibility
                if innovation_a == innovation_b:
                    # Similar Gene
                    similar += 1
                    weight_difference += abs(gene_a.weight - gene_b.weight)
                    index_a += 1
                    index_b += 1
                elif innovation_a > innovation_b:
                    # Disjoint Gene of b
                    disjoint += 1
                    index_b += 1
                else:
                    # Disjoint Gene of a
                    disjoint += 1
                    index_a += 1
        
        if crossover:
            # Copy the excess genes from genome_a
            while index_a < len(genome_a.connections):
                child.addConnection(copy.deepcopy(gene_a))
                index_a += 1

            # Copy all of the nodes associated with the connections (otherwise the child will have no nodes)
            for connection in child.connections.values():
                child.addNode(connection.in_node)
                child.addNode(connection.out_node)
            
            return child

        else: # compatibility
            # Calculate the excess - as genome_a has the higher innovation number it will be the one with excess genes
            excess = len(genome_a.connections) - index_a
            weight_difference /= similar
            return (self.neat.config.C1 * excess)/N + (self.neat.config.C2 * disjoint)/N + (self.neat.config.C3 * weight_difference)
    
    def compatibility(self, genome):
        """The compatibility function checks two genomes to determine how similar they are for speciation.
        
        Parameters:
            genome (Genome): The genome to compare against
        
        Returns:
            similarity (float): A value to represent the genomes similarity for speciation
                OR
            species (bool): Representing if these genomes are part of the same species
        """
        self._compatibilityCrossoverUtil(self, genome, False)

    def crossover(self, genome_a, genome_b):
        """
        """
        self._compatibilityCrossoverUtil(genome_a, genome_b, True)

    