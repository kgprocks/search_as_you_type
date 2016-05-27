from django.http import HttpResponse, HttpResponseBadRequest
from query_builder import QueryBuilder
import json

def suggest(request):
    query = request.GET.get('query')
    if (query is None) or (len(query.strip()) == 0):
        return HttpResponseBadRequest(json.dumps({'response': 'bad request'}))
    else:
        size = request.GET.get('size')
        query_obj = QueryBuilder(query, size)
        results = query_obj.fetch_result()['hits']['hits']
        data = []
        for result in results:
            data.append({'cin': result['_id'], 'name': result['_source']['name']})
    response = HttpResponse(json.dumps(data))
    response['Access-Control-Allow-Origin'] = '*'
    return response

