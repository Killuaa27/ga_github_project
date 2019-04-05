############## CALCOLO degree, betweenness, and closeness centrality ###############
from operator import itemgetter
from IPython.display import HTML
from IPython.core.display import display
import networkx as nx


# The classic Krackhardt kite graph
kkg = nx.generators.small.krackhardt_kite_graph()

print("Degree Centrality")
print(sorted(nx.degree_centrality(kkg).items(), 
             key=itemgetter(1), reverse=True))
print()

print("Betweenness Centrality")
print(sorted(nx.betweenness_centrality(kkg).items(), 
             key=itemgetter(1), reverse=True))
print()

print("Closeness Centrality")
print(sorted(nx.closeness_centrality(kkg).items(), 
             key=itemgetter(1), reverse=True))



#### PAG 337