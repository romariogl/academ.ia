from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
from collections import defaultdict

class ElasticsearchClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            load_dotenv()
            cls._instance = super(ElasticsearchClient, cls).__new__(cls)
            api_key = os.environ.get('ELASTICSEARCH_API_KEY', 'Empty')
            cls._instance.client = Elasticsearch("https://localhost:9200", api_key=api_key, verify_certs=False)
        return cls._instance

    def search(self, index_name, query):
            # Passo 1: Recuperação de documentos do Elasticsearch
        search_body = {
            "query": {
                "match": {
                    "content": query
                }
            },
            "size": 5
        }

        grouped_docs = defaultdict(str)

        response = self.client.search(index=index_name, body=search_body)
        for hit in response["hits"]["hits"]:
            article_name = hit["_source"].get("article_name", "Unknown Article")
            content = hit["_source"]["content"]
            grouped_docs[article_name] += content + " " 
        
        return dict(grouped_docs)
    
    def search_specific(self, index_name, query, filename):
            # Passo 1: Recuperação de documentos do Elasticsearch
        search_body = {
            "query": {
                "bool": {
                    "filter": {
                        "term": {
                            "article_name": filename  # Nome do arquivo fornecido
                        }
                    },
                    "must": {
                        "match": {
                            "content": query  # Conteúdo da consulta
                        }
                    }
                }
            },
            "size": 1 
        }


        grouped_docs = defaultdict(str)

        response = self.client.search(index=index_name, body=search_body)
        for hit in response["hits"]["hits"]:
            article_name = hit["_source"].get("article_name", "Unknown Article")
            content = hit["_source"]["content"]
            grouped_docs[article_name] += content + " " 
        
        return dict(grouped_docs)
    
    def _ensure_index_exists(self, index_name):
        if not self.client.indices.exists(index=index_name):
            # Defina o mapeamento do índice
            mapping = {
                "mappings": {
                    "properties": {
                        "article_name": {"type": "text"},
                        "article_fulldoc_url": {"type": "keyword"},
                        "content": {"type": "text"},
                        "article_id": {"type": "keyword"}
                    }
                }
            }
            self.client.indices.create(index=index_name, body=mapping)
            print(f"Índice '{index_name}' criado.")
        else:
            print(f"Índice '{index_name}' já existe.")

    def index(self, index_name, id, body):
        self._ensure_index_exists(index_name=index_name)
        self.client.index(index=index_name, id=id, body=body)