import neat
import networkx as nx
import matplotlib.pyplot as plt

    
network = neat.NEAT(2, 1, neat.Config())
genome = network.empty_genome()
#genome.createConnection(genome.nodes['1'], genome.nodes['3'], 1)
genome.mutate_connection()
genome.mutate_connection()

genome.mutate_node()
genome.mutate_node()
genome.mutate_node()

genome.mutate_connection()
genome.mutate_connection()
genome.mutate_connection()
genome.mutate_connection()

neat.drawGenome(genome)