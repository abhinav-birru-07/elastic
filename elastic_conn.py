from flask import Flask
from elastic import ElasticSearch
from flask import request
from flask_cors import CORS
from flask import jsonify
import json
app = Flask(__name__)
CORS(app)

es_index = 'test_12'


@app.route('/')
def main():
    print("welcome")
    return "Hello bhaiya!!!"


@app.route('/create_doc', methods=['POST'])
def create_doc():
    print("printing req args")
    print(request.data)
    print(type(json.loads(request.data.decode('utf-8'))))
    es = ElasticSearch()
    res = es.create_doc(doc=json.loads(request.data.decode('utf-8')), es_index=es_index)
    print(res)
    print(type(res))
    return res
    return jsonify("response from api")


@app.route('/get_docs_search', methods=['GET', 'POST'])
def get_docs_search():
    body = json.loads(request.data.decode('utf-8'))
    search_name = body['searchName']
    size = body['size'] if 'size' in body else 100
    sort_field = body['sortField'] if 'sortField' in body else None
    sort_order = body['sortOrder'] if 'sortOrder' in body else None
    es = ElasticSearch()
    if sort_field and sort_order:
        resp = es.get_docs_search(size=size, es_index=es_index, search_name=search_name, sort_field=sort_field, sort_order=sort_order)
    else:
        resp = es.get_docs_search(size=size, es_index=es_index, search_name=search_name)
    return resp


@app.route('/get_docs_click', methods=['GET', 'POST'])
def get_docs_click():
    es = ElasticSearch()
    body = json.loads(request.data.decode('utf-8'))
    print("check req body here")
    print(body)
    if ('sortField' in body) and ('sortOrder' in body):
        resp = es.get_docs_click(es_index=es_index, category_selected=body['category'],
                                 sort_field=body['sortField'], sort_order=body['sortOrder'])
    else:
        resp = es.get_docs_click(es_index=es_index, category_selected=body['category'])
    return resp


@app.route('/fetch_doc_id', methods=['GET', 'POST'])
def fetch_doc_id():
    es = ElasticSearch()
    body = json.loads(request.data.decode('utf-8'))
    resp = es.get_doc_id(doc_id=body['doc_id'], es_index=es_index)
    return resp


@app.route('/get_my_prod', methods= ['GET', 'POST'])
def get_my_prod():
    es = ElasticSearch()
    body = json.loads(request.data.decode('utf-8'))
    resp = es.get_my_prod(useref=body['useRef'], es_index=es_index)
    return resp


@app.route('/del_my_prod', methods = ['POST'])
def del_my_prod():
    es = ElasticSearch()
    body = json.loads(request.data.decode('utf-8'))
    resp = es.del_my_prod(es_index=es_index, prod_id=body['prodId'])
    return resp


@app.route('/update_prod', methods=['POST'])
def update_prod():
    es = ElasticSearch()
    body = json.loads(request.data.decode('utf-8'))
    prod_id = body['prodId']
    del body['prodId']
    body = {
        "doc": body
    }
    resp = es.update_prod(es_index=es_index, prod_id=prod_id, updated_data=body)
    print(resp)
    print(type(resp))
    return resp


if __name__ == '__main__':
    app.run()
