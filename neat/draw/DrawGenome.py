import networkx as nx
import matplotlib.pyplot as plt

def drawGenome(genome):
    nodes = []
    connections = []
    color_map = []
    weights = []

    for node in genome.nodes.values():
        if node.node_type == 'INPUT':
            color_map.append('red')
        elif node.node_type == 'OUTPUT':
            color_map.append('green')
        else:
            color_map.append('blue')

        nodes.append(
            node.innovation
        )

    for connection in genome.connections.values():
        if not connection.enabled:
            continue
        in_node = connection.in_node.innovation
        out_node = connection.out_node.innovation
        weight = connection.weight
        weights.append(weight)
        connections.append(
            (in_node, out_node, {'weight': weight})
        )

    graph = nx.DiGraph()

    graph.add_nodes_from(nodes)
    graph.add_edges_from(connections)

    pos = nx.spring_layout(graph, seed=1)

    nx.draw_networkx_nodes(graph, pos, node_size=300, node_color=color_map)
    nx.draw_networkx_edges(graph, pos)

    nx.draw_networkx_labels(graph, pos)
    #nx.draw_networkx_edge_labels(graph, pos, font_size=5)

    plt.show()