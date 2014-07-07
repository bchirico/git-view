import tornado.ioloop
import tornado.web
import asyncmongo
import logging
import os
import json
import pprint
import data_DAO

class MainHandler(tornado.web.RequestHandler):
    DAO = data_DAO()
    result = DAO.getAll()
    
#     def _on_response(self, response, error):
#         if error:
#             raise tornado.web.HTTPError(500)
#         for re in response:
#             print re
#         self.render('template', endpoints=response)
# 
# class GraphHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.render('force-collapsible.html')
#         
# class DataHandler(tornado.web.RequestHandler):
#     @property
#     def db(self):
#         if not hasattr(self, '_db'):
#             self._db = asyncmongo.Client(pool_id='mydb', host='127.0.0.1', port=27017, maxcached=10, maxconnections=50, dbname='RDFstruct')
#         return self._db
#      
#     @tornado.web.asynchronous
#     def get(self):
# #         self.db.EndPointSparql.find_one({'classNumber':{'$ne':None}, 'errors':{'$exists':False},'properties':{'$exists':True}},callback=self._on_response)
#         self.db.Test.find_one({'_id':104},callback=self._on_response)
#          
#          
#     def _on_response(self, response, error):
#          
# #         json_data=open('static/flare.json')
# #         data = json.load(json_data)
# #         nodes = []
# #         for 
#         node = []
#         invNode={}
#         index = 0
#         for clas in response['classes']:
#             node.append({'name':clas['class'].rsplit('/')[len(clas['class'].rsplit('/'))-1],'ni':int(clas['nInstance'])})
#             invNode[clas['class'].rsplit('/')[len(clas['class'].rsplit('/'))-1]]=index
#             index+=1
#         edges = []
# #         pprint.pprint(response["properties"])
#         for prop in response['properties']:
#             if prop['subject'].rsplit('/')[len(prop['subject'].rsplit('/'))-1] in invNode and prop['object'].rsplit('/')[len(prop['object'].rsplit('/'))-1] in invNode:
#                 edges.append({'source':invNode[prop['subject'].rsplit('/')[len(prop['subject'].rsplit('/'))-1]],
#                           'target':invNode[prop['object'].rsplit('/')[len(prop['object'].rsplit('/'))-1]],
#                           'np':int(prop['count'])})
#                 
#                 
#         pprint.pprint({'nodes':node,'links':edges})
# 
# 
#         self.write({'nodes':node,'links':edges})
#         self.finish()

application = tornado.web.Application(handlers=[
    (r"/", MainHandler),
#     (r"/index", GraphHandler),
#     (r"/getData", DataHandler),
 ],
static_path=os.path.join(os.path.dirname(__file__), "static")                                      )

if __name__ == "__main__":
    port = 8889
    print 'Listening on http://localhost:', port
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()