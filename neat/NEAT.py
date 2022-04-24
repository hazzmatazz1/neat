from NodeGene import NodeGene
from ConnectionGene import ConnectionGene
from Genome import Genome
from Config import Config

class NEAT:
    """A class to manage many functions of NEAT algorithm such as the connections and nodes 

    Attributes:
        all_connections (dict): A dictionary which maps connections to a innovation number
        all_nodes (dict): A dictionary which maps all nodes to an innovation number
        config (Config): A class for defining many different configuration parameters
    """
    def __init__(self, input_size, output_size, config):
        self.all_connections = {}
        self.all_nodes = {}
        self.config = config
        self.reset(input_size, output_size)

    def reset(self, input_size, output_size):
        """A method to reset this class back to defaults
        
        Parameters:
            input_size (int): How many inputs this network should take
            output_size (int): How many outputs this network should have
        """
        self.input_size = input_size
        self.output_size = output_size

        self.all_connections.clear()
        self.all_nodes.clear()

        for _ in range(input_size):
            self.createNode('INPUT')

        for _ in range(output_size):
            self.createNode('OUTPUT')

    def empty_genome(self):
        """A method to create an empty genome with the correct number of inputs and outputs
        
        Returns:
            genome (Genome): An empty genome with the specified number of inputs and outputs
        """
        genome = Genome(self)
        for i in range(self.input_size + self.output_size):
            genome.addNode(self.getNode(i))
        return genome

    def createConnection(self, in_node, out_node):
        """A method to create a new ConnectionGene. This first checks if the ConnectionGene already exists
        
        Parameters:
            in_node (NodeGene): The node which this connection originates from
            out_node (NodeGene): The node which this connection connects to
        
        Returns:
            connection (ConnectionGene): The connection created between the in and out nodes
        """
        connection = ConnectionGene(in_node, out_node, 1, True, self.config)

        if connection.hash() in self.all_connections:
            connection.innovation = self.all_connections.get(connection.hash()).innovation
        else:
            connection.innovation = len(self.all_connections)
            self.all_connections.update({str(connection.hash()): connection})

        return connection

    def getConnection(self, innovation):
        """Finds a connection based on the innovation number and returns it
        
        Parameters:
            innovation (int): The innovation number of the ConnectionGene to get
        
        Returns:
            connection (ConnectionGene): The connection found
        """
        if innovation < len(self.all_connections):
            return self.all_connections[innovation]
        raise ValueError(f"Connection innovation number {innovation} does not exist.")

    def createNode(self, node_type):
        """Creates a new node
        
        Parameters:
            node_type (str): The type that the created node should be
        
        Returns:
            node (NodeGene): The node created
        """
        node = NodeGene(node_type, len(self.all_nodes))
        self.all_nodes.update({str(node.innovation): node})
        return node

    def getNode(self, innovation):
        """Finds a node within this genome based on the innovation number and returns it
        
        Parameters:
            innovation (int): The innovation number of the NodeGene to get
        
        Returns:
            node (NodeGene): The node found
        """
        if innovation < len(self.all_nodes):
            return self.all_nodes.get(str(innovation))
        raise ValueError(f"Node innovation number {innovation} does not exist.")
        
if __name__ == "__main__":
    neat = NEAT(3, 3, Config)

    genome_a = neat.empty_genome()
    genome_b = neat.empty_genome()
    
    genome_a.compatibility(genome_b)
    print('done')