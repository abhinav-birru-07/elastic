from elasticsearch import Elasticsearch
import json
# url = "https://448c3faae8404b5aa6fe573b384b4673.us-central1.gcp.cloud.es.io:9243"
#
# username = "elastic"
# password = "WijL2wDEMsG0aj2DUdecwzJv"
# cloud_id = "b31fad04ba3a43c1ab3181b5bdbcadf4:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDliOWY5ZjhlM2I3MTQxN2E4MTEzMzAxYTY1Mjg4MzRjJDQ0OGMzZmFhZTg0MDRiNWFhNmZlNTczYjM4NGI0Njcz"
#
#
# client = Elasticsearch(
#     cloud_id=cloud_id,
#     http_auth=(username, password)
# )


class ElasticSearch:
    def __init__(self):
        username = "elastic"
        password = "D6CGGFRPUaP5p4etNf9lbbGV"
        cloud_id = "olxiitg:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRiZmE2NGEzOTk5NTU0MGE0YWRkNzMyNzNjZmRmZGVlZiQ2MmIzMDVkY2IxZDg0OTU4ODU3YTMyMjFhYTVhZDM2MQ=="

        client = Elasticsearch(
            cloud_id=cloud_id,
            http_auth=(username, password)
        )
        self.client = client

    def create_index(self, es_index=None):
        if not es_index:
            print("please provide an index name to be created")
            return
        try:
            self.client.indices.create(index=es_index)
        except Exception as e:
            print(e)

    def create_doc(self, doc, es_index):
        """

        :param doc:
        :param es_index:
        :return:
        """
        print("about to create a doc")
        print(doc)
        print(type(doc))
        res = self.client.index(index=es_index, body=doc)
        print("after created a doc in es")
        return json.dumps(res)
    
    def get_docs_search(self, es_index, search_name, size=1000, sort_field="timeAdded", sort_order="desc"):
        query = {
            "size": size,
            "query": {
                "match": {
                    "name": search_name
                }
            },
            "sort": [
                {
                    sort_field + '.keyword': {
                        "order": sort_order
                    }
                }
            ]
        }
        resp = self.client.search(index=es_index, body=query)
        return resp

    def get_docs_click(self, es_index, category_selected, size=1000, sort_field="timeAdded", sort_order="desc"):
        query = {
            "size": size,
            "query": {
                "match": {
                    "productdiv": category_selected
                }
            },
            "sort": [
                {
                    sort_field + '.keyword': {
                        "order": sort_order
                    }
                }
            ]
        }
        resp = self.client.search(index=es_index, body=query)
        return resp

    def get_doc_id(self, doc_id, es_index):
        resp = self.client.get(index=es_index, id=doc_id)
        return resp

    def get_my_prod(self, useref, es_index, size=1000):
        query = {
            "size": size,
            "query": {
                "match": {
                    "useRef": useref
                }
            }
        }
        resp = self.client.search(index=es_index, body=query)
        return resp

    def del_my_prod(self, es_index, prod_id):
        try:
            resp = self.client.delete(index=es_index, id=prod_id)
            if resp['result'] == "deleted":
                return "product deleted successfully"
            return "product not found"
        except Exception as e:
            return e

    def update_prod(self, es_index, prod_id, updated_data):
        try:
            print(updated_data)
            resp = self.client.update(index=es_index, id=prod_id, body=updated_data)
            if resp['result'] == "updated":
                return "product deleted successfully"
            return "product not found"
        except Exception as e:
            return e


es = ElasticSearch()
es.create_index("test_12")


'''
sort features:
1. date: time_added
2. name
3. price

'''