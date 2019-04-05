'''
One user created one repo
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

# Showing the graph
import matplotlib.pyplot as plt
nx.draw(g)
plt.show()

# Saving graph
import json
from networkx.readwrite import json_graph
nx.write_gpickle(g, "graphs/user_repo.graph")
d = json_graph.node_link_data(g)
json.dump(d, open('graphs/user_repo.json', 'w'))



