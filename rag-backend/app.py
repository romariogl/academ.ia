from flask import Flask, request, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch
import openai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)  # Permite comunicação com o frontend
es = Elasticsearch("http://localhost:9200")  # Conecte ao Elasticsearch

INDEX_NAME = "documents"

# Configuração da API OpenAI
openai.api_key = "os.environ.get('OPENAI-API-KEY', 'Empty')"

@app.route("/index", methods=["POST"])
def index_document():
    """
    Endpoint para indexar documentos no Elasticsearch.
    """
    data = request.json
    if not data or not data.get("text"):
        return jsonify({"error": "No document provided"}), 400

    response = es.index(index=INDEX_NAME, body=data)
    return jsonify({"result": response["result"]})

@app.route("/rag", methods=["POST"])
def rag():
    """
    Endpoint para lógica de Recuperação-Augmentação-Geração.
    """
    query = request.json.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Passo 1: Recuperação de documentos do Elasticsearch
    search_body = {
        "query": {
            "match": {
                "text": query
            }
        },
        "size": 5  # Recupera os 5 documentos mais relevantes
    }

    response = es.search(index=INDEX_NAME, body=search_body)
    retrieved_docs = [hit["_source"]["text"] for hit in response["hits"]["hits"]]

    if not retrieved_docs:
        return jsonify({"error": "No relevant documents found"}), 404

    # Passo 2: Construção do prompt com os documentos recuperados
    context = "\n\n".join(retrieved_docs)
    prompt = f"""Você é um assistente especializado em pesquisas cientificas, que responde perguntas feitas com base nos documentos de contexto. 
    Restrição: Use apenas o documento de contexto para responder e não use informações adicionais do modelo ou da internet
    
    Responda à pergunta abaixo com base nos seguintes documentos:

Documentos:
{context}

Pergunta:
{query}

Resposta:"""

    # Passo 3: Geração de resposta com modelo de linguagem (GPT)
    try:
        gpt_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        answer = gpt_response["choices"][0]["text"].strip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "query": query,
        "documents": retrieved_docs,
        "answer": answer
    })

if __name__ == "__main__":
    app.run(debug=True)
