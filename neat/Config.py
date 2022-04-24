"""
C1 = Weighting for Excess genes in compatibility function
C2 = Weighting for Disjoint genes in compatibility function
C3 = Weighting for Weight Difference in compatibility function
COMPATIBILITY_THRESHOLD = Compatibility Threshold

MUTATE_WEIGHTS = The chance for the weights of a genome to be mutated
MUTATE_WEIGHTS_UNIFORM = The chance for a weight to be mutated uniformly
MUTATE_WEIGHTS_RANDOM = The chance for a weight to be mutated randomly
MUTATE_ADD_NODE = The chance for a genome to add a new node
MUTATE_ADD_CONNECTION = The chance for a genome to add a new connection between two nodes

INHERIT_DISABLED = The chance for an inherited gene to be disabled the gene is disabled in either parent
MUTATE_NO_CROSSOVER = The percantage of the population that should reproduce by only mutation with no crossover
INTERSPECIES_CROSSOVER = The chance that crossover will happen between species

NO_IMPROVEMENT_THRESHOLD = How many generations pass before a specied is not allowed to reproduce
SPECIES_CHAMPION_SIZE = The champion of each species with more than this many networks is automatically copied to the next generation

MAX_NODES = The maximum number of nodes that can be in a network
"""

class Config:
    # Compatibility Function
    C1 = 1.0
    C2 = 1.0
    C3 = 0.4
    COMPATIBILITY_THRESHOLD: 3.0

    # Mutation
    MUTATE_WEIGHTS = 0.8
    MUTATE_WEIGHTS_UNIFORM = 0.9
    MUTATE_WEIGHTS_RANDOM = 0.1
    MUTATE_ADD_NODE = 0.03
    MUTATE_ADD_CONNECTION = 0.05

    # Crossover
    INHERIT_DISABLED = 0.75
    MUTATE_NO_CROSSOVER = 0.25
    INTERSPECIES_CROSSOVER = 0.001

    # Speciation
    NO_IMPROVEMENT_THRESHOLD = 15
    SPECIES_CHAMPION_SIZE = 5

    #
    MAX_NODES = pow(2, 20)