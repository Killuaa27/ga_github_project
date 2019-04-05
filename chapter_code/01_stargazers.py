from github import Github # pip install pygithub
# Specify your own access token here
import os
ACCESS_TOKEN = os.getenv('GITHUBTOKEN')
# Specify a username and a repository of interest for that user
USER = 'ptwobrussell'
REPO = 'Mining-the-Social-Web'


client = Github(ACCESS_TOKEN, per_page=100)
user = client.get_user(USER)
repo = user.get_repo(REPO)
# Get a list of people who have bookmarked the repo.
# Since you'll get a lazy iterator back, you have to traverse
# it if you want to get the total number of stargazers.
stargazers = [ s for s in repo.get_stargazers() ]
print("Number of stargazers", len(stargazers))
