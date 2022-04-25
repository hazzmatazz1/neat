from .NodeGene import NodeGene
from .ConnectionGene import ConnectionGene

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

    def createConnection(self, in_node, out_node, weight):
        """Creates a new connection between two specified nodes
        
        Parameters:
            in_node (NodeGene): The node which this connection originates from
            out_node (NodeGene): The node which this connection connects to
        
        Returns:
            connection (ConnectionGene): The connection created between the in and out nodes
        """
        connection = self.neat.createConnection(in_node, out_node, weight)
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
        return connection

    def getConnection(self, innovation):
        """Finds a connection within this genome based on the innovation number and returns it
        
        Parameters:
            innovation (int): The innovation number of the ConnectionGene to get
        
        Returns:
            connection (ConnectionGene): The connection found
        """
        if innovation in self.connections:
            return self.connections.get(str(innovation))
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
        return node

    def getNode(self, innovation):
        """Finds a node within this genome based on the innovation number and returns it
        
        Parameters:
            innovation (int): The innovation number of the NodeGene to get
        
        Returns:
            node (NodeGene): The node found
        """
        if innovation in self.nodes:
            return self.nodes.get(str(innovation))
        raise ValueError(f"NodeGene innovation number {innovation} does not exist.")

    def mutate(self):
        """A method to perform mutations at random on this genome
        """
        # Mutate weights or structure
        for connection in self.connections:
            if self.neat.config.MUTATE_WEIGHTS > random.random():
                # Mutate
                if self.neat.config.MUTATE_WEIGHTS_SHIFT > random.random():
                    self.mutate_weight_shift(connection)
                else:
                    self.mutate_weight_random(connection)

        if self.neat.config.MUTATE_ADD_CONNECTION > random.random():
            # Add a new connection
            self.mutate_connection()

        # Do mutate node after to create a very small chance for a connection to be created and split in a single mutation
        if self.neat.config.MUTATE_ADD_NODE > random.random():
            # Add a new node
            self.mutate_node()

    def mutate_connection(self):
        """A method to add a new random connection to this genome
        """
        for _ in range(100):
            node_a = random.choice(list(self.nodes.values()))
            node_b = random.choice(list(self.nodes.values()))

            #print(node_a, node_b)

            if node_a == node_b:
                continue

            if node_a.node_type == 'OUTPUT' or node_b.node_type == 'INPUT':
                # linking an output to anything or anything to an input is not allowed
                continue

            hashcode_a = node_a.innovation * self.neat.config.MAX_NODES + node_b.innovation
            hashcode_b = node_b.innovation * self.neat.config.MAX_NODES + node_a.innovation

            if self.neat.getConnection(hashcode_a) or self.neat.getConnection(hashcode_b):
                # a link already exists between these two nodes
                continue

            weight = random.uniform(-1, 1) * self.neat.config.MUTATE_WEIGHTS_RANDOM_STRENGTH
            
            return self.createConnection(node_a, node_b, weight)

    def mutate_node(self):
        """A method to split a random connection and add a node in the middle to this genome
        """
        if len(self.connections) == 0:
            # No connections to split so exit
            return
        connection = random.choice(list(self.connections.values()))
        if not connection or not connection.enabled:
            return

        in_node = connection.in_node
        out_node = connection.out_node

        middle_node = self.createNode('HIDDEN')

        connection_in_mid = self.createConnection(in_node, middle_node, 1)
        connection_mid_out = self.createConnection(middle_node, out_node, connection.weight)

        connection.enabled = False

    def mutate_weight_shift(self, connection):
        """A method to randomly shift a weight of a connection

        Parameters:
            connection (ConnectionGene): The connection to be weight shifted
        """
        if isinstance(connection, ConnectionGene):
            connection.weight += random.uniform(-1, 1) * self.neat.config.MUTATE_WEIGHTS_SHIFT_STRENGTH

    def mutate_weight_random(self, connection):
        """A method to randomly set a weight of a connection

        Parameters:
            connection (ConnectionGene): The connection to randomise the weight
        """
        if isinstance(connection, ConnectionGene):
            connection.weight = random.uniform(-1, 1) * self.neat.config.MUTATE_WEIGHTS_RANDOM_STRENGTH

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
        highest_innovation_a = list(genome_a.connections.keys())[-1]
        highest_innovation_b = list(genome_b.connections.keys())[-1]

        if not crossover and highest_innovation_a < highest_innovation_b:
            # Swap genomes over so genome_a has a higher maximum innovation number
            genome_a, genome_b = genome_b, genome_a

        # Need a list of the keys sorted by ascending order so that both genomes can be checked against each other
        genome_a_keys = list(genome_a.connections.keys())
        genome_b_keys = list(genome_b.connections.keys())

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
                    enabled = True
                    if (not gene_a.enabled or not gene_b.enabled) and self.neat.config.INHERIT_DISABLED > random.random():
                        # If either parent has this gene disabled, have a set chance for it to be disabled
                        enabled = False
                    if random.random() < 0.5:
                        connection = child.addConnection(copy.deepcopy(gene_a))
                        connection.enabled = enabled
                    else:
                        connection = child.addConnection(copy.deepcopy(gene_b))
                        connection.enabled = enabled
                    index_a += 1
                    index_b += 1
                elif innovation_a > innovation_b:
                    # Disjoint of b (ignored in crossover)
                    #child.addConnection(copy.deepcopy(gene_b))
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
                innovation_a = genome_a_keys[index_a]
                gene_a = genome_a.getConnection(innovation_a)
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
        return self._compatibilityCrossoverUtil(self, genome, False)

    def crossover(self, genome_a, genome_b):
        """
        """
        return self._compatibilityCrossoverUtil(genome_a, genome_b, True)

    def evaluate(self):
        """A function to evaluate the outputs of this genome
        """
        # Initialise previous outputs to be different from new_outputs so that the while loop runs once
        previous_outputs = ['xyz']
        new_outputs = []
        
        for node in self.nodes.values():
            # Initialise all nodes output to 0
            if node.node_type == 'INPUT':
                continue
            node.output = 0

        # As there can be loops in the genome, we evaluate all connections multiple times
        # We do this until the outputs stabilise or we reach a maximum number of iterations
        iterations = 0
        while previous_outputs != new_outputs and iterations < self.neat.config.MAX_EVALUATIONS:
            iterations += 1

            previous_outputs = new_outputs
            new_outputs = []

            for connection in self.connections.values():
                if not connection.enabled:
                    # Don't evaluate deactivated connections
                    continue
                output = connection.in_node.output * connection.weight
                connection.out_node.inputs.update({str(connection.innovation): output})
                evaluated = connection.out_node.evaluate()
                if connection.out_node.node_type == 'OUTPUT':
                    new_outputs.append(evaluated)

            print(new_outputs)

        return new_outputs