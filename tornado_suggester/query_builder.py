from pyelasticsearch.client import ElasticSearch
import pyelasticsearch
import sys
import os

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(SCRIPT_DIR + '/..'))

from config import settings

connection = ElasticSearch(settings.ES_HOST)

class QueryBuilder:

    def __init__(self, query, size):
        
        self.size = size
        self.should_query = []
        self.searchQuery = query
        self.edgeword, self.keyword = self.processText()
    
    def processText(self):
        
        text_split = self.searchQuery.split(" ")
        if len(text_split) == 1:
            return self.searchQuery, None

        edgeword = text_split.pop()
        keyword = " ".join(text_split)
        return edgeword, keyword

    @staticmethod
    def get_match_query(field, query, operator='or'):
        
        query_field = field
        query = {'match': {
                    query_field: {
                        'query': query,
                        'operator': operator,
                        "zero_terms_query": "all"
                        }
                    }
                }
        return query

    def build_query(self):

        self.should_query.append(self.get_match_query('name.name', self.searchQuery))
        self.should_query.append(self.build_edgeword_keyword_bool())

        query = { 'query':{
                    'bool': {
                    'should': self.should_query
                }}}
        return query

    def build_edgeword_keyword_bool(self):

        if self.keyword is None:
            return self.get_match_query('name.whitespace_edgegram', self.edgeword)
        query = {'bool': {'must': []}}
        query['bool']['must'].append(self.get_match_query('name.whitespace_keyword', self.keyword))
        query['bool']['must'].append(self.get_match_query('name.whitespace_edgegram', self.edgeword))
        return query

    def fetch_result(self):
        query = self.build_query()
        result = connection.search(query, index=settings.INDEX_NAME, doc_type=settings.DOC_TYPE, size=self.size)
        return result
