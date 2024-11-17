from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
from collections import defaultdict
from sentence_transformers import SentenceTransformer 

class ElasticsearchClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            load_dotenv()
            cls._instance = super(ElasticsearchClient, cls).__new__(cls)
            api_key = os.environ.get('ELASTICSEARCH_API_KEY', 'Empty')
            cls._instance.client = Elasticsearch(os.environ.get('ELASTICSEARCH_HOST', 'https://localhost:9200'), api_key=api_key)
            cls._instance.model = SentenceTransformer('all-MiniLM-L6-v2')
        return cls._instance

    def search(self, index_name, query):
        query_embedding = self.model.encode(query).tolist()

        search_body = {
                "size": 5,
                "knn": {
                    "field": "embedding",
                    "query_vector": query_embedding,
                    "k": 5
                },
                "query": {
                    "match": {
                        "content": query
                    }
                }
            }

        grouped_docs = defaultdict(str)

        response = self.client.search(index=index_name, body=search_body)
        for hit in response["hits"]["hits"]:
            article_name = hit["_source"].get("article_name", "Unknown Article")
            content = hit["_source"]["content"]
            grouped_docs[article_name] += content + " " 
        
        return dict(grouped_docs)
    
    def search_specific(self, index_name, query, filename):
        query_embedding = self.model.encode(query).tolist()

        search_body = {
            "size": 20,
            "knn": {
                "field": "embedding",
                "query_vector": query_embedding,
                "k": 20
            },
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "article_name": filename  # Nome do arquivo que você está procurando
                            }
                        },
                        {
                            "match": {
                                "content": query  # O conteúdo da consulta
                            }
                        }
                    ]
                }
            }
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
                        "article_id": {"type": "keyword"},
                        "embedding": {
                            "type": "dense_vector",
                            "dims": 384,  # Ajuste 'dims' conforme o modelo usado
                            "index": True,  # Necessário para KNN
                            "similarity": "cosine"  # Define a similaridade a ser usada
                        }
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