import networkx as nx
g = nx.read_gpickle("snapshots/github.gpickle.1")

####### PRINT DELLA RICERCA #######
from operator import itemgetter
from collections import Counter

print("Graph info: ")
print(nx.info(g))


### Print degli utennti con più di 2 archi entranti
c = Counter([e[1] for e in g.edges(data=True) if e[2]['type'] ==
'follows'])
popular_users = [ (u, f) for (u, f) in c.most_common() if f > 1 ]
print("Number of popular users", len(popular_users))
print("Top 10 popular users:", popular_users[:10])
