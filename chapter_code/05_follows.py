########### GETTIN THE DATA FROM GITHUB #############

from github import Github # pip install pygithub
import os
ACCESS_TOKEN = os.getenv('GITHUBTOKEN')
USER = 'ptwobrussell'
REPO = 'Mining-the-Social-Web'


client = Github(ACCESS_TOKEN, per_page=100)
user = client.get_user(USER)
repo = user.get_repo(REPO)
# Persone che hanno starrato
stargazers = [ s for s in repo.get_stargazers() ]


########## CREANDO IL GRAPH #####################
import networkx as nx

g = nx.DiGraph()
g.add_node(repo.name + '(repo)', type='repo', lang=repo.language, owner=user.login)
for sg in stargazers:
	g.add_node(sg.login + '(user)', type='user')
	g.add_edge(sg.login + '(user)', repo.name + '(repo)', type='gazes')


###### AGGIUNGENDO I FOLLOWERS ######

import sys

for i, sg in enumerate(stargazers):
    # Add "follows" edges between stargazers in the graph if any relationships exist
    try:
        for follower in sg.get_followers():
            if follower.login + '(user)' in g:
                g.add_edge(follower.login + '(user)', sg.login + '(user)', 
                           type='follows')
    except Exception as e: #ssl.SSLError
        print("Encountered an error fetching followers for", sg.login, \
              "Skipping.", file=sys.stderr)
        print(e, file=sys.stderr)

    print("Processed", i+1, " stargazers. Num nodes/edges in graph", \
          g.number_of_nodes(), "/", g.number_of_edges())
    print("Rate limit remaining", client.rate_limiting)



####### PRINT DELLA RICERCA #######
from operator import itemgetter
from collections import Counter

print("Quanti nodi aggiunti: ")
print(nx.info(g))


########## SALVO IL GRAFO ######
nx.write_gpickle(g, "snapshots/github.gpickle.1")