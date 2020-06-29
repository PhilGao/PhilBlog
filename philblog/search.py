from elasticsearch import Elasticsearch
from flask import current_app


def add_to_index(index, model):
    if not current_app.es:
        raise Exception('no es found!')
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.es.index(index=index, id=model.id, body=payload,request_timeout=30)


def remove_from_index(index, model):
    if not current_app.es:
        raise Exception('no es found!')
        return
    current_app.es.delete(index=index, id=model.id,request_timeout=30)
    return


def query_index(es, index, query, page, per_page):
    if not current_app.es:
        raise Exception('no es found!')
        return
    search = current_app.es.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},'from': (page - 1) * per_page,'size': per_page},
        request_timeout=30)
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']


if __name__ == "__main__":
    es = Elasticsearch('http://localhost:9200')


    # es.index(index='my_index', id=1, body={'text': 'this is a test'},request_timeout=30 )
    # es.index(index='my_index', id=2, body={'text': 'a second test'},request_timeout=30)
    # result = es.search(index='my_index', body={'query': {'match': {'text': 'this test'}}})

    # class Test():
    #     __searchable__ = ['content']
    #
    #     def __init__(self):
    #         self.id = 1
    #         self.content = 'this is an article'
    #
    #
    # add_to_index('my_index', Test())
    print(es.search(index='my_index',body='{"query":{"match_all":{}}}'))