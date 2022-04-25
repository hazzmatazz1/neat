import neat
    
network = neat.NEAT(3, 1, neat.Config())
genome_a = network.empty_genome()

neat.drawGenome(genome_a)
