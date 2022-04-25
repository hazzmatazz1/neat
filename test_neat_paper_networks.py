import neat
    
network = neat.NEAT(3, 1, neat.Config())
genome_a = network.empty_genome()
genome_b = network.empty_genome()
#genome.createConnection(genome.nodes['1'], genome.nodes['3'], 1)

inno_5 = genome_a.createNode('HIDDEN')
print(inno_5.innovation)
genome_a.createConnection(genome_a.nodes['1'], genome_a.nodes['4'], 1)
genome_a.createConnection(genome_a.nodes['2'], genome_a.nodes['4'], 1).enabled = False
genome_a.createConnection(genome_a.nodes['3'], genome_a.nodes['4'], 1)
genome_a.createConnection(genome_a.nodes['2'], genome_a.nodes['5'], 1)
genome_a.createConnection(genome_a.nodes['5'], genome_a.nodes['4'], 1)
genome_a.createConnection(genome_a.nodes['1'], genome_a.nodes['5'], 1)

genome_b.addNode(inno_5)
genome_b.createNode('HIDDEN')
genome_b.createConnection(genome_b.nodes['1'], genome_b.nodes['4'], 1)
genome_b.createConnection(genome_b.nodes['2'], genome_b.nodes['4'], 1).enabled = False
genome_b.createConnection(genome_b.nodes['3'], genome_b.nodes['4'], 1)
genome_b.createConnection(genome_b.nodes['2'], genome_b.nodes['5'], 1)
genome_b.createConnection(genome_b.nodes['5'], genome_b.nodes['4'], 1).enabled = False
genome_b.createConnection(genome_b.nodes['5'], genome_b.nodes['6'], 1)
genome_b.createConnection(genome_b.nodes['6'], genome_b.nodes['4'], 1)
genome_b.createConnection(genome_b.nodes['3'], genome_b.nodes['5'], 1)
genome_b.createConnection(genome_b.nodes['1'], genome_b.nodes['6'], 1)

child = genome_a.crossover(genome_a, genome_b)

neat.drawGenome(genome_a)
neat.drawGenome(genome_b)
neat.drawGenome(child)