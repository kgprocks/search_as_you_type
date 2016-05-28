import tornado.ioloop
import tornado.web
import json
from query_builder import QueryBuilder

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        query = self.get_argument('query')
        size = self.get_argument('size', 5)
        query_obj = QueryBuilder(query, size)
        results = query_obj.fetch_result()['hits']['hits']
        data = []
        for result in results:
            data.append({'cin': result['_id'], 'name': result['_source']['name']})
        self.write(json.dumps(data))

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()