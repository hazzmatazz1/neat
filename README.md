# NeuroEvolution of Augmenting Topologies in Python
I have been very interested in artificial intelligence and understanding the algorithms used in training neural networks. This repository is an exploration into the NEAT algorithm while trying to implement this in Python.

This project will be built using the _**Evolving Neural Networks through
Augmenting Topologies**_ paper, which can be found in the _docs_ folder.

# Paper Summary
## 3.1 Genetic Encoding
### Classes
#### Genome
* list of connection genes

#### ConnectionGene
* In NodeGene
* Out NodeGene
* Enabled
* Innovation number

#### NodeGene
* inputs, hidden nodes & outputs


### Mutations
#### Weights
* Scale weights
* Offset weights

#### Structure
* add connection
    * Add a new connection between two previously unconnected nodes
* add node
    * Split an existing connection gene and add a new node. Disable the old connection and add two new connections. the new connection into the new node gets a weight of 1. The new connection leading out of the new node gets the same weight as the old connection.

## 3.2 Tracking Genes through Historical Markings
### Global Innovation Number
* Keep globally, likely will need a list to make sure that two genomes don't accidentally do the same mutation twice with different innovation numbers.

### Crossover
* Genes with the same innovation number are _matching genes_
* Genes that do not match are either disjoint or excess
* All disjoint or excess genes are included from the more fit parent
* Matching genes are chosen at random from either parent

## 3.3 Protection Innovation through Speciation
### Speciation
* Protects organisms to allow them to evolve and optimise before being discarded from reproducing#
* A _compatibility distance_ (CD) function is defined as: 

    CD = ((c1\*E)/N) + ((c2\*D)/N) + c3 \* W 

    where E = # of excess genes, D = # of disjoint genes, W = average weight difference of matching genes, N is the number of genes in the largest genome & c1, c2 & c3, are constants to weight the importance of each expression.
* A compatibility threshold should also be defined to determine if genomes are part of the same species.
* Each existing species is represented by a random genome from the previous generation.
* A genome is places in the first species in which it is compatible to prevent species overlap.
* If a genome is not compatible with any existing species a new one is created with the genome as its representative.

### Fitness Sharing
* Explicit fitness sharing so that fitness alues are normalised by species such that it is unlikely any one species will overtake the whole population.
* Adjusted fitness  is defined as fitness/count(genomes in the same species).
* Species are assigned a potentially different number of children based on the sum of the adjusted fitness.
* Species reproduce by eliminating the lowest performing members. The entire population is then replaced by the offspring.

## 3.4 Minimizing Dimensionality through Incremental Growth from Minimal Structure
* Networks star with 0 hidden nodes- as minimal as possible
* Structure is introduced through mutations and only survive is the provide value

## 4.1 Parameter Settings
* Initial settings were as follows:
    * c1 = 1.0
    * c2 = 1.0
    * c3 = 0.4
    * CD Threshold = 3.0
    * 80% chance of connection weights mutated
        * 90% chance to uniformly change
        * 10% chance to assign random
    * 75% chance of an inherited gene to be disabled if it was disabled in either parent
    * 25% of each generation resulted from mutation without crossover.
    * Interspecies mating rate was 0.001
    * In small populations probability to add a new node was 0.03 and new connection was 0.05
    * In large populations a new link probability was 0.3
    * Sigmoidal transfer activation function for all nodes
* If there was no improvement in 15 generations the stagnant species were not allowed to reproduce
* The champion of each species with more than 5 networks was automatically copied to the next generation.
