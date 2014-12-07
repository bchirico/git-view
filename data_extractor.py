import pygithub3 as git
import sys
import pprint as pp
import data_DAO as DAO

user_dao = DAO.generic_DAO('github', 'users')
repo_dao = DAO.generic_DAO('github', 'repos')

def authentication(user = 'Neuro17', password = ""):
    """ return pygithub3 authentication
    
    user: string representing the username
    """
    auth = dict(login=user, password = password)
    return git.Github(**auth)

def init_database(username):
    """ retrieve followers and repos for a specific user and store in database
        called only for database initialization
    
    username: string representing the username
    """
    user = get_followers(username)
    user['repos'] = get_repos(user['username'])
    user['followers_count'] = len(user['followers'])
    save_user(user)

def get_followers(user):
    """returns user's followers list retrieved via API
    
    user: string representing the username   
    """
    print "connecting to Github via API for followers"
    result = github.users.followers.list(user = user)
    list_followers = {'username': user,
                      'followers': [],
                      'repos': [],
                      }
    for followers in result:
        for follower in followers:
            name = follower.login
            url = follower.url
            list_followers['followers'].append({'name': name, 'url': url})
            
    #list_followers = [{'name': follower.login, 'url': follower.url} for followers in result for follower in followers]
    return list_followers

def get_repos(user):
    """returns user's repos list retrieved via API
    
    user: string representing the username
    """
    print "connecting to Github via API for repos"
    result = github.repos.list(user = user)
    repo_list = []
    for repos in result:
        for repo in repos:
            repo_list.append({'name': repo.name, 
                              'description': repo.description, 
                              'owner': repo.owner.login, 
                              'language': repo.language,
                              'star_count': repo.stargazers_count,
                              'watchers_count': repo.watchers_count,
                              'open_issue_count': repo.open_issues_count,
                              'pushed_at': repo.pushed_at,
                              'created_at': repo.created_at,
                              'updated_at': repo.updated_at,
                              'forks_count': repo.forks_count,
                              'collaborators': []
                             })
    return repo_list

def get_collaborators(username,repo):
    """returns repo's collaborators list retrieved via API
    
    username: string represented username
    repo: string represented repo's name
    """
    print "connecting to Github via API for collaborators"
    try:
        result = github.repos.collaborators.list(user = username, repo = repo)
        collaborators_list = [collaborator.login for collaborators in result for collaborator in collaborators if collaborator.login != username]
        return collaborators_list
    except:
        print "Unexpected error", sys.exc_info()[0] 

def create_user_profile(username):
    """returns a dict rappresenting user's profile 
    
    username: string represented username
    """
    user = get_followers(username)
    user['repos'] = get_repos(username)
    user['followers_count'] = len(user['followers'])
    return user

def save_user(user):
    """Saves user's profile
    
    user: dict representing user's profile
    """
    print "trying to save user: ", user['username']
    user_dao.insert_with_check(user, 'username', user['username'])
            
def get_all_users():
    """Returns pymongo cursor"""
    print "find all user in database"
    return user_dao.find_all()

def already_saved(query):
    """Returns True if a specific user is already saved in database.
    
    query: dict representing the database's query.
    """
    print "Verifing if it is already in database"
    return user_dao.find_one(query) != None

def get_new_user(cycle = 1):
    """iterates on users stored in database to looking for new users.
    
    cycle: number of times, the function iterates to find new users. 
    """
    for i in range(cycle):
        cursor = get_all_users()
        for user in cursor:
            for follower in user['followers']:
                username = follower['name']
                if not already_saved({'username': username}):
                    user = create_user_profile(follower['name'])
                    save_user(user)
                else: print "user {} already in databases".format(username)
                
def create_repos_collection():
    """Given users stored in database it creates a new collection with one document for each repo."""
    cursor = user_dao.find_all()
    for doc in cursor:
        for repo in doc['repos']:
            if doc['username'] == repo['owner'] and repo_dao.find_one(repo) == None:
                repo['collaborators'] = get_collaborators(doc['username'], repo['name'])
                repo_dao.insert(repo)
#             if doc2 is None:
#                 if doc['username'] == repo['owner']:
#                     repo_dao.insert(repo)
#                 else:
#                     repo['collaborators'].append(doc['username'])
#                     repo_dao.insert(repo)
#             elif doc['username'] != repo['owner']:
#                 repo_dao.insert_collaborator(repo, doc['username'])

def find_new_colls_as_users():
    """Returns users that are not in database (list), based on users found as a repo collaborator"""
    print "finding new collaborators as users"
    new_users = []
    cursor = repo_dao.find_all()
    for repo in cursor:
        for username in repo['collaborators']:
            if user_dao.find_one({'username': username}) == None and not username in new_users:
                new_users.append(username)
                new_users = [u for u in new_users if u != 'Try-Git']
    return new_users

def update_users_database():
    """Updates users database"""
    print "Updating users' database"
    for new_user in find_new_colls_as_users():
        print new_user
        user_dao.insert(create_user_profile(new_user))
    
def most_starred_repos():
    for repo in repo_dao.most_starred_repos(10):
        pp.pprint([repo['name'], repo['owner'], repo['star_count']])
                
if __name__ == '__main__':
    print 'running'
    user = 'your_username'
    password = 'your_password'
    github = authentication(user, password)

    init_database(user)    
    get_new_user(1)
    create_repos_collection()
    update_users_database()
    most_starred_repos()
    #print get_collaborators('Neuro17', 'geoQuery')
        
        

