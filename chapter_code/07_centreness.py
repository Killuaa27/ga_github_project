from operator import itemgetter
import networkx as nx


# Create a copy of the graph so that we can iteratively mutate the copy
# as needed for experimentation
g = nx.read_gpickle("snapshots/github.gpickle.1")
h = g.copy()

# Remove the seed of the interest graph, which is a supernode, in order
# to get a better idea of the network dynamics
h.remove_node('Mining-the-Social-Web(repo)')

# Remove any other nodes that appear to be supernodes.
# Filter any other nodes that you can by threshold
# criteria or heuristics from inspection.
# Display the centrality measures for the top 10 nodes
dc = sorted(nx.degree_centrality(h).items(),
key=itemgetter(1), reverse=True)
print("Degree Centrality")
print(dc[:10])
print()
bc = sorted(nx.betweenness_centrality(h).items(),key=itemgetter(1), reverse=True)
print("Betweenness Centrality")
print(bc[:10])
print()
print("Closeness Centrality")
cc = sorted(nx.closeness_centrality(h).items(),
key=itemgetter(1), reverse=True)
print(cc[:10])