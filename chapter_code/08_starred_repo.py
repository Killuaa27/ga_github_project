from operator import itemgetter
import networkx as nx
from github import Github # pip install pygithub
import os
ACCESS_TOKEN = os.getenv('GITHUBTOKEN')
USER = 'ptwobrussell'
REPO = 'Mining-the-Social-Web'


client = Github(ACCESS_TOKEN, per_page=100)
client = Github(ACCESS_TOKEN, per_page=100)
user = client.get_user(USER)
repo = user.get_repo(REPO)
# Persone che hanno starrato
stargazers = [ s for s in repo.get_stargazers() ]


# Create a copy of the graph so that we can iteratively mutate the copy
# as needed for experimentation
h = nx.read_gpickle("snapshots/github.gpickle.1")
g = h.copy()


# Add each stargazer's additional starred repos and add edges
# to find additional interests
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


########## SALVO IL GRAFO ######
nx.write_gpickle(g, "snapshots/github.gpickle.2")
