import pymongo
import sys

class generic_DAO():
    def __init__(self, db, coll):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client[db]
        self.collection = self.db[coll]
        
    def find_one(self, query={}):
        try:
            return self.collection.find_one(query)
            
        except:
            print "Unexpected error", sys.exc_info()[0]
            
    def find_all(self, query={}):
        try:
            return self.collection.find(query)
        except:
            print "Unexpected error", sys.exc_info()[0]
            
    def insert_with_check(self, data, key, value):
        #name = data['username']
        try:
            doc = self.collection.find_one({key: value})
            if doc == None:
                self.collection.insert(data)
                print "finished without error"
            else:
                print "user {} already in database".format(value)
        except:
            print "Unexpected error", sys.exc_info()[0]
            
    def insert(self, data):
        try:
            self.collection.insert(data)
            print "finished without error"
        except:
            print "Unexpected error", sys.exc_info()[0]
            
    def update_repos(self, data, repos):
        try:
            self.collection.update({'username':data['username']},{'$set':{'repos':repos}})
            print "finished without error"
        except:
            print "Unexpected error", sys.exc_info()[0] 
            
    def insert_collaborator(self, repo, collaborator):
        try:
            doc = self.collection.update(repo,{'$addToSet':{'collaborators':collaborator}})
            print doc
            print "finished without error"
        except:
            print "Unexpected error", sys.exc_info()[0] 
            
    def most_starred_repos(self, limit):
        try:
            return self.collection.find().sort('star_count', pymongo.DESCENDING).limit(limit)
        except:
            print "Unexpected error", sys.exc_info()[0] 
                   