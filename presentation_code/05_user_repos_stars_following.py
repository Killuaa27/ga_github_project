'''
One user created one repo
Many user starred that repo
Many users created many repos
Many users starred many repos
Many users has many following
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

# Getting created repos from stargazers
MAX_REPOS = 500
for i, sg in enumerate(stargazers):
    print(sg.login)
    try:
        for repo in sg.get_repos()[:MAX_REPOS]: # Slice to avoidsupernodes
            g.add_node(repo.name + '(repo)', type='repo', lang=repo.language,owner=repo.owner.login)
            g.add_edge(sg.login + '(user)', repo.name + '(repo)', type='crator')
    except Exception as e: #ssl.SSLError:
        print("Encountered an error fetching created repos for", sg.login,"Skipping.")
    print("Processed", i+1, "stargazers' created repos")
    print("Num nodes/edges in graph", g.number_of_nodes(), "/", g.number_of_edges())
    print("Rate limit", client.rate_limiting)


# Getting starred repos from stargazers
MAX_REPOS = 500
for i, sg in enumerate(stargazers):
    print(sg.login)
    try:
        for starred in sg.get_starred()[:MAX_REPOS]: # Slice to avoidsupernodes
            g.add_node(starred.name + '(repo)', type='repo', lang=starred.language,owner=starred.owner.login)
            g.add_edge(sg.login + '(user)', starred.name + '(repo)', type='gazes')
    except Exception as e: #ssl.SSLError:
        print("Encountered an error fetching starred repos for", sg.login,"Skipping.")
    print("Processed", i+1, "stargazers' starred repos")
    print("Num nodes/edges in graph", g.number_of_nodes(), "/", g.number_of_edges())
    print("Rate limit", client.rate_limiting)

# Getting following from stargazers
import sys
for i, sg in enumerate(stargazers):
    # Add "follows" edges between stargazers in the graph if any relationships exist
    try:
        for following in sg.get_following():
            if following.login + '(user)' not in g:
                g.add_node(following.login + '(user)', type="user")
            g.add_edge(following.login + '(user)', sg.login + '(user)', 
                           type='following')
    except Exception as e: #ssl.SSLError
        print("Encountered an error fetching following for", sg.login, \
              "Skipping.", file=sys.stderr)
        print(e, file=sys.stderr)

    print("Processed", i+1, " stargazers. Num nodes/edges in graph", \
          g.number_of_nodes(), "/", g.number_of_edges())
    print("Rate limit remaining", client.rate_limiting)


# Showing the graph
import matplotlib.pyplot as plt
nx.draw(g)
plt.show()

# Saving graph
import json
from networkx.readwrite import json_graph
nx.write_gpickle(g, "graphs/users_repos_stars_following.graph")
d = json_graph.node_link_data(g)
json.dump(d, open('graphs/users_repos_stars_following.json', 'w'))



