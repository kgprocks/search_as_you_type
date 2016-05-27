from pyelasticsearch.client import ElasticSearch
import json
import requests
import pyelasticsearch

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
        print type(settings)
        try:
            self.connection.create_index(self.index_name, settings)
        except pyelasticsearch.exceptions.ElasticHttpError as e:
        # except:
            print e
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
                # print cin, name
                doc = {'cin':cin, 'name':name}
                objects.append(doc)
                if len(objects) > 1000:
                    #check for errors
                    response = self.connection.bulk_index(self.index_name, index_type, objects, id_field='cin')
                    # print response
                    objects = []
            self.connection.bulk_index(self.index_name, index_type, objects, id_field='cin')



object_data = IndexData('your_company_name', 'es_config.json')
object_data.index_data('companynames.tsv', 'suggestions')