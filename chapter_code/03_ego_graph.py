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
g.add_no(user.log + ' (user)', type='user')
g.add_edge(user.login + '(user)', repo.name + '(repo)', type='created')
for sg in stargazers:
	g.add_node(sg.login + '(user)', type='user')
	g.add_edge(sg.login + '(user)', repo.name + '(repo)', type='gazes')

# Poke around in the current graph to get a better feel for how NetworkX works
print(nx.info(g))
print()
print("Repository: ")
print(g.node['Mining-the-Social-Web(repo)'])
print()
print("User:")
print(g.node['ptwobrussell(user)'])
print(g['ptwobrussell(user)']['Mining-the-Social-Web(repo)'])

print()
print(g['ptwobrussell(user)'])
print(g['Mining-the-Social-Web(repo)'])
print()
print(g.in_edges(['ptwobrussell(user)']))
print(g.out_edges(['ptwobrussell(user)']))
print()
print("Archi entranti: ")
print(g.in_edges(['Mining-the-Social-Web(repo)']))
print("\nArchi uscenti: ")
print(g.out_edges(['Mining-the-Social-Web(repo)']))

