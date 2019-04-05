import networkx as nx
g = nx.read_gpickle("snapshots/github.gpickle.2")

####### PRINT DELLA RICERCA #######
from operator import itemgetter
from collections import Counter

# Poke around: how to get users/repos
from operator import itemgetter
print(nx.info(g))
print()

# Get a list of repositories from the graph
repos = [n for n in g.nodes() if g.node[n]['type'] == 'repo']

# Most popular repos
print("Popular repositories")
print(sorted([(n,d)
for (n,d) in g.in_degree()
if g.node[n]['type'] == 'repo'],
key=itemgetter(1), reverse=True)[:10])
print()

# Projects gazed at by a user
print("Respositories that ptwobrussell has bookmarked")
print([(n,g.node[n]['lang'])
for n in g['ptwobrussell(user)']
if g['ptwobrussell(user)'][n]['type'] == 'gazes'])
print()

# Programming languages for each user
print("Programming languages ptwobrussell is interested in")
print(list(set([g.node[n]['lang']
    for n in g['ptwobrussell(user)']
        if g['ptwobrussell(user)'][n]['type'] == 'gazes'])
))
print()

# Find supernodes in the graph by approximating with a high number of
# outgoing edges
print("Supernode candidates")
print(sorted([(n, len(g.out_edges(n)))
    for n in g.nodes()
        if g.node[n]['type'] == 'user' and len(g.out_edges(n
)) > 500],
key=itemgetter(1), reverse=True))