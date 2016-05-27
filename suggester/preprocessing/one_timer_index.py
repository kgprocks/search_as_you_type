from pyelasticsearch.client import ElasticSearch
import json
import requests
import pyelasticsearch
import sys
import os
import django

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(SCRIPT_DIR + '/../..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.conf import settings


class IndexData:

    def __init__(self, index_name, settings_path, host="http://127.0.0.1:9200"):
        
        self.connection = ElasticSearch(host)
        self.index_name = index_name
        self.settings_path = settings_path

        self.create_index()

    def get_settings(self):

        config_file = file(self.settings_path)
        settings = json.load(config_file)
        return settings

    def create_index(self):

        settings = self.get_settings()
        try:
            self.connection.create_index(self.index_name, settings)
        except pyelasticsearch.exceptions.ElasticHttpError as e:
            self.connection.delete_index(self.index_name)
            self.connection.create_index(self.index_name, settings)

    def index_data(self, data_path, index_type):

        if index_type is None:
            raise "Please enter valid index type"
        objects = []
        count = 0
        with open(data_path) as f:
            for line in f:
                word_split = line.split("\t")
                cin = word_split[0]
                name = word_split[1].strip()
                doc = {'cin':cin, 'name':name}
                objects.append(doc)
                if len(objects) > 1000:
                    response = self.connection.bulk_index(self.index_name, index_type, objects, id_field='cin')
                    objects = []
            self.connection.bulk_index(self.index_name, index_type, objects, id_field='cin')


if __name__ == "__main__":
    object_data = IndexData(settings.INDEX_NAME, 'es_config.json', host=settings.ES_HOST)
    object_data.index_data('companynames.tsv', settings.DOC_TYPE)