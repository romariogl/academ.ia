from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

class ElasticsearchClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            load_dotenv()
            cls._instance = super(ElasticsearchClient, cls).__new__(cls)
            api_key = os.environ.get('ELASTICSEARCH_API_KEY', 'Empty')
            cls._instance.client = Elasticsearch("http://localhost:9200", api_key=api_key, verify_certs=False)
        return cls._instance

    def search(self, index_name, query):
            # Passo 1: Recuperação de documentos do Elasticsearch
        search_body = {
            "query": {
                "match": {
                    "text": query
                }
            },
            "size": 5  # Recupera os 5 documentos mais relevantes
        }

        response = self.client.search(index=index_name, body=search_body)
        retrieved_docs = [hit["_source"]["text"] for hit in response["hits"]["hits"]]
        return retrieved_docs
    
    def search_specific(self, index_name, query, filename):
            # Passo 1: Recuperação de documentos do Elasticsearch
        search_body = {
            "query": {
                "bool": {
                    "filter": {
                        "term": {
                            "file_name": filename  # Nome do arquivo fornecido
                        }
                    },
                    "must": {
                        "match": {
                            "text": query  # Conteúdo da consulta
                        }
                    }
                }
            },
            "size": 5  # Recupera os 5 documentos mais relevantes
        }


        response = self.client.search(index=index_name, body=search_body)
        retrieved_docs = [hit["_source"]["text"] for hit in response["hits"]["hits"]]
        return retrieved_docs