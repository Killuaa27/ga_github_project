'''
One user created one repo
Many user starred that repo
'''

# Github data 
import os
from github import Github
import os
ACCESS_TOKEN = os.getenv('GITHUBTOKEN')
USER = 'bobctr'
REPO = 'sec-crawl'

client = Github(ACCESS_TOKEN, per_page=100)
user = client.get_user(USER)
repo = user.get_repo(REPO)


# Creating graph 
import networkx as nx

g = nx.DiGraph()
g.add_node(repo.name + '(repo)', type='repo', lang=repo.language)
g.add_node(user.login + '(user)', type='user')
g.add_edge(user.login + '(user)', repo.name + '(repo)', type='creator')

# Getting the stargazers
stargazers = [ s for s in repo.get_stargazers() ]
for sg in stargazers:
	g.add_node(sg.login + '(user)', type='user')
	g.add_edge(sg.login + '(user)', repo.name + '(repo)', type='gazes')


# Showing the graph
import matplotlib.pyplot as plt
node_map = []
for node in g:
    if "repo" in node:
        node_map.append('#fcb383')
    elif "user" in node:
        node_map.append('#f44141')

edge_map = []
for edge in g.edges():
    if ("user" in edge[0]) and ("repo" in edge[1]):
        edge_map.append('grey')
    elif ("user" in edge[0]) and ("user" in edge[1]):
        edge_map.append('#f442b6')
nx.draw(g, node_color = node_map, edge_color = edge_map, with_labels = True)
plt.show()

# Saving graph
import json
from networkx.readwrite import json_graph
nx.write_gpickle(g, "graphs/users_repo.graph")
d = json_graph.node_link_data(g)
json.dump(d, open('graphs/users_repo.json', 'w'))



