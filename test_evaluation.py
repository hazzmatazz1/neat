import neat
    
network = neat.NEAT(2, 1)
genome_a = network.empty_genome()

genome_a.createNode('HIDDEN')
genome_a.createNode('HIDDEN')
genome_a.createNode('HIDDEN')

genome_a.createNode('OUTPUT')

genome_a.createConnection(genome_a.nodes['1'], genome_a.nodes['4'], 0.5)
genome_a.createConnection(genome_a.nodes['2'], genome_a.nodes['4'], 0.2)
genome_a.createConnection(genome_a.nodes['4'], genome_a.nodes['5'], 0.7)
genome_a.createConnection(genome_a.nodes['5'], genome_a.nodes['6'], 0.4)
genome_a.createConnection(genome_a.nodes['6'], genome_a.nodes['4'], 0.8)
genome_a.createConnection(genome_a.nodes['6'], genome_a.nodes['3'], 0.9)
genome_a.createConnection(genome_a.nodes['6'], genome_a.nodes['7'], 0.2)
genome_a.createConnection(genome_a.nodes['4'], genome_a.nodes['7'], 0.2)

print(genome_a.evaluate())


neat.drawGenome(genome_a)
