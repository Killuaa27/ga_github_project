# Adding programming languages as nodes
# Iterate over all of the repos, and add edges for programming languages
# # for each person in the graph. We'll also add edges back to repos sothat
# we have a good point to "pivot" upon.
from operator import itemgetter
import networkx as nx
h = nx.read_gpickle("snapshots/github.gpickle.2")
g = h.copy()

repos = [n for n in g.nodes()
if g.node[n]['type'] == 'repo']
for repo in repos:
    lang = (g.node[repo]['lang'] or "") + "(lang)"
    stargazers = [u 
        for (u, r, d) in g.in_edges(repo, data=True)
            if d['type'] == 'gazes'
    ]
    for sg in stargazers:
        g.add_node(lang, type='lang')
        g.add_edge(sg, lang, type='programs')
        g.add_edge(lang, repo, type='implements')

# Some stats
print(nx.info(g))
print()

# What languages exist in the graph?
print("Programming languages in graph: ")
print([n
    for n in g.nodes()
        if g.node[n]['type'] == 'lang']
)
print()

# What is the most popular programming language?
print("Most popular languages")
print(sorted([(n, g.in_degree(n))
    for n in g.nodes()
        if g.node[n]['type'] == 'lang'], key=itemgetter(1), reverse=True)[:10]
)
print()


# How many users program in a particular language?
python_programmers = [u
    for (u, l) in g.in_edges('Python(lang)')
        if g.node[u]['type'] == 'user']
print("Number of Python programmers:", len(python_programmers))
print()


########## SALVO IL GRAFO ######
nx.write_gpickle(g, "snapshots/github.gpickle.3")
